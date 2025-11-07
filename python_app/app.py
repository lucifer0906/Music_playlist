"""
Spotify-style Music Playlist Dashboard
Streamlit frontend for the C playlist backend
"""

import streamlit as st
import os
import sys
from pathlib import Path
from PIL import Image
import base64
import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from playlist import PlaylistBackend

# Page configuration
st.set_page_config(
    page_title="Musfluent - Music Player",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    if os.path.exists(css_path):
        with open(css_path, "r") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Initialize session state
if 'playlist' not in st.session_state:
    st.session_state.playlist = None
if 'current_song' not in st.session_state:
    st.session_state.current_song = None
if 'current_song_path' not in st.session_state:
    st.session_state.current_song_path = None
if 'is_playing' not in st.session_state:
    st.session_state.is_playing = False
if 'playlist_initialized' not in st.session_state:
    st.session_state.playlist_initialized = False
if 'songs_data' not in st.session_state:
    st.session_state.songs_data = {}  # Store play counts and favorites

# Initialize playlist backend
def init_playlist():
    if st.session_state.playlist is None:
        playlist = PlaylistBackend()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(base_dir)
        c_code_dir = os.path.join(parent_dir, "c_code")
        
        # Try to load library
        if playlist.load_library():
            playlist.initialize()
            st.session_state.playlist = playlist
            return True
        else:
            st.error("Failed to load playlist library. Please build it first.")
            return False
    return True

# Get song file path
def get_song_path(song_name):
    """Find the actual file path for a song name."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)
    
    # Try both "songs" and "Songs" (case-insensitive)
    songs_dirs = [
        os.path.join(parent_dir, "songs"),
        os.path.join(parent_dir, "Songs"),
    ]
    
    # Try common extensions
    extensions = ['.mp3', '.wav', '.ogg', '.m4a', '.flac']
    
    for songs_dir in songs_dirs:
        if not os.path.exists(songs_dir):
            continue
            
        # Try with extensions
        for ext in extensions:
            filepath = os.path.join(songs_dir, song_name + ext)
            if os.path.exists(filepath):
                return filepath
        
        # Try exact match (song_name might already have extension)
        filepath = os.path.join(songs_dir, song_name)
        if os.path.exists(filepath):
            return filepath
        
        # Try case-insensitive match
        for filename in os.listdir(songs_dir):
            if os.path.splitext(filename)[0].lower() == song_name.lower():
                return os.path.join(songs_dir, filename)
    
    return None

# Get cover image
def get_cover_image(song_name):
    """Get cover image for a song."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")
    
    # Try to find cover image
    base_name = os.path.splitext(song_name)[0]
    for ext in ['.jpg', '.jpeg', '.png']:
        cover_path = os.path.join(assets_dir, base_name + ext)
        if os.path.exists(cover_path):
            return cover_path
    
    # Use default
    default_path = os.path.join(assets_dir, "default.jpg")
    if os.path.exists(default_path):
        return default_path
    
    return None

# Get base64 encoded image
def get_image_base64(image_path):
    """Get base64 encoded image for HTML display."""
    if image_path and os.path.exists(image_path):
        try:
            with open(image_path, 'rb') as f:
                return base64.b64encode(f.read()).decode()
        except:
            return None
    return None

# Load songs from directory
def load_songs_from_directory():
    """Scan songs directory and add to playlist."""
    if not st.session_state.playlist:
        return
    
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(base_dir)
    
    # Try both "songs" and "Songs" directories
    songs_dirs = [
        os.path.join(parent_dir, "songs"),
        os.path.join(parent_dir, "Songs"),
    ]
    
    # Supported audio formats
    audio_extensions = ['.mp3', '.wav', '.ogg', '.m4a', '.flac']
    
    for songs_dir in songs_dirs:
        if not os.path.exists(songs_dir):
            continue
        
        for filename in os.listdir(songs_dir):
            filepath = os.path.join(songs_dir, filename)
            if os.path.isfile(filepath):
                ext = os.path.splitext(filename)[1].lower()
                if ext in audio_extensions:
                    try:
                        st.session_state.playlist.add_song(filepath)
                    except Exception as e:
                        pass  # Silently skip duplicates or errors

