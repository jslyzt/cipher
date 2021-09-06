#pragma once

#ifdef __cplusplus
extern "C"{
#endif

unsigned char * base64_encode(const unsigned char *src, size_t len,
			      size_t *out_len);
unsigned char * base64_decode(const unsigned char *src, size_t len,
			      size_t *out_len);

#ifdef __cplusplus
}
#endif
