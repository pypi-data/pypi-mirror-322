// Copyright (c) ONNX Project Contributors

/*
 * SPDX-License-Identifier: Apache-2.0
 */

#pragma once

#include <filesystem>
#include <fstream>
#include <string>

#ifdef _WIN32
#include "onnx/common/path.h"
#endif
#include "onnx/checker.h"

namespace ONNX_NAMESPACE {

template <typename T>
void LoadProtoFromPath(const std::string& proto_path, T& proto) {
#ifdef _WIN32
  std::filesystem::path proto_u8_path(utf8str_to_wstring(proto_path, true));
#else
  std::filesystem::path proto_u8_path(proto_path);
#endif
  std::fstream proto_stream(proto_u8_path, std::ios::in | std::ios::binary);
  if (!proto_stream.good()) {
    fail_check("Unable to open proto file: ", proto_path, ". Please check if it is a valid proto. ");
  }
  std::string data{std::istreambuf_iterator<char>{proto_stream}, std::istreambuf_iterator<char>{}};
  if (!ParseProtoFromBytes(&proto, data.c_str(), data.size())) {
    fail_check(
        "Unable to parse proto from file: ", proto_path, ". Please check if it is a valid protobuf file of proto. ");
  }
}
} // namespace ONNX_NAMESPACE
