# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: chalk/auth/v1/featurepermission.proto
# Protobuf Python Version: 4.25.3
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n%chalk/auth/v1/featurepermission.proto\x12\rchalk.auth.v1"\xb0\x01\n\x12\x46\x65\x61turePermissions\x12?\n\x04tags\x18\x01 \x03(\x0b\x32+.chalk.auth.v1.FeaturePermissions.TagsEntryR\x04tags\x1aY\n\tTagsEntry\x12\x10\n\x03key\x18\x01 \x01(\tR\x03key\x12\x36\n\x05value\x18\x02 \x01(\x0e\x32 .chalk.auth.v1.FeaturePermissionR\x05value:\x02\x38\x01*\x99\x01\n\x11\x46\x65\x61turePermission\x12"\n\x1e\x46\x45\x41TURE_PERMISSION_UNSPECIFIED\x10\x00\x12\x1c\n\x18\x46\x45\x41TURE_PERMISSION_ALLOW\x10\x01\x12%\n!FEATURE_PERMISSION_ALLOW_INTERNAL\x10\x02\x12\x1b\n\x17\x46\x45\x41TURE_PERMISSION_DENY\x10\x03\x42\x91\x01\n\x11\x63om.chalk.auth.v1B\x16\x46\x65\x61turepermissionProtoP\x01Z\x0e\x61uth/v1;authv1\xa2\x02\x03\x43\x41X\xaa\x02\rChalk.Auth.V1\xca\x02\rChalk\\Auth\\V1\xe2\x02\x19\x43halk\\Auth\\V1\\GPBMetadata\xea\x02\x0f\x43halk::Auth::V1b\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, "chalk.auth.v1.featurepermission_pb2", _globals)
if _descriptor._USE_C_DESCRIPTORS == False:
    _globals["DESCRIPTOR"]._options = None
    _globals[
        "DESCRIPTOR"
    ]._serialized_options = b"\n\021com.chalk.auth.v1B\026FeaturepermissionProtoP\001Z\016auth/v1;authv1\242\002\003CAX\252\002\rChalk.Auth.V1\312\002\rChalk\\Auth\\V1\342\002\031Chalk\\Auth\\V1\\GPBMetadata\352\002\017Chalk::Auth::V1"
    _globals["_FEATUREPERMISSIONS_TAGSENTRY"]._options = None
    _globals["_FEATUREPERMISSIONS_TAGSENTRY"]._serialized_options = b"8\001"
    _globals["_FEATUREPERMISSION"]._serialized_start = 236
    _globals["_FEATUREPERMISSION"]._serialized_end = 389
    _globals["_FEATUREPERMISSIONS"]._serialized_start = 57
    _globals["_FEATUREPERMISSIONS"]._serialized_end = 233
    _globals["_FEATUREPERMISSIONS_TAGSENTRY"]._serialized_start = 144
    _globals["_FEATUREPERMISSIONS_TAGSENTRY"]._serialized_end = 233
# @@protoc_insertion_point(module_scope)