# Update songs data (play counts, favorites)
def update_songs_data():
    """Update session state with current play counts and favorites."""
    if not st.session_state.playlist:
        return
    
    try:
        all_songs = st.session_state.playlist.get_playlist()
        favorites = st.session_state.playlist.get_favorites()
        fav_set = set(favorites)
        
        for song in all_songs:
            search_result = st.session_state.playlist.search_song(song)
            if search_result:
                # Parse: "Title (Plays: X, Favorite: Yes/No)"
                parts = search_result.split("(Plays: ")
                if len(parts) == 2:
                    play_part = parts[1].split(",")[0]
                    try:
                        play_count = int(play_part.strip())
                    except:
                        play_count = 0
                else:
                    play_count = 0
                
                is_favorite = song in fav_set
                st.session_state.songs_data[song] = {
                    'play_count': play_count,
                    'is_favorite': is_favorite
                }
    except Exception as e:
        st.error(f"Error updating songs data: {e}")

# Initialize on first run
if not st.session_state.playlist_initialized:
    if init_playlist():
        # Try to load saved playlist
        base_dir = os.path.dirname(os.path.abspath(__file__))
        playlist_file = os.path.join(base_dir, "playlist_data.csv")
        if os.path.exists(playlist_file):
            try:
                st.session_state.playlist.load(playlist_file)
            except:
                pass
        
        # Load songs from directory
        load_songs_from_directory()
        update_songs_data()
        st.session_state.playlist_initialized = True

