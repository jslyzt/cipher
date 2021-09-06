#pragma once

#ifdef  __cplusplus
extern "C" {
#endif

void aes256_encrypt_pubkey(unsigned char *key, unsigned char *blk, int len);
void aes256_decrypt_pubkey(unsigned char *key, unsigned char *blk, int len);

#ifdef  __cplusplus
}
#endif
