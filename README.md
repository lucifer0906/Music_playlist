# Spotify-style Music Playlist Application

A polished music playlist management system with a Spotify-like dark-themed UI, built with Streamlit frontend and C backend implementing a circular doubly linked list data structure.

## Project Structure

```
music_playlist_project/
├── c_code/
│   ├── playlist.h          # C header file with data structures and function declarations
│   ├── playlist.c          # C implementation (circular doubly linked list)
│   └── Makefile            # Build configuration for Linux/Windows
├── python_app/
│   ├── playlist.py         # Python ctypes wrapper for C library
│   ├── app.py              # Streamlit dashboard application
│   ├── style.css           # Custom CSS styling (Spotify-like dark theme)
│   ├── requirements.txt    # Python dependencies
│   └── assets/             # Cover images and icons
│       └── default.jpg     # Default album cover
├── songs/                  # Directory for audio files (mp3, wav, ogg, etc.)
├── tests/
│   ├── test_playlist_c.c   # C unit tests
│   └── test_python.py      # Python integration tests
├── README.md               # This file
└── DS_REPORT.md            # Data Structures report
```

## Features

- **Circular Doubly Linked List**: Efficient playlist management in C
- **Spotify-like UI**: Dark theme with glassmorphism effects, green accents
- **Play Count Tracking**: Automatically tracks plays per song
- **Favorites System**: Songs become favorites after 3+ plays
- **Audio Playback**: HTML5 audio player integrated in Streamlit
- **Song Upload**: Upload new songs via web interface
- **Search Functionality**: Search songs in playlist
- **Persistent Storage**: Save/load playlist data (play counts, favorites)
- **Responsive Design**: Works on different screen sizes

## Build Instructions

### Linux

1. **Build the C library:**
   ```bash
   cd c_code
   make
   # Or manually:
   gcc -fPIC -shared -o playlist.so playlist.c
   ```

2. **Set up Python environment:**
   ```bash
   cd ../python_app
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

### Windows (MinGW)

1. **Build the C library:**
   ```bash
   cd c_code
   gcc -shared -o playlist.dll playlist.c
   ```

2. **Set up Python environment:**
   ```bash
   cd ..\python_app
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

### macOS

1. **Build the C library:**
   ```bash
   cd c_code
   gcc -fPIC -shared -o playlist.dylib playlist.c
   ```

2. **Set up Python environment:**
   ```bash
   cd ../python_app
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Add Songs:**
   - Place audio files (`.mp3`, `.wav`, `.ogg`, `.m4a`, `.flac`) in the `/songs` directory
   - The app will automatically load them on startup
   - Or use the Upload page to add songs via the web interface

2. **Play Songs:**
   - Click the "Play" button on any song card
   - Use the bottom player bar controls (Previous, Play/Pause, Next)
   - Play count increments automatically on each play

3. **Favorites:**
   - Songs automatically become favorites after 3+ plays
   - View favorites in the "Favorites" section

4. **Search:**
   - Use the search bar in the Discover page to find songs

5. **Save/Load:**
   - Playlist data (play counts, favorites) is automatically saved
   - Data persists in `python_app/playlist_data.csv`

## Cover Images

- Place cover images in `/python_app/assets/` directory
- Name them as `<song_basename>.jpg` or `<song_basename>.png`
- If not found, the app uses `assets/default.jpg`

## Testing

### C Unit Tests

```bash
cd c_code
gcc -o test_playlist test_playlist_c.c playlist.c
./test_playlist
```

### Python Integration Tests

```bash
cd python_app
pytest tests/test_python.py -v
```

## Data Structure Details

The playlist is implemented as a **circular doubly linked list** in C:

- **Node Structure:**
  - `songName[256]`: Song title (basename)
  - `playCount`: Number of times played
  - `isFavorite`: Boolean flag (1 if favorite, 0 otherwise)
  - `next`: Pointer to next node
  - `prev`: Pointer to previous node

- **Key Operations:**
  - `addSong()`: O(1) - Insertion at tail with tail pointer
  - `deleteSong()`: O(n) - Search and delete by name
  - `playNext()` / `playPrevious()`: O(1) - Move current pointer
  - `displayPlaylist()`: O(n) - Traverse entire list
  - `searchSong()`: O(n) - Linear search

See `DS_REPORT.md` for detailed complexity analysis and implementation notes.

## Troubleshooting

1. **Library not found:**
   - Ensure the shared library (`.so`, `.dll`, or `.dylib`) is built in `c_code/` directory
   - Check that the library file has correct permissions

2. **Songs not loading:**
   - Verify audio files are in the `/songs` directory
   - Check file extensions are supported (`.mp3`, `.wav`, `.ogg`, etc.)

3. **Audio not playing:**
   - Ensure audio files are valid and not corrupted
   - Check browser supports HTML5 audio

4. **Memory issues:**
   - The C library properly manages memory, but ensure Python wrapper calls `freeString()` and `freeStringArray()`

## Requirements

- **C Compiler:** GCC (MinGW on Windows)
- **Python:** 3.8 or higher
- **Streamlit:** Latest version
- **Operating System:** Linux, Windows, or macOS

## License

This project is for educational purposes (Data Structures course project).

## Author

Created as a Data Structures project demonstrating:
- Circular doubly linked list implementation
- C/Python interop via ctypes
- Modern web UI with Streamlit
- Complete software development lifecycle

