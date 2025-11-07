"""
Python ctypes wrapper for the C playlist library.
Handles loading the shared library and provides a Python-friendly API.
"""

import ctypes
import os
import sys
import platform

class PlaylistBackend:
    """Wrapper class for the C playlist library."""
    
    def __init__(self):
        self.lib = None
        self._setup_functions()
    
    def load_library(self, lib_path=None):
        """
        Load the shared library. Auto-detects .so, .dll, or .dylib.
        
        Args:
            lib_path: Optional path to library. If None, searches in common locations.
        
        Returns:
            True if loaded successfully, False otherwise.
        """
        if lib_path and os.path.exists(lib_path):
            try:
                self.lib = ctypes.CDLL(lib_path)
                self._setup_functions()
                return True
            except Exception as e:
                print(f"Error loading library from {lib_path}: {e}")
                return False
        
        # Auto-detect library
        system = platform.system()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(base_dir)
        c_code_dir = os.path.join(parent_dir, "c_code")
        
        if system == "Windows":
            lib_names = ["playlist.dll", "libplaylist.dll"]
        elif system == "Darwin":
            lib_names = ["playlist.dylib", "libplaylist.dylib"]
        else:
            lib_names = ["playlist.so", "libplaylist.so"]
        
        for lib_name in lib_names:
            # Try in c_code directory
            lib_path = os.path.join(c_code_dir, lib_name)
            if os.path.exists(lib_path):
                try:
                    self.lib = ctypes.CDLL(lib_path)
                    self._setup_functions()
                    return True
                except Exception as e:
                    print(f"Error loading {lib_path}: {e}")
            
            # Try in current directory
            if os.path.exists(lib_name):
                try:
                    self.lib = ctypes.CDLL(lib_name)
                    self._setup_functions()
                    return True
                except Exception as e:
                    print(f"Error loading {lib_name}: {e}")
        
        print("Error: Could not find playlist library. Please build it first.")
        return False
    
    def _setup_functions(self):
        """Setup ctypes function signatures."""
        if not self.lib:
            return
        
        # initializePlaylist
        self.lib.initializePlaylist.argtypes = []
        self.lib.initializePlaylist.restype = None
        
        # addSong
        self.lib.addSong.argtypes = [ctypes.c_char_p]
        self.lib.addSong.restype = ctypes.c_int
        
        # deleteSong
        self.lib.deleteSong.argtypes = [ctypes.c_char_p]
        self.lib.deleteSong.restype = ctypes.c_int
        
        # playSong
        self.lib.playSong.argtypes = [ctypes.c_char_p]
        self.lib.playSong.restype = ctypes.POINTER(ctypes.c_char)
        
        # playNext
        self.lib.playNext.argtypes = []
        self.lib.playNext.restype = ctypes.POINTER(ctypes.c_char)
        
        # playPrevious
        self.lib.playPrevious.argtypes = []
        self.lib.playPrevious.restype = ctypes.POINTER(ctypes.c_char)
        
        # searchSong
        self.lib.searchSong.argtypes = [ctypes.c_char_p]
        self.lib.searchSong.restype = ctypes.POINTER(ctypes.c_char)
        
        # displayPlaylist
        self.lib.displayPlaylist.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.lib.displayPlaylist.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
        
        # displayFavorites
        self.lib.displayFavorites.argtypes = [ctypes.POINTER(ctypes.c_int)]
        self.lib.displayFavorites.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_char))
        
        # savePlaylistToFile
        self.lib.savePlaylistToFile.argtypes = [ctypes.c_char_p]
        self.lib.savePlaylistToFile.restype = None
        
        # loadPlaylistFromFile
        self.lib.loadPlaylistFromFile.argtypes = [ctypes.c_char_p]
        self.lib.loadPlaylistFromFile.restype = None
        
        # cleanupPlaylist
        self.lib.cleanupPlaylist.argtypes = []
        self.lib.cleanupPlaylist.restype = None
        
        # freeStringArray
        self.lib.freeStringArray.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_char)), ctypes.c_int]
        self.lib.freeStringArray.restype = None
        
        # freeString
        self.lib.freeString.argtypes = [ctypes.POINTER(ctypes.c_char)]
        self.lib.freeString.restype = None
    
    def _cstring_to_python(self, c_string_ptr):
        """Convert C string pointer to Python string and free C memory."""
        if not c_string_ptr:
            return None
        
        try:
            result = ctypes.string_at(c_string_ptr).decode('utf-8')
            self.lib.freeString(c_string_ptr)
            return result
        except Exception as e:
            print(f"Error converting C string: {e}")
            if c_string_ptr:
                self.lib.freeString(c_string_ptr)
            return None
    
    def initialize(self):
        """Initialize the playlist."""
        if not self.lib:
            raise RuntimeError("Library not loaded")
        self.lib.initializePlaylist()
    
    def add_song(self, filepath):
        """
        Add a song to the playlist.
        
        Args:
            filepath: Full path to the song file.
        
        Returns:
            True if successful, False otherwise.
        """
        if not self.lib:
            raise RuntimeError("Library not loaded")
        
        filepath_bytes = filepath.encode('utf-8')
        result = self.lib.addSong(filepath_bytes)
        return result == 1
    
    def delete_song(self, title):
        """
        Delete a song from the playlist.
        
        Args:
            title: Song title (basename).
        
        Returns:
            True if successful, False otherwise.
        """
        if not self.lib:
            raise RuntimeError("Library not loaded")
        
        title_bytes = title.encode('utf-8')
        result = self.lib.deleteSong(title_bytes)
        return result == 1
    
    def play_song(self, title):
        """
        Play a song (increments play count, marks favorite if >= 3).
        
        Args:
            title: Song title.
        
        Returns:
            Song title string, or None if not found.
        """
        if not self.lib:
            raise RuntimeError("Library not loaded")
        
        title_bytes = title.encode('utf-8')
        result_ptr = self.lib.playSong(title_bytes)
        return self._cstring_to_python(result_ptr)
    
    def play_next(self):
        """
        Play the next song in the playlist.
        
        Returns:
            Song title string, or None if playlist is empty.
        """
        if not self.lib:
            raise RuntimeError("Library not loaded")
        
        result_ptr = self.lib.playNext()
        return self._cstring_to_python(result_ptr)
    
    def play_previous(self):
        """
        Play the previous song in the playlist.
        
        Returns:
            Song title string, or None if playlist is empty.
        """
        if not self.lib:
            raise RuntimeError("Library not loaded")
        
        result_ptr = self.lib.playPrevious()
        return self._cstring_to_python(result_ptr)
    
    def search_song(self, title):
        """
        Search for a song and return info string.
        
        Args:
            title: Song title to search for.
        
        Returns:
            Info string like "Title (Plays: X, Favorite: Yes/No)", or None if not found.
        """
        if not self.lib:
            raise RuntimeError("Library not loaded")
        
        title_bytes = title.encode('utf-8')
        result_ptr = self.lib.searchSong(title_bytes)
        return self._cstring_to_python(result_ptr)
    
    def get_playlist(self):
        """
        Get all songs in the playlist.
        
        Returns:
            List of song titles.
        """
        if not self.lib:
            raise RuntimeError("Library not loaded")
        
        count = ctypes.c_int(0)
        result_ptr = self.lib.displayPlaylist(ctypes.byref(count))
        
        if not result_ptr or count.value == 0:
            return []
        
        songs = []
        for i in range(count.value):
            if result_ptr[i]:
                song = ctypes.string_at(result_ptr[i]).decode('utf-8')
                songs.append(song)
        
        # Free the array
        self.lib.freeStringArray(result_ptr, count.value)
        
        return songs
    
    def get_favorites(self):
        """
        Get all favorite songs.
        
        Returns:
            List of favorite song titles.
        """
        if not self.lib:
            raise RuntimeError("Library not loaded")
        
        count = ctypes.c_int(0)
        result_ptr = self.lib.displayFavorites(ctypes.byref(count))
        
        if not result_ptr or count.value == 0:
            return []
        
        favorites = []
        for i in range(count.value):
            if result_ptr[i]:
                song = ctypes.string_at(result_ptr[i]).decode('utf-8')
                favorites.append(song)
        
        # Free the array
        self.lib.freeStringArray(result_ptr, count.value)
        
        return favorites
    
    def save(self, filename):
        """
        Save playlist to file.
        
        Args:
            filename: Path to save file.
        """
        if not self.lib:
            raise RuntimeError("Library not loaded")
        
        filename_bytes = filename.encode('utf-8')
        self.lib.savePlaylistToFile(filename_bytes)
    
    def load(self, filename):
        """
        Load playlist from file.
        
        Args:
            filename: Path to load file from.
        """
        if not self.lib:
            raise RuntimeError("Library not loaded")
        
        filename_bytes = filename.encode('utf-8')
        self.lib.loadPlaylistFromFile(filename_bytes)
    
    def cleanup(self):
        """Cleanup and free all memory."""
        if not self.lib:
            return
        self.lib.cleanupPlaylist()

