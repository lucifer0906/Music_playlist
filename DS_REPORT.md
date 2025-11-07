# Data Structures Report: Circular Doubly Linked List Playlist

## 1. Data Structure Overview

### Node Structure

```c
typedef struct Node {
    char songName[256];   // Song title (basename, fixed-length for safety)
    int playCount;        // Number of times the song has been played
    int isFavorite;       // Boolean flag: 1 if favorite, 0 otherwise
    struct Node* next;    // Pointer to next node in the list
    struct Node* prev;    // Pointer to previous node in the list
} Node;
```

### Global Variables

- `head`: Pointer to the first node in the circular list
- `tail`: Pointer to the last node in the circular list
- `current`: Pointer to the currently playing song
- `listSize`: Integer tracking the number of nodes

## 2. Implementation Details

### Circular Doubly Linked List

A **circular doubly linked list** is a data structure where:
- Each node has pointers to both the next and previous nodes
- The last node's `next` points to the first node (head)
- The first node's `prev` points to the last node (tail)
- This creates a circular structure with no NULL pointers (except when list is empty)

**Advantages:**
- Efficient insertion at tail: O(1) with tail pointer
- Efficient navigation: Can traverse forward or backward
- Easy next/previous operations: O(1) by following pointers
- No need to check for NULL when traversing (except empty list)

**Disadvantages:**
- More memory overhead (two pointers per node)
- Slightly more complex implementation

## 3. Key Operations and Complexity Analysis

### 3.1 `addSong(const char* filepath)` - O(1)

**Operation:** Insert a new song at the tail of the list.

**Algorithm:**
1. Extract basename from filepath
2. Check if song already exists (O(n) worst case, but typically O(1) if not found early)
3. Create new node with song data
4. If list is empty, make it the only node (circular with itself)
5. Otherwise, insert at tail:
   - Set `newNode->next = head`
   - Set `newNode->prev = tail`
   - Update `tail->next = newNode`
   - Update `head->prev = newNode`
   - Update `tail = newNode`

**Complexity:** O(1) for insertion (with tail pointer), but O(n) for duplicate check. In practice, insertion is O(1) amortized.

**Space Complexity:** O(1) - only creates one new node.

### 3.2 `deleteSong(const char* songName)` - O(n)

**Operation:** Delete a song by name.

**Algorithm:**
1. Traverse the list to find the node with matching songName
2. If found:
   - Update `prev->next = current->next`
   - Update `next->prev = current->prev`
   - Update head/tail pointers if necessary
   - Update current pointer if it points to deleted node
   - Free the node memory
3. Decrement listSize

**Complexity:** O(n) - must search through list to find the node.

**Space Complexity:** O(1) - only uses temporary pointers.

### 3.3 `playSong(const char* songName)` - O(n)

**Operation:** Set current song, increment play count, mark favorite if count >= 3.

