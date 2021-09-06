#pragma once

#include <string>

bool Base64Encode(const std::string& input, std::string* output);
bool Base64Encode(const std::string& input, char* output, size_t* len);

bool Base64Decode(const std::string& input, std::string* output);
bool Base64Decode(const std::string& input, char* output, size_t* len);
