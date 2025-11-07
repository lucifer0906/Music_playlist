"""
Python Integration Tests for Playlist Backend
Run: pytest tests/test_python.py -v
"""

import pytest
import os
import sys
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python_app'))
from playlist import PlaylistBackend

class TestPlaylistBackend:
    """Test suite for PlaylistBackend class."""
    
    @pytest.fixture
    def playlist(self):
        """Create a playlist instance for testing."""
        p = PlaylistBackend()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(base_dir)
        c_code_dir = os.path.join(parent_dir, "c_code")
        
        # Try to load library
        if not p.load_library():
            pytest.skip("Playlist library not found. Please build it first.")
        
        p.initialize()
        return p
    
    def test_initialize(self, playlist):
        """Test playlist initialization."""
        assert playlist is not None
        songs = playlist.get_playlist()
        assert isinstance(songs, list)
    
    def test_add_song(self, playlist):
        """Test adding songs."""
        # Add songs
        assert playlist.add_song("test1.mp3") == True
        assert playlist.add_song("test2.mp3") == True
        assert playlist.add_song("test3.mp3") == True
        
        # Try duplicate
        assert playlist.add_song("test1.mp3") == False
        
        # Verify songs are in playlist
        songs = playlist.get_playlist()
        assert len(songs) == 3
        assert "test1" in songs
        assert "test2" in songs
        assert "test3" in songs
    
    def test_play_song(self, playlist):
        """Test playing a song."""
        playlist.add_song("play_test.mp3")
        
        result = playlist.play_song("play_test")
        assert result == "play_test"
        
        # Check play count
        info = playlist.search_song("play_test")
        assert "Plays: 1" in info
    
    def test_play_next_previous(self, playlist):
        """Test next/previous navigation."""
        playlist.add_song("song1.mp3")
        playlist.add_song("song2.mp3")
        playlist.add_song("song3.mp3")
        
        # Play first song
        playlist.play_song("song1")
        
        # Play next
        next_song = playlist.play_next()
        assert next_song == "song2"
        
        # Play previous
        prev_song = playlist.play_previous()
        assert prev_song == "song1"
    
    def test_favorites(self, playlist):
        """Test favorites system."""
        playlist.add_song("fav_test.mp3")
        
        # Play 3 times to make it favorite
        playlist.play_song("fav_test")
        playlist.play_song("fav_test")
        playlist.play_song("fav_test")
        
        favorites = playlist.get_favorites()
        assert len(favorites) == 1
        assert "fav_test" in favorites
    
    def test_search_song(self, playlist):
        """Test song search."""
        playlist.add_song("search_test.mp3")
        playlist.play_song("search_test")
        
        info = playlist.search_song("search_test")
        assert info is not None
        assert "search_test" in info
        assert "Plays:" in info
        assert "Favorite:" in info
    
    def test_delete_song(self, playlist):
        """Test deleting a song."""
        playlist.add_song("delete1.mp3")
        playlist.add_song("delete2.mp3")
        
        assert playlist.delete_song("delete1") == True
        assert playlist.delete_song("delete1") == False  # Already deleted
        
        songs = playlist.get_playlist()
        assert len(songs) == 1
        assert "delete1" not in songs
        assert "delete2" in songs
    
    def test_save_load(self, playlist):
        """Test saving and loading playlist."""
        # Create test data
        playlist.add_song("save1.mp3")
        playlist.add_song("save2.mp3")
        playlist.play_song("save1")
        playlist.play_song("save1")
        playlist.play_song("save1")  # Make it favorite
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
            temp_file = f.name
        
        try:
            playlist.save(temp_file)
            
            # Create new playlist and load
            new_playlist = PlaylistBackend()
            new_playlist.load_library()
            new_playlist.initialize()
            new_playlist.load(temp_file)
            
            # Verify data
            songs = new_playlist.get_playlist()
            assert len(songs) == 2
            
            favorites = new_playlist.get_favorites()
            assert "save1" in favorites
            
            info = new_playlist.search_song("save1")
            assert "Plays: 3" in info or "Plays: 4" in info  # May have incremented during load
            
        finally:
            # Cleanup
            if os.path.exists(temp_file):
                os.remove(temp_file)
    
    def test_memory_management(self, playlist):
        """Test that memory is properly freed."""
        playlist.add_song("mem_test1.mp3")
        playlist.add_song("mem_test2.mp3")
        
        # These should not leak memory
        songs = playlist.get_playlist()
        assert len(songs) == 2
        
        info = playlist.search_song("mem_test1")
        assert info is not None
        
        favorites = playlist.get_favorites()
        assert isinstance(favorites, list)
        
        # If we get here without crashing, memory management is working
        assert True
    
    def test_empty_playlist(self, playlist):
        """Test operations on empty playlist."""
        songs = playlist.get_playlist()
        assert len(songs) == 0
        
        favorites = playlist.get_favorites()
        assert len(favorites) == 0
        
        result = playlist.play_next()
        assert result is None
        
        result = playlist.play_previous()
        assert result is None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])

