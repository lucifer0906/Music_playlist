#!/bin/bash
# Build script for Linux/macOS

echo "Building playlist library..."

cd c_code

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "Building for Linux..."
    gcc -fPIC -shared -o playlist.so playlist.c
    if [ $? -eq 0 ]; then
        echo "✓ Successfully built playlist.so"
    else
        echo "✗ Build failed"
        exit 1
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "Building for macOS..."
    gcc -fPIC -shared -o playlist.dylib playlist.c
    if [ $? -eq 0 ]; then
        echo "✓ Successfully built playlist.dylib"
    else
        echo "✗ Build failed"
        exit 1
    fi
else
    echo "Unsupported OS. Please build manually."
    exit 1
fi

cd ..

echo "Build complete!"

