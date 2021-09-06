file(GLOB
	CIPHER_SRCS
	*.c
	cipher/*.c
	cipher/*/*.c

	*.cpp
	cipher/*.cpp
	cipher/*/*.cpp
)

add_library(cipher ${CIPHER_SRCS})


file(GLOB
	UNITTEST_SRCS
	unittest/*.c
	unittest/*.cpp
)
add_executable(test ${UNITTEST_SRCS})
add_dependencies(test cipher)
