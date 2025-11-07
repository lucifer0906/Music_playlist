# Quick Start Guide

## Prerequisites

- **C Compiler**: GCC (MinGW on Windows, gcc on Linux/macOS)
- **Python**: 3.8 or higher
- **pip**: Python package manager

## Step 1: Build the C Library

### Windows:
```bash
cd c_code
gcc -shared -o playlist.dll playlist.c
```

Or use the build script:
```bash
build.bat
```

### Linux:
```bash
cd c_code
gcc -fPIC -shared -o playlist.so playlist.c
```

Or use the build script:
```bash
chmod +x build.sh
./build.sh
```

### macOS:
```bash
cd c_code
gcc -fPIC -shared -o playlist.dylib playlist.c
```

## Step 2: Install Python Dependencies

```bash
cd python_app
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

## Step 3: Add Songs

Place your audio files (`.mp3`, `.wav`, `.ogg`, etc.) in the `Songs/` or `songs/` directory at the project root.

## Step 4: Run the Application

```bash
cd python_app
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`

## Step 5: Using the App

1. **Discover**: Browse and play songs
2. **Playlist**: View all songs in your playlist
3. **Favorites**: View songs you've played 3+ times
4. **Stats**: See statistics about your playlist
5. **Upload**: Add new songs via the web interface

## Troubleshooting

### Library not found
- Make sure you built the C library in step 1
- Check that the `.dll`, `.so`, or `.dylib` file exists in `c_code/`

### Songs not loading
- Verify audio files are in `Songs/` or `songs/` directory
- Check file extensions are supported (`.mp3`, `.wav`, `.ogg`, `.m4a`, `.flac`)

### Import errors
- Make sure you activated the virtual environment
- Run `pip install -r requirements.txt` again

## Testing

### C Unit Tests:
```bash
cd c_code
gcc -o test_playlist test_playlist_c.c playlist.c
./test_playlist  # Linux/macOS
test_playlist.exe  # Windows
```

### Python Tests:
```bash
cd python_app
pytest ../tests/test_python.py -v
```

