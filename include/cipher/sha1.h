#pragma once

#ifdef __cplusplus
extern "C" {
#endif

    typedef struct {
        unsigned int state[5];
        unsigned int count[2];
        unsigned char buffer[64];
    } SHA1_CTX;

    void SHA1Transform(unsigned int state[5], const unsigned char buffer[64]);
    void SHA1Init(SHA1_CTX* context);
    void SHA1Update(SHA1_CTX* context, const unsigned char* data, unsigned int len);
    void SHA1Final(unsigned char digest[20], SHA1_CTX* context);
    // The function to calculate the message digest string
    // of a given string based on the SHA1 algrithm.
    void SHA1Calc(const unsigned char *input, unsigned int inlen, unsigned char *output);

    
#ifdef __cplusplus
}
#endif
