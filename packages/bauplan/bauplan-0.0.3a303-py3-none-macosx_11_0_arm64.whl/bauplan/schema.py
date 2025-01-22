from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Dict, Generic, List, Optional, TypeVar

import google.protobuf as protobuf
from pydantic import BaseModel

from ._bpln_proto.commander.service.v2 import JobInfo, RunnerEvent
from ._bpln_proto.commander.service.v2.runner_events_pb2 import RuntimeLogEvent

T = TypeVar('T')


# Safely convert proto timestamp fields to native Python datetime
def proto_datetime_to_py_datetime(
    ts: protobuf.timestamp_pb2.Timestamp,
) -> Optional[datetime]:
    if not ts.seconds and not ts.nanos:
        return None
    return ts.ToDatetime()


class _BauplanData(BaseModel):
    def __str__(self) -> str:
        return self.__repr__()


class APIMetadata(_BauplanData):
    error: Optional[str]
    pagination_token: Optional[str]
    request_id: Optional[str]
    request_ts: Optional[int]
    request_ms: Optional[int]


class APIResponse(_BauplanData):
    data: Any
    metadata: APIMetadata
    ref: Optional[Ref] = None


class RefMetadata(_BauplanData):
    """
    Some metadata about a reference.
    """

    message: str
    committer: str
    authors: list[str]
    commit_time: str
    author_time: str
    parent_commit_hashes: list[str]
    num_commits_ahead: Optional[int]
    num_commits_behind: Optional[int]
    common_ancestor_hash: Optional[str]
    num_total_commits: int

    @classmethod
    def from_dict(cls, metadata: Optional[dict] = None) -> Optional[RefMetadata]:
        """Convert a dictionary of reference metadata to a DataCatalogRefMetadata object."""
        if metadata is None:
            return None
        return cls(
            message=metadata['commitMetaOfHEAD']['message'],
            committer=metadata['commitMetaOfHEAD']['committer'],
            authors=metadata['commitMetaOfHEAD']['authors'],
            commit_time=metadata['commitMetaOfHEAD']['commitTime'],
            author_time=metadata['commitMetaOfHEAD']['authorTime'],
            parent_commit_hashes=metadata['commitMetaOfHEAD']['parentCommitHashes'],
            num_commits_ahead=metadata['numCommitsAhead'],
            num_commits_behind=metadata['numCommitsBehind'],
            common_ancestor_hash=metadata['commonAncestorHash'],
            num_total_commits=metadata['numTotalCommits'],
        )


class Ref(_BauplanData):
    """
    A branch or a tag
    """

    name: str
    hash: str
    metadata: Optional[RefMetadata] = None

    def __str__(self) -> str:
        if self.hash:
            return f'{self.name}@{self.hash}'
        return self.name

    @classmethod
    def from_dict(cls, data: Dict) -> Ref:
        return cls(
            name=data.get('name'),
            hash=data.get('hash'),
            metadata=RefMetadata.from_dict(data.get('metadata')),
        )


class Branch(Ref):
    pass


class Namespace(_BauplanData):
    name: str


class Entry(_BauplanData):
    name: str
    namespace: str
    kind: str

    @property
    def fqn(self) -> str:
        return f'{self.namespace}.{self.name}'


class TableField(_BauplanData):
    id: int
    name: str
    required: bool
    type: str


class PartitionField(_BauplanData):
    name: str
    transform: str


class Table(Entry):
    kind: str = 'TABLE'


class TableWithMetadata(Table):
    id: str
    records: Optional[int]
    size: Optional[int]
    last_updated_ms: int
    fields: List[TableField]
    snapshots: Optional[int]
    partitions: List[PartitionField]
    metadata_location: str
    current_snapshot_id: Optional[int]
    current_schema_id: Optional[int]
    raw: Optional[Dict]


class Commit(_BauplanData):
    ref: Ref
    message: Optional[str]
    authors: list[Actor]
    authored_date: datetime
    committer: Actor
    committed_date: datetime
    parent_ref: Ref
    parent_hashes: list[str]

    @property
    def author(self) -> Actor:
        return self.authors[0]


class Actor(_BauplanData):
    name: str
    email: str | None


@dataclass
class _BauplanIteratorContext:
    page_idx: int = 0
    page_item_idx: int = 0
    idx: int = 0
    finished: bool = False

    def next_page(self) -> None:
        self.page_idx = self.page_idx + 1
        self.page_item_idx = 0

    def next_item(self, limit: int | None) -> None:
        self.page_item_idx = self.page_item_idx + 1
        self.idx = self.idx + 1
        self.finished = True if limit and self.idx >= limit else False


