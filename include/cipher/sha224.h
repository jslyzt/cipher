#pragma once

#include "sha256.h"

#ifdef  __cplusplus
extern "C" {
#endif

    void SHA224_Init(SHA256_State * s);
    void SHA224_Bytes(SHA256_State * s, const void *p, int len);
    void SHA224_Final(SHA256_State * s, unsigned char *output);
    void SHA224_Simple(const void *p, int len, unsigned char *output);

#ifdef  __cplusplus
}
#endif