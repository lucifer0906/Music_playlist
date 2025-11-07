#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include "playlist.h"

// Global pointers for circular doubly linked list
static Node* head = NULL;
static Node* tail = NULL;
static Node* current = NULL;
static int listSize = 0;

// Helper function to extract basename from filepath
static void extractBasename(const char* filepath, char* basename) {
    const char* lastSlash = strrchr(filepath, '/');
    const char* lastBackslash = strrchr(filepath, '\\');
    const char* start = (lastSlash > lastBackslash) ? lastSlash + 1 : 
                        (lastBackslash ? lastBackslash + 1 : filepath);
    
    const char* lastDot = strrchr(start, '.');
    size_t len = lastDot ? (size_t)(lastDot - start) : strlen(start);
    
    if (len >= 256) len = 255;
    strncpy(basename, start, len);
    basename[len] = '\0';
}

// Initialize the playlist
void initializePlaylist() {
    cleanupPlaylist();
    head = NULL;
    tail = NULL;
    current = NULL;
    listSize = 0;
}

// Add a song to the playlist (insertion at tail - O(1))
int addSong(const char* filepath) {
    if (!filepath || strlen(filepath) == 0) {
        return 0;
    }
    
    char basename[256];
    extractBasename(filepath, basename);
    
    // Check if song already exists
    Node* temp = head;
    if (temp) {
        do {
            if (strcmp(temp->songName, basename) == 0) {
                return 0; // Song already exists
            }
            temp = temp->next;
        } while (temp != head);
    }
    
    // Create new node
    Node* newNode = (Node*)malloc(sizeof(Node));
    if (!newNode) {
        return 0;
    }
    
    strncpy(newNode->songName, basename, 255);
    newNode->songName[255] = '\0';
    newNode->playCount = 0;
    newNode->isFavorite = 0;
    
    // Insert at tail (O(1) with tail pointer)
    if (head == NULL) {
        // First node - circular list with single node
        head = newNode;
        tail = newNode;
        newNode->next = newNode;
        newNode->prev = newNode;
        current = newNode;
    } else {
        // Insert at tail
        newNode->next = head;
        newNode->prev = tail;
        tail->next = newNode;
        head->prev = newNode;
        tail = newNode;
    }
    
    listSize++;
    return 1;
}

// Delete a song by name (O(n) - must search)
int deleteSong(const char* songName) {
    if (!songName || !head) {
        return 0;
    }
    
    Node* temp = head;
    do {
        if (strcmp(temp->songName, songName) == 0) {
            // Found the node to delete
            if (listSize == 1) {
                // Only one node
                free(head);
                head = NULL;
                tail = NULL;
                current = NULL;
            } else {
                // Update pointers
                temp->prev->next = temp->next;
                temp->next->prev = temp->prev;
                
                if (temp == head) {
                    head = temp->next;
                }
                if (temp == tail) {
                    tail = temp->prev;
                }
                if (temp == current) {
                    current = temp->next;
                }
                
                free(temp);
            }
            listSize--;
            return 1;
        }
        temp = temp->next;
    } while (temp != head);
    
    return 0; // Song not found
}

// Play a song (increment count, mark favorite if >= 3)
char* playSong(const char* songName) {
    if (!songName || !head) {
        return NULL;
    }
    
    Node* temp = head;
    do {
        if (strcmp(temp->songName, songName) == 0) {
            current = temp;
            temp->playCount++;
            if (temp->playCount >= 3) {
                temp->isFavorite = 1;
            }
            
            // Return malloc'd string
            char* result = (char*)malloc(256);
            if (result) {
                strncpy(result, temp->songName, 255);
                result[255] = '\0';
            }
            return result;
        }
        temp = temp->next;
    } while (temp != head);
    
    return NULL; // Song not found
}

// Play next song (O(1) - just move pointer)
char* playNext() {
    if (!current) {
        return NULL;
    }
    
    current = current->next;
    current->playCount++;
    if (current->playCount >= 3) {
        current->isFavorite = 1;
    }
    
    char* result = (char*)malloc(256);
    if (result) {
        strncpy(result, current->songName, 255);
        result[255] = '\0';
    }
    return result;
}

// Play previous song (O(1) - just move pointer)
char* playPrevious() {
    if (!current) {
        return NULL;
    }
    
    current = current->prev;
    current->playCount++;
    if (current->playCount >= 3) {
        current->isFavorite = 1;
    }
    
    char* result = (char*)malloc(256);
    if (result) {
        strncpy(result, current->songName, 255);
        result[255] = '\0';
    }
    return result;
}

