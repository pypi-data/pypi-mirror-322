# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: onnx/onnx-operators-ml.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from onnx import onnx_ml_pb2 as onnx_dot_onnx__ml__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1connx/onnx-operators-ml.proto\x12\x04onnx\x1a\x12onnx/onnx-ml.proto\"q\n\rOperatorProto\x12\x0f\n\x07op_type\x18\x01 \x01(\t\x12\x15\n\rsince_version\x18\x02 \x01(\x03\x12$\n\x06status\x18\x03 \x01(\x0e\x32\x14.onnx.OperatorStatus\x12\x12\n\ndoc_string\x18\n \x01(\t\"\xf9\x01\n\x10OperatorSetProto\x12\r\n\x05magic\x18\x01 \x01(\t\x12\x12\n\nir_version\x18\x02 \x01(\x03\x12\x1d\n\x15ir_version_prerelease\x18\x03 \x01(\t\x12\x19\n\x11ir_build_metadata\x18\x07 \x01(\t\x12\x0e\n\x06\x64omain\x18\x04 \x01(\t\x12\x15\n\ropset_version\x18\x05 \x01(\x03\x12\x12\n\ndoc_string\x18\x06 \x01(\t\x12%\n\x08operator\x18\x08 \x03(\x0b\x32\x13.onnx.OperatorProto\x12&\n\tfunctions\x18\t \x03(\x0b\x32\x13.onnx.FunctionProtoB\x02H\x03')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'onnx.onnx_operators_ml_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'H\003'
  _OPERATORPROTO._serialized_start=58
  _OPERATORPROTO._serialized_end=171
  _OPERATORSETPROTO._serialized_start=174
  _OPERATORSETPROTO._serialized_end=423
# @@protoc_insertion_point(module_scope)
