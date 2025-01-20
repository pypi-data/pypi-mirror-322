# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chalk/engine/v2/query_log.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chalk._gen.chalk.common.v1 import operation_kind_pb2 as chalk_dot_common_dot_v1_dot_operation__kind__pb2
from chalk._gen.chalk.common.v1 import query_status_pb2 as chalk_dot_common_dot_v1_dot_query__status__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\x1f\x63halk/engine/v2/query_log.proto\x12\x0f\x63halk.engine.v2\x1a$chalk/common/v1/operation_kind.proto\x1a"chalk/common/v1/query_status.proto\x1a\x1fgoogle/protobuf/timestamp.proto"}\n\x12VersionedQueryName\x12\x1d\n\nquery_name\x18\x01 \x01(\tR\tqueryName\x12\x31\n\x12query_name_version\x18\x02 \x01(\tH\x00R\x10queryNameVersion\x88\x01\x01\x42\x15\n\x13_query_name_version"\xef\x03\n\x0fQueryLogFilters\x12!\n\x0coperation_id\x18\x01 \x03(\tR\x0boperationId\x12\x45\n\x0eoperation_kind\x18\x02 \x03(\x0e\x32\x1e.chalk.common.v1.OperationKindR\roperationKind\x12\x42\n\nquery_name\x18\x03 \x03(\x0b\x32#.chalk.engine.v2.VersionedQueryNameR\tqueryName\x12\x19\n\x08\x61gent_id\x18\x05 \x03(\tR\x07\x61gentId\x12\x1f\n\x0b\x62ranch_name\x18\x06 \x03(\tR\nbranchName\x12%\n\x0e\x63orrelation_id\x18\x07 \x03(\tR\rcorrelationId\x12\x19\n\x08trace_id\x18\x08 \x03(\tR\x07traceId\x12"\n\rquery_plan_id\x18\t \x03(\tR\x0bqueryPlanId\x12#\n\rdeployment_id\x18\n \x03(\tR\x0c\x64\x65ploymentId\x12?\n\x0cquery_status\x18\x0b \x03(\x0e\x32\x1c.chalk.common.v1.QueryStatusR\x0bqueryStatus\x12&\n\x0fmeta_query_hash\x18\x0c \x03(\tR\rmetaQueryHash"\x93\x01\n\x1bGetQueryLogEntriesPageToken\x12(\n\x10operation_id_hwm\x18\x01 \x01(\tR\x0eoperationIdHwm\x12J\n\x13query_timestamp_hwm\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x11queryTimestampHwm"\x9e\x03\n\x19GetQueryLogEntriesRequest\x12l\n%query_timestamp_lower_bound_inclusive\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampR!queryTimestampLowerBoundInclusive\x12q\n%query_timestamp_upper_bound_exclusive\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x00R!queryTimestampUpperBoundExclusive\x88\x01\x01\x12:\n\x07\x66ilters\x18\x03 \x01(\x0b\x32 .chalk.engine.v2.QueryLogFiltersR\x07\x66ilters\x12\x1b\n\tpage_size\x18\x04 \x01(\x05R\x08pageSize\x12\x1d\n\npage_token\x18\x05 \x01(\tR\tpageTokenB(\n&_query_timestamp_upper_bound_exclusive"\xa3\x06\n\rQueryLogEntry\x12!\n\x0coperation_id\x18\x01 \x01(\tR\x0boperationId\x12%\n\x0e\x65nvironment_id\x18\x02 \x01(\tR\renvironmentId\x12#\n\rdeployment_id\x18\x03 \x01(\tR\x0c\x64\x65ploymentId\x12\x45\n\x0eoperation_kind\x18\x04 \x01(\x0e\x32\x1e.chalk.common.v1.OperationKindR\roperationKind\x12\x43\n\x0fquery_timestamp\x18\x05 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x0equeryTimestamp\x12L\n\x14\x65xecution_started_at\x18\x06 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x12\x65xecutionStartedAt\x12N\n\x15\x65xecution_finished_at\x18\x07 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x13\x65xecutionFinishedAt\x12?\n\x0cquery_status\x18\x08 \x01(\x0e\x32\x1c.chalk.common.v1.QueryStatusR\x0bqueryStatus\x12\x1d\n\nquery_name\x18\t \x01(\tR\tqueryName\x12,\n\x12query_name_version\x18\n \x01(\tR\x10queryNameVersion\x12\x19\n\x08\x61gent_id\x18\x0b \x01(\tR\x07\x61gentId\x12\x1f\n\x0b\x62ranch_name\x18\x0c \x01(\tR\nbranchName\x12%\n\x0e\x63orrelation_id\x18\r \x01(\tR\rcorrelationId\x12\x19\n\x08trace_id\x18\x0e \x01(\tR\x07traceId\x12"\n\rquery_plan_id\x18\x0f \x01(\tR\x0bqueryPlanId\x12!\n\x0cvalue_tables\x18\x10 \x03(\tR\x0bvalueTables\x12&\n\x0fmeta_query_hash\x18\x11 \x01(\tR\rmetaQueryHash"~\n\x1aGetQueryLogEntriesResponse\x12\x38\n\x07\x65ntries\x18\x01 \x03(\x0b\x32\x1e.chalk.engine.v2.QueryLogEntryR\x07\x65ntries\x12&\n\x0fnext_page_token\x18\x02 \x01(\tR\rnextPageTokenB\x82\x01\n\x13\x63om.chalk.engine.v2B\rQueryLogProtoP\x01\xa2\x02\x03\x43\x45X\xaa\x02\x0f\x43halk.Engine.V2\xca\x02\x0f\x43halk\\Engine\\V2\xe2\x02\x1b\x43halk\\Engine\\V2\\GPBMetadata\xea\x02\x11\x43halk::Engine::V2b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "chalk.engine.v2.query_log_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals["DESCRIPTOR"]._options = None
    _globals[
        "DESCRIPTOR"
    ]._serialized_options = b"\n\023com.chalk.engine.v2B\rQueryLogProtoP\001\242\002\003CEX\252\002\017Chalk.Engine.V2\312\002\017Chalk\\Engine\\V2\342\002\033Chalk\\Engine\\V2\\GPBMetadata\352\002\021Chalk::Engine::V2"
    _globals["_VERSIONEDQUERYNAME"]._serialized_start = 159
    _globals["_VERSIONEDQUERYNAME"]._serialized_end = 284
    _globals["_QUERYLOGFILTERS"]._serialized_start = 287
    _globals["_QUERYLOGFILTERS"]._serialized_end = 782
    _globals["_GETQUERYLOGENTRIESPAGETOKEN"]._serialized_start = 785
    _globals["_GETQUERYLOGENTRIESPAGETOKEN"]._serialized_end = 932
    _globals["_GETQUERYLOGENTRIESREQUEST"]._serialized_start = 935
    _globals["_GETQUERYLOGENTRIESREQUEST"]._serialized_end = 1349
    _globals["_QUERYLOGENTRY"]._serialized_start = 1352
    _globals["_QUERYLOGENTRY"]._serialized_end = 2155
    _globals["_GETQUERYLOGENTRIESRESPONSE"]._serialized_start = 2157
    _globals["_GETQUERYLOGENTRIESRESPONSE"]._serialized_end = 2283
# @@protoc_insertion_point(module_scope)