// Search for a song and return info string
char* searchSong(const char* songName) {
    if (!songName || !head) {
        return NULL;
    }
    
    Node* temp = head;
    do {
        if (strcmp(temp->songName, songName) == 0) {
            // Format: "Title (Plays: X, Favorite: Yes/No)"
            char* result = (char*)malloc(512);
            if (result) {
                snprintf(result, 511, "%s (Plays: %d, Favorite: %s)", 
                        temp->songName, temp->playCount,
                        temp->isFavorite ? "Yes" : "No");
                result[511] = '\0';
            }
            return result;
        }
        temp = temp->next;
    } while (temp != head);
    
    return NULL; // Song not found
}

// Display entire playlist (returns array of strings)
char** displayPlaylist(int* outCount) {
    *outCount = 0;
    if (!head) {
        return NULL;
    }
    
    char** result = (char**)malloc(listSize * sizeof(char*));
    if (!result) {
        return NULL;
    }
    
    Node* temp = head;
    int index = 0;
    do {
        result[index] = (char*)malloc(256);
        if (result[index]) {
            strncpy(result[index], temp->songName, 255);
            result[index][255] = '\0';
        }
        index++;
        temp = temp->next;
    } while (temp != head);
    
    *outCount = listSize;
    return result;
}

// Display favorites only
char** displayFavorites(int* outCount) {
    *outCount = 0;
    if (!head) {
        return NULL;
    }
    
    // First pass: count favorites
    int favCount = 0;
    Node* temp = head;
    do {
        if (temp->isFavorite) {
            favCount++;
        }
        temp = temp->next;
    } while (temp != head);
    
    if (favCount == 0) {
        return NULL;
    }
    
    // Second pass: allocate and fill
    char** result = (char**)malloc(favCount * sizeof(char*));
    if (!result) {
        return NULL;
    }
    
    temp = head;
    int index = 0;
    do {
        if (temp->isFavorite) {
            result[index] = (char*)malloc(256);
            if (result[index]) {
                strncpy(result[index], temp->songName, 255);
                result[index][255] = '\0';
            }
            index++;
        }
        temp = temp->next;
    } while (temp != head);
    
    *outCount = favCount;
    return result;
}

// Save playlist to file (CSV format)
void savePlaylistToFile(const char* filename) {
    if (!filename || !head) {
        return;
    }
    
    FILE* file = fopen(filename, "w");
    if (!file) {
        return;
    }
    
    Node* temp = head;
    do {
        fprintf(file, "%s,%d,%d\n", temp->songName, temp->playCount, temp->isFavorite);
        temp = temp->next;
    } while (temp != head);
    
    fclose(file);
}

// Load playlist from file
void loadPlaylistFromFile(const char* filename) {
    if (!filename) {
        return;
    }
    
    FILE* file = fopen(filename, "r");
    if (!file) {
        return;
    }
    
    char line[512];
    while (fgets(line, sizeof(line), file)) {
        // Parse CSV: song,playcount,isfavorite
        char songName[256];
        int playCount = 0;
        int isFavorite = 0;
        
        if (sscanf(line, "%255[^,],%d,%d", songName, &playCount, &isFavorite) == 3) {
            // Add song if not exists
            Node* temp = head;
            int exists = 0;
            if (temp) {
                do {
                    if (strcmp(temp->songName, songName) == 0) {
                        exists = 1;
                        temp->playCount = playCount;
                        temp->isFavorite = isFavorite;
                        break;
                    }
                    temp = temp->next;
                } while (temp != head);
            }
            
            if (!exists) {
                // Create node directly with data
                Node* newNode = (Node*)malloc(sizeof(Node));
                if (newNode) {
                    strncpy(newNode->songName, songName, 255);
                    newNode->songName[255] = '\0';
                    newNode->playCount = playCount;
                    newNode->isFavorite = isFavorite;
                    
                    if (head == NULL) {
                        head = newNode;
                        tail = newNode;
                        newNode->next = newNode;
                        newNode->prev = newNode;
                        current = newNode;
                    } else {
                        newNode->next = head;
                        newNode->prev = tail;
                        tail->next = newNode;
                        head->prev = newNode;
                        tail = newNode;
                    }
                    listSize++;
                }
            }
        }
    }
    
    fclose(file);
}

// Cleanup and free all memory
void cleanupPlaylist() {
    if (!head) {
        return;
    }
    
    Node* temp = head;
    Node* next;
    do {
        next = temp->next;
        free(temp);
        temp = next;
    } while (temp != head);
    
    head = NULL;
    tail = NULL;
    current = NULL;
    listSize = 0;
}

// Free array of strings
void freeStringArray(char** array, int count) {
    if (!array) {
        return;
    }
    
    for (int i = 0; i < count; i++) {
        if (array[i]) {
            free(array[i]);
        }
    }
    free(array);
}

// Free a single string
void freeString(char* s) {
    if (s) {
        free(s);
    }
}

