# Makefile for building playlist shared library
# Supports both Linux and Windows (MinGW)

# Detect OS
UNAME_S := $(shell uname -s 2>/dev/null || echo "Windows")

# Linux build
ifeq ($(UNAME_S),Linux)
	LIB_NAME = playlist.so
	CFLAGS = -fPIC -shared -Wall -Wextra
	LDFLAGS = -shared
endif

# Windows build (MinGW)
ifeq ($(UNAME_S),Windows)
	LIB_NAME = playlist.dll
	CFLAGS = -shared -Wall -Wextra
	LDFLAGS = -shared
endif

# macOS build
ifeq ($(UNAME_S),Darwin)
	LIB_NAME = playlist.dylib
	CFLAGS = -fPIC -shared -Wall -Wextra
	LDFLAGS = -shared
endif

# Default target
all: $(LIB_NAME)

$(LIB_NAME): playlist.c playlist.h
	gcc $(CFLAGS) -o $(LIB_NAME) playlist.c $(LDFLAGS)

clean:
	rm -f $(LIB_NAME) playlist.dll playlist.so playlist.dylib

# Manual build commands (for reference):
# Linux: gcc -fPIC -shared -o playlist.so playlist.c
# Windows (MinGW): gcc -shared -o playlist.dll playlist.c
# macOS: gcc -fPIC -shared -o playlist.dylib playlist.c

.PHONY: all clean

