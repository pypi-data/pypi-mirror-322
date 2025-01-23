#ifndef SIGTOOL_HASH_H
#define SIGTOOL_HASH_H

#include <cstddef>
#include <string>
#include "magic_numbers.h"

namespace SigTool {
struct SHA256Hash {
    static const int constexpr hashSize = 32;
    static const int constexpr hashType = CS_HASHTYPE_SHA256;
    char bytes[hashSize]{};

    SHA256Hash(const char *data, size_t len);
    SHA256Hash(const unsigned char *data, size_t len);

    explicit SHA256Hash(const std::string &str);

    SHA256Hash(): bytes{} {};
};

using Hash = SHA256Hash;
};

#endif
