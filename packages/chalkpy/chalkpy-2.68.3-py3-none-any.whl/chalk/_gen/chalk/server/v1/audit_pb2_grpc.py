# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from chalk._gen.chalk.server.v1 import audit_pb2 as chalk_dot_server_dot_v1_dot_audit__pb2


class AuditServiceStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.GetAuditLogs = channel.unary_unary(
            "/chalk.server.v1.AuditService/GetAuditLogs",
            request_serializer=chalk_dot_server_dot_v1_dot_audit__pb2.GetAuditLogsRequest.SerializeToString,
            response_deserializer=chalk_dot_server_dot_v1_dot_audit__pb2.GetAuditLogsResponse.FromString,
        )


class AuditServiceServicer(object):
    """Missing associated documentation comment in .proto file."""

    def GetAuditLogs(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_AuditServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "GetAuditLogs": grpc.unary_unary_rpc_method_handler(
            servicer.GetAuditLogs,
            request_deserializer=chalk_dot_server_dot_v1_dot_audit__pb2.GetAuditLogsRequest.FromString,
            response_serializer=chalk_dot_server_dot_v1_dot_audit__pb2.GetAuditLogsResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler("chalk.server.v1.AuditService", rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class AuditService(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def GetAuditLogs(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/chalk.server.v1.AuditService/GetAuditLogs",
            chalk_dot_server_dot_v1_dot_audit__pb2.GetAuditLogsRequest.SerializeToString,
            chalk_dot_server_dot_v1_dot_audit__pb2.GetAuditLogsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
