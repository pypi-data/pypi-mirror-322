# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chalk/chart/v1/densetimeserieschart.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chalk._gen.chalk.arrow.v1 import arrow_pb2 as chalk_dot_arrow_dot_v1_dot_arrow__pb2
from google.protobuf import duration_pb2 as google_dot_protobuf_dot_duration__pb2
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n)chalk/chart/v1/densetimeserieschart.proto\x12\x0e\x63halk.chart.v1\x1a\x1a\x63halk/arrow/v1/arrow.proto\x1a\x1egoogle/protobuf/duration.proto\x1a\x1fgoogle/protobuf/timestamp.proto"1\n\nDensePoint\x12\x19\n\x05value\x18\x01 \x01(\x01H\x00R\x05value\x88\x01\x01\x42\x08\n\x06_value"Z\n\x08GroupTag\x12\x1b\n\tgroup_key\x18\x01 \x01(\tR\x08groupKey\x12\x31\n\x05value\x18\x02 \x01(\x0b\x32\x1b.chalk.arrow.v1.ScalarValueR\x05value"\xa8\x01\n\x0f\x44\x65nseTimeSeries\x12\x32\n\x06points\x18\x01 \x03(\x0b\x32\x1a.chalk.chart.v1.DensePointR\x06points\x12\x14\n\x05label\x18\x02 \x01(\tR\x05label\x12\x12\n\x04unit\x18\x03 \x01(\tR\x04unit\x12\x37\n\ngroup_tags\x18\x04 \x03(\x0b\x32\x18.chalk.chart.v1.GroupTagR\tgroupTags"\xdc\x01\n\x14\x44\x65nseTimeSeriesChart\x12\x14\n\x05title\x18\x01 \x01(\tR\x05title\x12\x37\n\x06series\x18\x02 \x03(\x0b\x32\x1f.chalk.chart.v1.DenseTimeSeriesR\x06series\x12\x35\n\x08x_series\x18\x03 \x03(\x0b\x32\x1a.google.protobuf.TimestampR\x07xSeries\x12>\n\rwindow_period\x18\x04 \x01(\x0b\x32\x19.google.protobuf.DurationR\x0cwindowPeriodB\x9d\x01\n\x12\x63om.chalk.chart.v1B\x19\x44\x65nsetimeserieschartProtoP\x01Z\x12server/v1;serverv1\xa2\x02\x03\x43\x43X\xaa\x02\x0e\x43halk.Chart.V1\xca\x02\x0e\x43halk\\Chart\\V1\xe2\x02\x1a\x43halk\\Chart\\V1\\GPBMetadata\xea\x02\x10\x43halk::Chart::V1b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "chalk.chart.v1.densetimeserieschart_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals["DESCRIPTOR"]._options = None
    _globals[
        "DESCRIPTOR"
    ]._serialized_options = b"\n\022com.chalk.chart.v1B\031DensetimeserieschartProtoP\001Z\022server/v1;serverv1\242\002\003CCX\252\002\016Chalk.Chart.V1\312\002\016Chalk\\Chart\\V1\342\002\032Chalk\\Chart\\V1\\GPBMetadata\352\002\020Chalk::Chart::V1"
    _globals["_DENSEPOINT"]._serialized_start = 154
    _globals["_DENSEPOINT"]._serialized_end = 203
    _globals["_GROUPTAG"]._serialized_start = 205
    _globals["_GROUPTAG"]._serialized_end = 295
    _globals["_DENSETIMESERIES"]._serialized_start = 298
    _globals["_DENSETIMESERIES"]._serialized_end = 466
    _globals["_DENSETIMESERIESCHART"]._serialized_start = 469
    _globals["_DENSETIMESERIESCHART"]._serialized_end = 689
# @@protoc_insertion_point(module_scope)
