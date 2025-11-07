/*
 * C Unit Tests for Playlist Library
 * Compile: gcc -o test_playlist test_playlist_c.c playlist.c
 * Run: ./test_playlist
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include "../c_code/playlist.h"

void test_initialize() {
    printf("Testing initializePlaylist()...\n");
    initializePlaylist();
    printf("✓ Passed\n\n");
}

void test_add_song() {
    printf("Testing addSong()...\n");
    initializePlaylist();
    
    assert(addSong("test1.mp3") == 1);
    assert(addSong("test2.mp3") == 1);
    assert(addSong("test3.mp3") == 1);
    
    // Test duplicate
    assert(addSong("test1.mp3") == 0);
    
    printf("✓ Passed\n\n");
}

void test_display_playlist() {
    printf("Testing displayPlaylist()...\n");
    initializePlaylist();
    
    addSong("song1.mp3");
    addSong("song2.mp3");
    addSong("song3.mp3");
    
    int count = 0;
    char** songs = displayPlaylist(&count);
    
    assert(count == 3);
    assert(strcmp(songs[0], "song1") == 0);
    assert(strcmp(songs[1], "song2") == 0);
    assert(strcmp(songs[2], "song3") == 0);
    
    freeStringArray(songs, count);
    printf("✓ Passed\n\n");
}

void test_play_song() {
    printf("Testing playSong()...\n");
    initializePlaylist();
    
    addSong("test.mp3");
    
    char* result = playSong("test");
    assert(result != NULL);
    assert(strcmp(result, "test") == 0);
    freeString(result);
    
    // Test search to verify play count
    char* info = searchSong("test");
    assert(info != NULL);
    assert(strstr(info, "Plays: 1") != NULL);
    freeString(info);
    
    printf("✓ Passed\n\n");
}

void test_play_next_previous() {
    printf("Testing playNext() and playPrevious()...\n");
    initializePlaylist();
    
    addSong("song1.mp3");
    addSong("song2.mp3");
    addSong("song3.mp3");
    
    // Play first song
    char* result = playSong("song1");
    freeString(result);
    
    // Play next
    result = playNext();
    assert(result != NULL);
    assert(strcmp(result, "song2") == 0);
    freeString(result);
    
    // Play previous
    result = playPrevious();
    assert(result != NULL);
    assert(strcmp(result, "song1") == 0);
    freeString(result);
    
    printf("✓ Passed\n\n");
}

void test_favorites() {
    printf("Testing favorites system...\n");
    initializePlaylist();
    
    addSong("fav_test.mp3");
    
    // Play 3 times to make it favorite
    playSong("fav_test");
    playSong("fav_test");
    playSong("fav_test");
    
    int count = 0;
    char** favorites = displayFavorites(&count);
    
    assert(count == 1);
    assert(strcmp(favorites[0], "fav_test") == 0);
    
    freeStringArray(favorites, count);
    printf("✓ Passed\n\n");
}

void test_delete_song() {
    printf("Testing deleteSong()...\n");
    initializePlaylist();
    
    addSong("delete1.mp3");
    addSong("delete2.mp3");
    addSong("delete3.mp3");
    
    assert(deleteSong("delete2") == 1);
    assert(deleteSong("delete2") == 0); // Already deleted
    
    int count = 0;
    char** songs = displayPlaylist(&count);
    assert(count == 2);
    freeStringArray(songs, count);
    
    printf("✓ Passed\n\n");
}

void test_save_load() {
    printf("Testing savePlaylistToFile() and loadPlaylistFromFile()...\n");
    initializePlaylist();
    
    addSong("save1.mp3");
    addSong("save2.mp3");
    playSong("save1");
    playSong("save1");
    playSong("save1"); // Make it favorite
    
    savePlaylistToFile("test_playlist.csv");
    
    // Clear and reload
    cleanupPlaylist();
    initializePlaylist();
    loadPlaylistFromFile("test_playlist.csv");
    
    int count = 0;
    char** songs = displayPlaylist(&count);
    assert(count == 2);
    
    char* info = searchSong("save1");
    assert(strstr(info, "Favorite: Yes") != NULL);
    freeString(info);
    
    freeStringArray(songs, count);
    
    // Cleanup
    remove("test_playlist.csv");
    
    printf("✓ Passed\n\n");
}

int main() {
    printf("Running C Unit Tests for Playlist Library\n");
    printf("==========================================\n\n");
    
    test_initialize();
    test_add_song();
    test_display_playlist();
    test_play_song();
    test_play_next_previous();
    test_favorites();
    test_delete_song();
    test_save_load();
    
    cleanupPlaylist();
    
    printf("==========================================\n");
    printf("All tests passed! ✓\n");
    
    return 0;
}