class _BauplanIterableCatalogAPIResponse(Generic[T]):
    ref: Ref | None = None
    responses: List[APIResponse]

    def __init__(
        self,
        data_fetcher: Callable[[int, Optional[str]], APIResponse],
        data_mapper: Callable[[Dict[str, Any]], T],
        itersize: int,
        limit: int | None = None,
    ) -> None:
        self.responses = []

        self._limit = limit
        self._itersize = itersize
        self._data_fetcher = data_fetcher
        self._data_mapper = data_mapper
        self._iter = _BauplanIteratorContext()
        self._has_next_page = True
        self._fetch_next_page()

    def values(self) -> List[T]:
        return list(self)

    def __iter__(self) -> _BauplanIterableCatalogAPIResponse[T]:
        # We need to reset the iterator context
        self._iter = _BauplanIteratorContext()
        return self

    def __getitem__(self, idx: int) -> T:
        if idx < 0:
            raise ValueError('Negative indexing is not supported')
        # TODO: this is not efficient
        pos = 0
        for res in self:
            if pos == idx:
                return res
            pos += 1
        raise IndexError('Index out of range')

    def __next__(self) -> T:
        if self._iter.finished:
            raise StopIteration
        # Get the current page
        page = self.responses[self._iter.page_idx]
        if self._iter.page_item_idx >= len(page.data):
            # We've reached the end of the current page
            self._fetch_next_page()
            self._iter.next_page()
            self._iter.finished = self._iter.page_idx >= len(self.responses)
            return self.__next__()
        # Get the current item
        item = page.data[self._iter.page_item_idx]
        self._iter.next_item(self._limit)
        return self._data_mapper(item)

    def __len__(self) -> int:
        while self._has_next_page:
            self._fetch_next_page()
        return self._response_data_len()

    def __str__(self) -> str:
        return f'{self.__class__.__name__}(ref={str(self.ref)!r}, iterator={self.responses[0].metadata.request_id!r})'

    def _response_data_len(self) -> int:
        # Actual number of items fetched over all pages
        return sum(len(page.data) for page in self.responses)

    @property
    def _next_pagination_token(self) -> Optional[str]:
        if not self._has_next_page:
            return None
        if self.responses:
            return self.responses[-1].metadata.pagination_token
        return None

    def _fetch_next_page(self) -> None:
        if not self._has_next_page:
            return
        if self._limit:
            # We should fetch only the remaining items, without exceeding the setted itersize
            missing_items = min(self._itersize, self._limit - self._response_data_len())
        else:
            # Without an explicit limit, we should fetch the itersize
            missing_items = self._itersize
        page = self._data_fetcher(missing_items, self._next_pagination_token)
        self.responses.append(page)
        if page.ref and not hasattr(self, 'ref'):
            self.ref = page.ref
        # We need to use the private __len method to prevent an infinite loop
        tot_items = self._response_data_len()
        if self._limit and tot_items >= self._limit:
            # We should stop fetching pages when we have enough items
            self._has_next_page = False
            # and remove the extra items from the last page
            if tot_items > self._limit:
                page.data = page.data[: self._limit - tot_items]
        else:
            # We should stop fetching pages when there are no more pages
            self._has_next_page = self._next_pagination_token is not None


class GetCommitsResponse(_BauplanIterableCatalogAPIResponse[Commit]):
    ref: Ref


class GetTablesResponse(_BauplanIterableCatalogAPIResponse[Table]):
    ref: Ref


class GetNamespacesResponse(_BauplanIterableCatalogAPIResponse[Namespace]):
    ref: Ref


class GetBranchesResponse(_BauplanIterableCatalogAPIResponse[Branch]): ...


class Job(BaseModel):
    """
    EXPERIMENTAL AND SUBJECT TO CHANGE.

    Job is a model for a job in the Bauplan system. It is tracked as a result
    of a code snapshot run.
    """

    id: str
    kind: str
    user: str
    status: str
    created_at: Optional[datetime]
    finished_at: Optional[datetime]

    @classmethod
    def from_proto(cls, job_pb: JobInfo) -> 'Job':
        return cls(
            id=job_pb.id,
            kind=job_pb.kind,
            user=job_pb.user,
            status=job_pb.status,
            created_at=proto_datetime_to_py_datetime(job_pb.created_at),
            finished_at=proto_datetime_to_py_datetime(job_pb.finished_at),
        )


class JobLogStream(Enum):
    STDOUT = 0
    STDERR = 1


class JobLog(BaseModel):
    """
    EXPERIMENTAL AND SUBJECT TO CHANGE.

    JobLog is a model for a log message from a job.

    When you output logs within a Python model, they are persisted as JobLogs.
    """

    message: str
    stream: JobLogStream

    @classmethod
    def from_proto(cls, log_pb: RunnerEvent) -> JobLog:
        if not log_pb.HasField('runtime_user_log'):
            raise ValueError('RunnerEvent is not a RuntimeUserLog')

        user_log = log_pb.runtime_user_log

        if user_log.output_stream == RuntimeLogEvent.OUTPUT_STREAM_STDERR:
            stream = JobLogStream.STDERR
        else:
            stream = JobLogStream.STDOUT

        return cls(message=user_log.msg, stream=stream)
