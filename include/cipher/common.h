#pragma once

#include <stdint.h>
#include <string.h>

#ifdef WIN32
#include <winsock2.h>
#else
#include <endian.h>
#endif

uint16_t static inline ReadLE16(const unsigned char* ptr)
{
	uint16_t x;
	memcpy((char*)&x, ptr, 2);
#ifdef WIN32
	return ntohs(x);
#else
	return le16toh(x);
#endif
}

uint32_t static inline ReadLE32(const unsigned char* ptr)
{
	uint32_t x;
	memcpy((char*)&x, ptr, 4);
#ifdef WIN32
	return ntohl(x);
#else
	return le32toh(x);
#endif
}

uint64_t static inline ReadLE64(const unsigned char* ptr)
{
	uint64_t x;
	memcpy((char*)&x, ptr, 8);
#ifdef WIN32
	return ntohll(x);
#else
	return le64toh(x);
#endif
}

void static inline WriteLE16(unsigned char* ptr, uint16_t x)
{
#ifdef WIN32
	uint16_t v = htons(x);
#else
	uint16_t v = htole16(x);
#endif
	memcpy(ptr, (char*)&v, 2);
}

void static inline WriteLE32(unsigned char* ptr, uint32_t x)
{
#ifdef WIN32
	uint32_t v = htonl(x);
#else
	uint32_t v = htole32(x);
#endif
	memcpy(ptr, (char*)&v, 4);
}

void static inline WriteLE64(unsigned char* ptr, uint64_t x)
{
#ifdef WIN32
	uint64_t v = htonll(x);
#else
	uint64_t v = htole64(x);
#endif
	memcpy(ptr, (char*)&v, 8);
}

uint32_t static inline ReadBE32(const unsigned char* ptr)
{
	uint32_t x;
	memcpy((char*)&x, ptr, 4);
#ifdef WIN32
	return ntohl(x);
#else
	return be32toh(x);
#endif
}

uint64_t static inline ReadBE64(const unsigned char* ptr)
{
	uint64_t x;
	memcpy((char*)&x, ptr, 8);
#ifdef WIN32
	return ntohll(x);
#else
	return be64toh(x);
#endif
}

void static inline WriteBE32(unsigned char* ptr, uint32_t x)
{
#ifdef WIN32
	uint32_t v = htonl(x);
#else
	uint32_t v = htobe32(x);
#endif
	memcpy(ptr, (char*)&v, 4);
}

void static inline WriteBE64(unsigned char* ptr, uint64_t x)
{
#ifdef WIN32
	uint32_t v = htonll(x);
#else
	uint64_t v = htobe64(x);
#endif
	memcpy(ptr, (char*)&v, 8);
}

/** Return the smallest number n such that (x >> n) == 0 (or 64 if the highest bit in x is set. */
uint64_t static inline CountBits(uint64_t x)
{
#ifdef HAVE_DECL___BUILTIN_CLZL
	if (sizeof(unsigned long) >= sizeof(uint64_t)) {
		return x ? 8 * sizeof(unsigned long) - __builtin_clzl(x) : 0;
	}
#endif
#ifdef HAVE_DECL___BUILTIN_CLZLL
	if (sizeof(unsigned long long) >= sizeof(uint64_t)) {
		return x ? 8 * sizeof(unsigned long long) - __builtin_clzll(x) : 0;
	}
#endif
	int ret = 0;
	while (x) {
		x >>= 1;
		++ret;
	}
	return ret;
}