**Algorithm:**
1. Search for the song in the list (O(n))
2. Set `current = found_node`
3. Increment `playCount`
4. If `playCount >= 3`, set `isFavorite = 1`
5. Return song name (malloc'd string)

**Complexity:** O(n) - linear search to find the song.

**Space Complexity:** O(1) - returns a string of fixed max length.

### 3.4 `playNext()` - O(1)

**Operation:** Move to next song and play it.

**Algorithm:**
1. Set `current = current->next`
2. Increment `current->playCount`
3. If `playCount >= 3`, set `isFavorite = 1`
4. Return current song name

**Complexity:** O(1) - just follows the next pointer.

**Space Complexity:** O(1)

### 3.5 `playPrevious()` - O(1)

**Operation:** Move to previous song and play it.

**Algorithm:**
1. Set `current = current->prev`
2. Increment `current->playCount`
3. If `playCount >= 3`, set `isFavorite = 1`
4. Return current song name

**Complexity:** O(1) - just follows the prev pointer.

**Space Complexity:** O(1)

### 3.6 `searchSong(const char* songName)` - O(n)

**Operation:** Search for a song and return formatted info string.

**Algorithm:**
1. Traverse the list to find matching songName
2. Format string: "Title (Plays: X, Favorite: Yes/No)"
3. Return malloc'd string

**Complexity:** O(n) - linear search.

**Space Complexity:** O(1) - returns fixed-size string.

### 3.7 `displayPlaylist(int* outCount)` - O(n)

**Operation:** Return array of all song names.

**Algorithm:**
1. Allocate array of char* pointers (size = listSize)
2. Traverse the list once
3. For each node, allocate and copy songName to array
4. Set outCount to listSize
5. Return array

**Complexity:** O(n) - must visit every node.

**Space Complexity:** O(n) - creates array of n strings.

### 3.8 `displayFavorites(int* outCount)` - O(n)

**Operation:** Return array of favorite song names.

**Algorithm:**
1. First pass: Count favorites (O(n))
2. Allocate array of char* pointers (size = favCount)
3. Second pass: Traverse and add favorites to array (O(n))
4. Set outCount to favCount
5. Return array

**Complexity:** O(n) - two passes through the list.

**Space Complexity:** O(k) where k = number of favorites.

### 3.9 `savePlaylistToFile(const char* filename)` - O(n)

**Operation:** Save playlist to CSV file.

**Algorithm:**
1. Open file for writing
2. Traverse the list once
3. Write each node as: "songName,playCount,isFavorite\n"
4. Close file

**Complexity:** O(n) - must visit every node.

**Space Complexity:** O(1)

### 3.10 `loadPlaylistFromFile(const char* filename)` - O(n)

**Operation:** Load playlist from CSV file.

**Algorithm:**
1. Open file for reading
2. For each line:
   - Parse CSV: songName,playCount,isFavorite
   - Check if song exists (O(n) per check)
   - If exists, update playCount and isFavorite
   - If not, add new node (O(1))
3. Close file

**Complexity:** O(n*m) where n = lines in file, m = current list size (for duplicate checks).

**Space Complexity:** O(n) - adds nodes for new songs.

## 4. Memory Management

### Allocation
- All nodes are allocated using `malloc()`
- Returned strings are allocated using `malloc()`
- String arrays are allocated using `malloc()`

### Deallocation
- `cleanupPlaylist()`: Frees all nodes in the list
- `freeString()`: Frees a single malloc'd string
- `freeStringArray()`: Frees an array of malloc'd strings

### Python Integration
- Python wrapper (`playlist.py`) ensures all C-allocated memory is freed
- Uses `freeString()` and `freeStringArray()` after converting C strings to Python strings

## 5. Design Decisions

### Why Circular Doubly Linked List?

1. **Efficient Navigation:** Next/Previous operations are O(1)
2. **Natural Playlist Behavior:** Circular structure allows continuous playback
3. **Bidirectional Traversal:** Can move forward or backward efficiently
4. **Tail Insertion:** O(1) insertion at end with tail pointer

### Why Fixed-Length Strings?

- `songName[256]`: Fixed-length array prevents buffer overflows
- Safe with `strncpy()` and bounds checking
- Simpler memory management than dynamic strings

### Why Separate Head, Tail, and Current Pointers?

- **Head:** Starting point for traversal
- **Tail:** O(1) insertion at end
- **Current:** Tracks currently playing song for next/previous operations

## 6. Edge Cases Handled

1. **Empty List:** All operations check for NULL head pointer
2. **Single Node:** Circular list with node pointing to itself
3. **Duplicate Songs:** `addSong()` checks for existing songs before adding
4. **File I/O Errors:** Functions check for NULL file pointers
5. **Memory Allocation Failures:** Check malloc() return values
6. **String Overflow:** Use `strncpy()` with bounds checking

## 7. Viva-Style Q&A

**Q: Why use a circular list instead of a linear list?**
A: Circular list allows continuous playback - after the last song, next goes to first song. Also, no NULL checks needed during traversal (except for empty list).

**Q: What is the time complexity of finding a song by name?**
A: O(n) - linear search through the list. Could be improved with a hash table, but that would add complexity.

**Q: How do you handle memory leaks?**
A: All malloc'd memory is freed:
- Nodes freed in `cleanupPlaylist()`
- Strings freed via `freeString()` called from Python wrapper
- Arrays freed via `freeStringArray()`

**Q: What happens if you delete the current song?**
A: The `current` pointer is updated to point to the next node (or NULL if list becomes empty).

**Q: Why is insertion O(1) but deletion O(n)?**
A: Insertion uses the tail pointer for O(1) access. Deletion requires searching for the node first, which is O(n).

**Q: How does the favorites system work?**
A: When a song's `playCount` reaches 3 or more, `isFavorite` is automatically set to 1. This is checked in `playSong()`, `playNext()`, and `playPrevious()`.

**Q: Can the list have duplicate songs?**
A: No, `addSong()` checks for existing songs and returns 0 if duplicate is found.

**Q: What is the space complexity of the entire playlist?**
A: O(n) where n is the number of songs. Each node stores fixed-size data (songName[256], 2 ints, 2 pointers).

## 8. Summary

The circular doubly linked list provides an efficient data structure for a music playlist with:
- O(1) insertion at tail
- O(1) next/previous navigation
- O(n) search and deletion (acceptable for typical playlist sizes)
- Natural circular behavior for continuous playback
- Efficient memory usage with proper cleanup

This implementation demonstrates core data structure concepts while providing a practical, working solution for playlist management.

