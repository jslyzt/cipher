#pragma once

#ifdef  __cplusplus
extern "C" {
#endif

    void PKCS5_PBKDF2_HMAC(const unsigned char *password, size_t plen,
        const unsigned char *salt, size_t slen,
        const unsigned long iteration_count, const unsigned long key_length,
        unsigned char *output);
    void PKCS5_PBKDF2_HMAC2(const unsigned char *password, size_t plen,
        const unsigned char *salt, size_t slen,
        const unsigned long iteration_count, const unsigned long key_length,
        unsigned char *output);
    void PKCS5_PBKDF2_HMAC5(const unsigned char *password, size_t plen,
        const unsigned char *salt, size_t slen,
        const unsigned long iteration_count, const unsigned long key_length,
        unsigned char *output);
        
#ifdef  __cplusplus
}
#endif