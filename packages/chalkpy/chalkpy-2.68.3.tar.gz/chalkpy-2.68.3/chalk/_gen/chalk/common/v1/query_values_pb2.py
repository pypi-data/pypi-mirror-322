# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chalk/common/v1/query_values.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chalk._gen.chalk.common.v1 import query_log_pb2 as chalk_dot_common_dot_v1_dot_query__log__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n"chalk/common/v1/query_values.proto\x12\x0f\x63halk.common.v1\x1a\x1f\x63halk/common/v1/query_log.proto\x1a\x1fgoogle/protobuf/timestamp.proto"C\n\x1aOperationIdTableIdentifier\x12!\n\x0coperation_id\x18\x01 \x01(\tR\x0boperationId:\x02\x18\x01"y\n\x18TableNameTableIdentifier\x12\x1d\n\ntable_name\x18\x01 \x01(\tR\ttableName\x12:\n\x07\x66ilters\x18\x02 \x01(\x0b\x32 .chalk.common.v1.QueryLogFiltersR\x07\x66ilters:\x02\x18\x01"\xb1\x01\n\x17GetQueryValuesPageToken\x12J\n\x13query_timestamp_hwm\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.TimestampR\x11queryTimestampHwm\x12(\n\x10operation_id_hwm\x18\x02 \x01(\tR\x0eoperationIdHwm\x12\x1c\n\nrow_id_hwm\x18\x03 \x01(\x03R\x08rowIdHwm:\x02\x18\x01"\xda\x04\n\x15GetQueryValuesRequest\x12\x65\n\x17operation_id_identifier\x18\x01 \x01(\x0b\x32+.chalk.common.v1.OperationIdTableIdentifierH\x00R\x15operationIdIdentifier\x12_\n\x15table_name_identifier\x18\x02 \x01(\x0b\x32).chalk.common.v1.TableNameTableIdentifierH\x00R\x13tableNameIdentifier\x12l\n%query_timestamp_lower_bound_inclusive\x18\x03 \x01(\x0b\x32\x1a.google.protobuf.TimestampR!queryTimestampLowerBoundInclusive\x12q\n%query_timestamp_upper_bound_exclusive\x18\x04 \x01(\x0b\x32\x1a.google.protobuf.TimestampH\x01R!queryTimestampUpperBoundExclusive\x88\x01\x01\x12\x1a\n\x08\x66\x65\x61tures\x18\x05 \x03(\tR\x08\x66\x65\x61tures\x12\x1b\n\tpage_size\x18\x07 \x01(\x05R\x08pageSize\x12\x1d\n\npage_token\x18\x08 \x01(\tR\tpageToken:\x02\x18\x01\x42\x12\n\x10table_identifierB(\n&_query_timestamp_upper_bound_exclusive"k\n\x16GetQueryValuesResponse\x12&\n\x0fnext_page_token\x18\x01 \x01(\tR\rnextPageToken\x12\x1a\n\x07parquet\x18\x02 \x01(\x0cH\x00R\x07parquet:\x02\x18\x01\x42\t\n\x07payloadB\x85\x01\n\x13\x63om.chalk.common.v1B\x10QueryValuesProtoP\x01\xa2\x02\x03\x43\x43X\xaa\x02\x0f\x43halk.Common.V1\xca\x02\x0f\x43halk\\Common\\V1\xe2\x02\x1b\x43halk\\Common\\V1\\GPBMetadata\xea\x02\x11\x43halk::Common::V1b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "chalk.common.v1.query_values_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals["DESCRIPTOR"]._options = None
    _globals[
        "DESCRIPTOR"
    ]._serialized_options = b"\n\023com.chalk.common.v1B\020QueryValuesProtoP\001\242\002\003CCX\252\002\017Chalk.Common.V1\312\002\017Chalk\\Common\\V1\342\002\033Chalk\\Common\\V1\\GPBMetadata\352\002\021Chalk::Common::V1"
    _globals["_OPERATIONIDTABLEIDENTIFIER"]._options = None
    _globals["_OPERATIONIDTABLEIDENTIFIER"]._serialized_options = b"\030\001"
    _globals["_TABLENAMETABLEIDENTIFIER"]._options = None
    _globals["_TABLENAMETABLEIDENTIFIER"]._serialized_options = b"\030\001"
    _globals["_GETQUERYVALUESPAGETOKEN"]._options = None
    _globals["_GETQUERYVALUESPAGETOKEN"]._serialized_options = b"\030\001"
    _globals["_GETQUERYVALUESREQUEST"]._options = None
    _globals["_GETQUERYVALUESREQUEST"]._serialized_options = b"\030\001"
    _globals["_GETQUERYVALUESRESPONSE"]._options = None
    _globals["_GETQUERYVALUESRESPONSE"]._serialized_options = b"\030\001"
    _globals["_OPERATIONIDTABLEIDENTIFIER"]._serialized_start = 121
    _globals["_OPERATIONIDTABLEIDENTIFIER"]._serialized_end = 188
    _globals["_TABLENAMETABLEIDENTIFIER"]._serialized_start = 190
    _globals["_TABLENAMETABLEIDENTIFIER"]._serialized_end = 311
    _globals["_GETQUERYVALUESPAGETOKEN"]._serialized_start = 314
    _globals["_GETQUERYVALUESPAGETOKEN"]._serialized_end = 491
    _globals["_GETQUERYVALUESREQUEST"]._serialized_start = 494
    _globals["_GETQUERYVALUESREQUEST"]._serialized_end = 1096
    _globals["_GETQUERYVALUESRESPONSE"]._serialized_start = 1098
    _globals["_GETQUERYVALUESRESPONSE"]._serialized_end = 1205
# @@protoc_insertion_point(module_scope)
