#ifndef PLAYLIST_H
#define PLAYLIST_H

#ifdef __cplusplus
extern "C" {
#endif

// Node structure for circular doubly linked list
typedef struct Node {
    char songName[256];   // safe fixed-length
    int playCount;
    int isFavorite;       // 0 or 1
    struct Node* next;
    struct Node* prev;
} Node;

// Exported functions
void initializePlaylist();
int addSong(const char* filepath);
int deleteSong(const char* songName);
char* playSong(const char* songName);
char* playNext();
char* playPrevious();
char* searchSong(const char* songName);
char** displayPlaylist(int* outCount);
char** displayFavorites(int* outCount);
void savePlaylistToFile(const char* filename);
void loadPlaylistFromFile(const char* filename);
void cleanupPlaylist();
void freeStringArray(char** array, int count);
void freeString(char* s);

#ifdef __cplusplus
}
#endif

#endif // PLAYLIST_H

