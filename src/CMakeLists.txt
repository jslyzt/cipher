file(GLOB
	CIPHER_SRCS
	
	cipher/*.c
	cipher/*/*.c
	util/*.c

	cipher/*.cpp
	cipher/*/*.cpp
	util/*.cpp
)

add_library(cipher ${CIPHER_SRCS})


file(GLOB
	UNITTEST_SRCS
	unittest/*.c
	unittest/*.cpp
)
add_executable(test ${UNITTEST_SRCS})
add_dependencies(test cipher)
