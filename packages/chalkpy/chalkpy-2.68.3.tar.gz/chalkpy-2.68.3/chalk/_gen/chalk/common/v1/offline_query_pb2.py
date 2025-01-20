# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chalk/common/v1/offline_query.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from chalk._gen.chalk.common.v1 import chalk_error_pb2 as chalk_dot_common_dot_v1_dot_chalk__error__pb2
from chalk._gen.chalk.common.v1 import online_query_pb2 as chalk_dot_common_dot_v1_dot_online__query__pb2
from chalk._gen.chalk.expression.v1 import expression_pb2 as chalk_dot_expression_dot_v1_dot_expression__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n#chalk/common/v1/offline_query.proto\x12\x0f\x63halk.common.v1\x1a!chalk/common/v1/chalk_error.proto\x1a"chalk/common/v1/online_query.proto\x1a$chalk/expression/v1/expression.proto"\xdc\x01\n\x1dOfflineQueryRecomputeFeatures\x12 \n\x0b\x61ll_or_none\x18\x01 \x01(\x08H\x00R\tallOrNone\x12_\n\x0c\x66\x65\x61ture_list\x18\x02 \x01(\x0b\x32:.chalk.common.v1.OfflineQueryRecomputeFeatures.FeatureListH\x00R\x0b\x66\x65\x61tureList\x1a\x30\n\x0b\x46\x65\x61tureList\x12!\n\x0c\x66\x65\x61ture_list\x18\x01 \x03(\tR\x0b\x66\x65\x61tureListB\x06\n\x04impl"\x80\x01\n\x13OfflineQueryExplain\x12\x18\n\x06truthy\x18\x01 \x01(\x08H\x00R\x06truthy\x12?\n\x04only\x18\x02 \x01(\x0b\x32).chalk.common.v1.OfflineQueryExplain.OnlyH\x00R\x04only\x1a\x06\n\x04OnlyB\x06\n\x04impl"\x9e\x01\n\x12OfflineQueryInputs\x12\'\n\x0e\x66\x65\x61ther_inputs\x18\x01 \x01(\x0cH\x00R\rfeatherInputs\x12K\n\tno_inputs\x18\x02 \x01(\x0b\x32,.chalk.common.v1.OfflineQueryInputs.NoInputsH\x00R\x08noInputs\x1a\n\n\x08NoInputsB\x06\n\x04impl"\xf7\x07\n\x13OfflineQueryRequest\x12;\n\x06inputs\x18\x01 \x01(\x0b\x32#.chalk.common.v1.OfflineQueryInputsR\x06inputs\x12\x18\n\x07outputs\x18\x02 \x03(\tR\x07outputs\x12)\n\x10required_outputs\x18\x03 \x03(\tR\x0frequiredOutputs\x12-\n\x12\x64\x65stination_format\x18\x04 \x01(\tR\x11\x64\x65stinationFormat\x12\x1b\n\x06\x62ranch\x18\x05 \x01(\tH\x00R\x06\x62ranch\x88\x01\x01\x12&\n\x0c\x64\x61taset_name\x18\x06 \x01(\tH\x01R\x0b\x64\x61tasetName\x88\x01\x01\x12]\n\x12recompute_features\x18\x07 \x01(\x0b\x32..chalk.common.v1.OfflineQueryRecomputeFeaturesR\x11recomputeFeatures\x12*\n\x11store_plan_stages\x18\x08 \x01(\x08R\x0fstorePlanStages\x12>\n\x07\x66ilters\x18\x0b \x03(\x0b\x32$.chalk.expression.v1.LogicalExprNodeR\x07\x66ilters\x12$\n\x0bmax_samples\x18\x65 \x01(\x05H\x02R\nmaxSamples\x88\x01\x01\x12\x30\n\x12max_cache_age_secs\x18\x66 \x01(\x05H\x03R\x0fmaxCacheAgeSecs\x88\x01\x01\x12\x42\n\x07\x65xplain\x18g \x01(\x0b\x32$.chalk.common.v1.OfflineQueryExplainB\x02\x18\x01R\x07\x65xplain\x12;\n\x08\x65xplain2\x18j \x01(\x0b\x32\x1f.chalk.common.v1.ExplainOptionsR\x08\x65xplain2\x12\x12\n\x04tags\x18h \x03(\tR\x04tags\x12*\n\x0e\x63orrelation_id\x18i \x01(\tH\x04R\rcorrelationId\x88\x01\x01\x12;\n\x17observed_at_lower_bound\x18\xc9\x01 \x01(\tH\x05R\x14observedAtLowerBound\x88\x01\x01\x12;\n\x17observed_at_upper_bound\x18\xca\x01 \x01(\tH\x06R\x14observedAtUpperBound\x88\x01\x01\x42\t\n\x07_branchB\x0f\n\r_dataset_nameB\x0e\n\x0c_max_samplesB\x15\n\x13_max_cache_age_secsB\x11\n\x0f_correlation_idB\x1a\n\x18_observed_at_lower_boundB\x1a\n\x18_observed_at_upper_bound"\xce\x01\n\x12\x43olumnMetadataList\x12N\n\x08metadata\x18\x01 \x03(\x0b\x32\x32.chalk.common.v1.ColumnMetadataList.ColumnMetadataR\x08metadata\x1ah\n\x0e\x43olumnMetadata\x12\x1f\n\x0b\x66\x65\x61ture_fqn\x18\x01 \x01(\tR\nfeatureFqn\x12\x1f\n\x0b\x63olumn_name\x18\x02 \x01(\tR\ncolumnName\x12\x14\n\x05\x64type\x18\x03 \x01(\tR\x05\x64type"\xf0\x01\n\x1aGetOfflineQueryJobResponse\x12\x1f\n\x0bis_finished\x18\x01 \x01(\x08R\nisFinished\x12\x18\n\x07version\x18\x02 \x01(\x05R\x07version\x12\x12\n\x04urls\x18\x03 \x03(\tR\x04urls\x12\x33\n\x06\x65rrors\x18\x04 \x03(\x0b\x32\x1b.chalk.common.v1.ChalkErrorR\x06\x65rrors\x12\x42\n\x07\x63olumns\x18\x05 \x01(\x0b\x32#.chalk.common.v1.ColumnMetadataListH\x00R\x07\x63olumns\x88\x01\x01\x42\n\n\x08_columnsB\x86\x01\n\x13\x63om.chalk.common.v1B\x11OfflineQueryProtoP\x01\xa2\x02\x03\x43\x43X\xaa\x02\x0f\x43halk.Common.V1\xca\x02\x0f\x43halk\\Common\\V1\xe2\x02\x1b\x43halk\\Common\\V1\\GPBMetadata\xea\x02\x11\x43halk::Common::V1b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "chalk.common.v1.offline_query_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals["DESCRIPTOR"]._options = None
    _globals[
        "DESCRIPTOR"
    ]._serialized_options = b"\n\023com.chalk.common.v1B\021OfflineQueryProtoP\001\242\002\003CCX\252\002\017Chalk.Common.V1\312\002\017Chalk\\Common\\V1\342\002\033Chalk\\Common\\V1\\GPBMetadata\352\002\021Chalk::Common::V1"
    _globals["_OFFLINEQUERYREQUEST"].fields_by_name["explain"]._options = None
    _globals["_OFFLINEQUERYREQUEST"].fields_by_name["explain"]._serialized_options = b"\030\001"
    _globals["_OFFLINEQUERYRECOMPUTEFEATURES"]._serialized_start = 166
    _globals["_OFFLINEQUERYRECOMPUTEFEATURES"]._serialized_end = 386
    _globals["_OFFLINEQUERYRECOMPUTEFEATURES_FEATURELIST"]._serialized_start = 330
    _globals["_OFFLINEQUERYRECOMPUTEFEATURES_FEATURELIST"]._serialized_end = 378
    _globals["_OFFLINEQUERYEXPLAIN"]._serialized_start = 389
    _globals["_OFFLINEQUERYEXPLAIN"]._serialized_end = 517
    _globals["_OFFLINEQUERYEXPLAIN_ONLY"]._serialized_start = 503
    _globals["_OFFLINEQUERYEXPLAIN_ONLY"]._serialized_end = 509
    _globals["_OFFLINEQUERYINPUTS"]._serialized_start = 520
    _globals["_OFFLINEQUERYINPUTS"]._serialized_end = 678
    _globals["_OFFLINEQUERYINPUTS_NOINPUTS"]._serialized_start = 660
    _globals["_OFFLINEQUERYINPUTS_NOINPUTS"]._serialized_end = 670
    _globals["_OFFLINEQUERYREQUEST"]._serialized_start = 681
    _globals["_OFFLINEQUERYREQUEST"]._serialized_end = 1696
    _globals["_COLUMNMETADATALIST"]._serialized_start = 1699
    _globals["_COLUMNMETADATALIST"]._serialized_end = 1905
    _globals["_COLUMNMETADATALIST_COLUMNMETADATA"]._serialized_start = 1801
    _globals["_COLUMNMETADATALIST_COLUMNMETADATA"]._serialized_end = 1905
    _globals["_GETOFFLINEQUERYJOBRESPONSE"]._serialized_start = 1908
    _globals["_GETOFFLINEQUERYJOBRESPONSE"]._serialized_end = 2148
# @@protoc_insertion_point(module_scope)
