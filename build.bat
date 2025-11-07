@echo off
REM Build script for Windows (MinGW)

echo Building playlist library...

cd c_code

gcc -shared -o playlist.dll playlist.c

if %ERRORLEVEL% EQU 0 (
    echo Successfully built playlist.dll
) else (
    echo Build failed
    exit /b 1
)

cd ..

echo Build complete!

