#pragma once

#ifdef __cplusplus
extern "C" {
#endif

    /**
     * encrypt plain text to crypt text by TEA alg.
     * @param plain_text
     * @param crypted_text
     * @param len
     * @param iv
     * @param key
     */
  void TeaEncryptCBC(
          unsigned char *crypted_text,
          unsigned char *plain_text,
          int len,
          unsigned char iv[8],
          unsigned char key[16]);

  /**
   * decrypt crypt text to plain text by TEA alg
   * @param plain_text
   * @param crypted_text
   * @param len
   * @param iv
   * @param key
   */
  int TeaDecryptCBC(
          unsigned char *crypted_text,
          unsigned char *plain_text,
          int len,
          unsigned char iv[8],
          unsigned char key[16]);


#ifdef __cplusplus
}
#endif
