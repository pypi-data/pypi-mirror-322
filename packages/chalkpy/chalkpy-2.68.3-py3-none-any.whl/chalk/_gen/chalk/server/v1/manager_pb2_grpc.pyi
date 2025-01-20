"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
from abc import (
    ABCMeta,
    abstractmethod,
)
from chalk._gen.chalk.server.v1.manager_pb2 import (
    GetClusterEnvironmentsRequest,
    GetClusterEnvironmentsResponse,
)
from grpc import (
    Channel,
    Server,
    ServicerContext,
    UnaryUnaryMultiCallable,
)

class ManagerServiceStub:
    def __init__(self, channel: Channel) -> None: ...
    GetClusterEnvironments: UnaryUnaryMultiCallable[
        GetClusterEnvironmentsRequest,
        GetClusterEnvironmentsResponse,
    ]
    """If any checks fail, this request fails."""

class ManagerServiceServicer(metaclass=ABCMeta):
    @abstractmethod
    def GetClusterEnvironments(
        self,
        request: GetClusterEnvironmentsRequest,
        context: ServicerContext,
    ) -> GetClusterEnvironmentsResponse:
        """If any checks fail, this request fails."""

def add_ManagerServiceServicer_to_server(servicer: ManagerServiceServicer, server: Server) -> None: ...
