"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
from abc import (
    ABCMeta,
    abstractmethod,
)
from chalk._gen.chalk.server.v1.log_pb2 import (
    SearchLogEntriesRequest,
    SearchLogEntriesResponse,
)
from grpc import (
    Channel,
    Server,
    ServicerContext,
    UnaryUnaryMultiCallable,
)

class LogSearchServiceStub:
    def __init__(self, channel: Channel) -> None: ...
    SearchLogEntries: UnaryUnaryMultiCallable[
        SearchLogEntriesRequest,
        SearchLogEntriesResponse,
    ]

class LogSearchServiceServicer(metaclass=ABCMeta):
    @abstractmethod
    def SearchLogEntries(
        self,
        request: SearchLogEntriesRequest,
        context: ServicerContext,
    ) -> SearchLogEntriesResponse: ...

def add_LogSearchServiceServicer_to_server(servicer: LogSearchServiceServicer, server: Server) -> None: ...