# Sidebar
with st.sidebar:
    st.markdown("""
    <div class="logo-container">
        <div class="logo-icon">🎵</div>
        <div class="logo-text">musfluent</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Navigation
    page = st.radio(
        "Navigation",
        ["Discover", "Playlist", "Favorites", "Stats", "Upload"],
        label_visibility="collapsed",
        key="nav"
    )
    
    st.markdown("---")
    
    # My Library section
    st.markdown("""
    <div class="library-section">
        <div class="library-header">
            <span class="library-title">My Library</span>
            <span style="color: #1DB954; cursor: pointer;">+</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Main content area
if page == "Discover":
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
        <h1 style="color: #ffffff; font-size: 32px; font-weight: 700;">Discover</h1>
        <div style="flex: 1; max-width: 400px; margin-left: 2rem;">
            <input type="text" placeholder="Search anything here..." class="search-input" id="search-input">
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Search functionality
    search_query = st.text_input("", placeholder="Search anything here...", key="search", label_visibility="collapsed")
    
    # Hero/Now Playing Card
    if st.session_state.current_song:
        song_name = st.session_state.current_song
        cover_path = get_cover_image(song_name)
        cover_b64 = get_image_base64(cover_path) if cover_path else None
        
        if cover_b64:
            st.markdown(f"""
            <div class="hero-card">
                <img src="data:image/jpeg;base64,{cover_b64}" 
                     class="hero-cover" alt="Cover">
                <div class="hero-info">
                    <div class="verified-badge">
                        <span>✓</span>
                        <span>Now Playing</span>
                    </div>
                    <h2 class="hero-title">{song_name}</h2>
                    <div class="hero-subtitle">
                        <span>🎵</span>
                        <span>Currently playing</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="hero-card">
                <div class="hero-info">
                    <div class="verified-badge">
                        <span>✓</span>
                        <span>Now Playing</span>
                    </div>
                    <h2 class="hero-title">{song_name}</h2>
                    <div class="hero-subtitle">
                        <span>🎵</span>
                        <span>Currently playing</span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Trendy Songs Section
    st.markdown("""
    <div class="section-header">
        <h2 class="section-title">Trendy Songs</h2>
        <div style="display: flex; gap: 0.5rem;">
            <button style="background: transparent; border: none; color: #b3b3b3; cursor: pointer;">&lt;</button>
            <button style="background: transparent; border: none; color: #b3b3b3; cursor: pointer;">&gt;</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display songs grid
    if st.session_state.playlist:
        all_songs = st.session_state.playlist.get_playlist()
        
        # Filter by search
        if search_query:
            all_songs = [s for s in all_songs if search_query.lower() in s.lower()]
        
        if all_songs:
            # Create columns for grid
            cols = st.columns(4)
            for idx, song in enumerate(all_songs[:12]):  # Show first 12
                col = cols[idx % 4]
                with col:
                    cover_path = get_cover_image(song)
                    play_count = st.session_state.songs_data.get(song, {}).get('play_count', 0)
                    is_favorite = st.session_state.songs_data.get(song, {}).get('is_favorite', False)
                    
                    # Display cover
                    if cover_path and os.path.exists(cover_path):
                        st.image(cover_path, use_container_width=True)
                    
                    st.markdown(f"""
                    <div class="song-card">
                        <h4 class="song-card-title">{song}</h4>
                        <p class="song-card-artist">Artist</p>
                        <div class="song-card-actions">
                            <button onclick="playSong('{song}')" class="song-card-icon play-button">▶</button>
                            <span class="play-count-badge">{play_count} plays</span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Play button
                    if st.button("▶ Play", key=f"play_{song}"):
                        try:
                            result = st.session_state.playlist.play_song(song)
                            if result:
                                st.session_state.current_song = result
                                st.session_state.current_song_path = get_song_path(result)
                                st.session_state.is_playing = True
                                update_songs_data()
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error playing song: {e}")
        else:
            st.info("No songs found. Upload some songs in the Upload section!")

elif page == "Playlist":
    st.title("My Playlist")
    
    if st.session_state.playlist:
        all_songs = st.session_state.playlist.get_playlist()
        
        if all_songs:
            for idx, song in enumerate(all_songs):
                col1, col2, col3, col4 = st.columns([1, 3, 2, 2])
                
                with col1:
                    cover_path = get_cover_image(song)
                    if cover_path and os.path.exists(cover_path):
                        st.image(cover_path, width=60)
                
                with col2:
                    st.markdown(f"**{song}**")
                    st.caption("Artist")
                
                with col3:
                    play_count = st.session_state.songs_data.get(song, {}).get('play_count', 0)
                    st.markdown(f"<span class='play-count-badge'>{play_count} plays</span>", unsafe_allow_html=True)
                
                with col4:
                    if st.button("Play", key=f"playlist_play_{idx}"):
                        try:
                            result = st.session_state.playlist.play_song(song)
                            if result:
                                st.session_state.current_song = result
                                st.session_state.current_song_path = get_song_path(result)
                                st.session_state.is_playing = True
                                update_songs_data()
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
        else:
            st.info("Your playlist is empty!")

elif page == "Favorites":
    st.title("Favorites")
    
    if st.session_state.playlist:
        favorites = st.session_state.playlist.get_favorites()
        
        if favorites:
            cols = st.columns(4)
            for idx, song in enumerate(favorites):
                col = cols[idx % 4]
                with col:
                    cover_path = get_cover_image(song)
                    if cover_path and os.path.exists(cover_path):
                        st.image(cover_path, use_container_width=True)
                    
                    st.markdown(f"**{song}**")
                    
                    if st.button("Play", key=f"fav_play_{idx}"):
                        try:
                            result = st.session_state.playlist.play_song(song)
                            if result:
                                st.session_state.current_song = result
                                st.session_state.current_song_path = get_song_path(result)
                                st.session_state.is_playing = True
                                update_songs_data()
                                st.rerun()
                        except Exception as e:
                            st.error(f"Error: {e}")
        else:
            st.info("No favorites yet! Play songs 3+ times to add them to favorites.")

elif page == "Stats":
    st.title("Statistics")
    
    if st.session_state.playlist:
        all_songs = st.session_state.playlist.get_playlist()
        favorites = st.session_state.playlist.get_favorites()
        total_plays = sum(st.session_state.songs_data.get(s, {}).get('play_count', 0) for s in all_songs)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{len(all_songs)}</div>
                <div class="stat-label">Total Songs</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{len(favorites)}</div>
                <div class="stat-label">Favorites</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-value">{total_plays}</div>
                <div class="stat-label">Total Plays</div>
            </div>
            """, unsafe_allow_html=True)

elif page == "Upload":
    st.title("Upload Song")
    
    uploaded_file = st.file_uploader("Choose an audio file", type=['mp3', 'wav', 'ogg', 'm4a', 'flac'])
    
    if uploaded_file is not None:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(base_dir)
        
        # Try to use existing Songs directory, otherwise create songs
        songs_dir = os.path.join(parent_dir, "Songs")
        if not os.path.exists(songs_dir):
            songs_dir = os.path.join(parent_dir, "songs")
        os.makedirs(songs_dir, exist_ok=True)
        
        filepath = os.path.join(songs_dir, uploaded_file.name)
        
        if st.button("Upload"):
            try:
                with open(filepath, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                if st.session_state.playlist:
                    if st.session_state.playlist.add_song(filepath):
                        st.success(f"Successfully uploaded {uploaded_file.name}!")
                        update_songs_data()
                        st.rerun()
                    else:
                        st.warning("Song already exists in playlist or failed to add.")
            except Exception as e:
                st.error(f"Error uploading file: {e}")

# Bottom Player Bar
if st.session_state.current_song and st.session_state.current_song_path:
    st.markdown("---")
    
    col1, col2, col3 = st.columns([2, 5, 2])
    
    with col1:
        cover_path = get_cover_image(st.session_state.current_song)
        if cover_path and os.path.exists(cover_path):
            st.image(cover_path, width=60)
        st.markdown(f"**{st.session_state.current_song}**")
    
    with col2:
        # Audio player
        try:
            with open(st.session_state.current_song_path, 'rb') as audio_file:
                audio_bytes = audio_file.read()
            st.audio(audio_bytes, format='audio/mp3', autoplay=st.session_state.is_playing)
        except Exception as e:
            st.error(f"Error loading audio: {e}")
        
        # Control buttons
        btn_col1, btn_col2, btn_col3, btn_col4, btn_col5 = st.columns(5)
        
        with btn_col1:
            if st.button("⏮"):
                try:
                    result = st.session_state.playlist.play_previous()
                    if result:
                        st.session_state.current_song = result
                        st.session_state.current_song_path = get_song_path(result)
                        update_songs_data()
                        st.rerun()
                except:
                    pass
        
        with btn_col2:
            if st.button("⏯" if st.session_state.is_playing else "▶"):
                st.session_state.is_playing = not st.session_state.is_playing
                st.rerun()
        
        with btn_col3:
            if st.button("⏭"):
                try:
                    result = st.session_state.playlist.play_next()
                    if result:
                        st.session_state.current_song = result
                        st.session_state.current_song_path = get_song_path(result)
                        update_songs_data()
                        st.rerun()
                except:
                    pass
    
    with col3:
        is_favorite = st.session_state.songs_data.get(st.session_state.current_song, {}).get('is_favorite', False)
        fav_icon = "❤️" if is_favorite else "🤍"
        if st.button(fav_icon):
            # Toggle favorite by playing again (or implement toggle function)
            pass

# Save playlist on exit
if st.session_state.playlist:
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        playlist_file = os.path.join(base_dir, "playlist_data.csv")
        st.session_state.playlist.save(playlist_file)
    except:
        pass

