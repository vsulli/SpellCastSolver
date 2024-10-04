# SPELLCAST SOLVER

A program that uses computer vision to take images of the Discord game SpellCast, calculate the words with most points, and select the desired word using pyautogui.

# PROJECT OVERVIEW

- Inserts all the words in the dictionary into trie and prints to console
- Shows a b&w image of the current board in discord on the screen
- Cuts out 26 block images as .jpg images for character recognition
- Prints to the console what blocks were recognized as and whether it detected 2x, DL, or gem
- Prints to the console a representation of the board with their indices and letter as recognized with computer vision
- Menu Options: 
    - Taking a screenshot of the new board and detecting letters
    - Correcting any of the states of a tile (letter, gem, DL, TL, 2x)
    - Calculating the top 5 words by point value
    - Adding & removing words from dictionary text document

# TODO LIST

- Error handling for preventing the addition of duplicate words to the dictionary

- Add function to select and save coordinates for the corners of the game board
    - I currently have stored values based on the resolution of my second monitor. Using pyautogui I could adapt it to work on any monitor by calculating the relative positions of each tile

# CHANGES

* If I were to start this project over, given what I've learned during its completion, I would implement some of these changes. 

- There are ways to train the model on custom data, so if I were to return to this project I would try to train it with custom images of multiple letter cutouts that included some of the special statuses at random.
    - detection of TL by reading the "TL" characters

- Option to try new OCR on a single row, single column or single square of the board

- Improve the efficiency of removal/insertion of words to the dictionary file using binary search

- JSON database for storing the dictionary of words

- Currently calculating all of the possible valid words takes a lot of time, so I would probably add a condition to exit the trie if a word is found that is 50+ points or allow the user to set a time threshold anywhere from 30s to an unlimited amount of time

- The current program doesn't make use of swap letter or shuffle, so that is a functionality that I could learn how to implement in the future

- Different modes: automatically play the game or allow user to enter word

# RESEARCH NOTES

## opencv

[opencv docs](https://docs.opencv.org/4.x/d9/df8/tutorial_root.html)

* While computer vision did not end up having 100% accuracy in this project, the purpose was to attempt to use computer vision to bypass manual entry of each letter and status(gem, TL, DL, 2x). 

**Optical Character Recognition**
https://pyimagesearch.com/2020/08/17/ocr-with-keras-tensorflow-and-deep-learning/

**Ocring Video Streams**
https://pyimagesearch.com/2022/03/07/ocring-video-streams/

* I decided to go with images of the game board over a video stream because a constant video stream would be memory intensive and what changes on the board 
only really matters when a word is played and new characters are generated


## pyautogui

[pyautogui docs](https://pyautogui.readthedocs.io/en/latest/)

## Discord - SpellCast

[SpellCast Rules](https://discord.fandom.com/wiki/SpellCast)

* dictionary with values of letters and the letter

{A: 1, B: 4, C: 5, D: 3, E: 1, F: 5, G: 3, H: 4, I: 1, J: 7, K: 6, L: 3, M: 4, N: 2, O: 1, P: 4, Q: 8, R: 2, S: 2, T: 2, U: 4, V: 5, W: 5, X: 7, Y: 4, Z: 8}

**Dictionary**

[collins.txt from Oli Bomby on Github](https://raw.githubusercontent.com/OliBomby/SpellCastSolver/master/SpellCastSolverLib/collins.txt)

* 279,494 total words 
* Discord did not have an official list of the words they use in their game and I found that some English words that are considered valid in other dictionaries did not occur in SpellCast. The collins.txt list of words still includes some words that are not valid in SpellCast, but there is now an option to delete those words as they are encountered


**Python Tuples**

Ordered: They contain elements that are sequentially arranged according to their specific insertion order.
Lightweight: They consume relatively small amounts of memory compared to other sequences like lists.
Indexable through a zero-based index: They allow you to access their elements by integer indices that start from zero.
Immutable: They don’t support in-place mutations or changes to their contained elements. They don’t support growing or shrinking operations.
Heterogeneous: They can store objects of different data types and domains, including mutable objects.
Nestable: They can contain other tuples, so you can have tuples of tuples.
Iterable: They support iteration, so you can traverse them using a loop or comprehension while you perform operations with each of their elements.
Sliceable: They support slicing operations, meaning that you can extract a series of elements from a tuple.
Combinable: They support concatenation operations, so you can combine two or more tuples using the concatenation operators, which creates a new tuple.
Hashable: They can work as keys in dictionaries when all the tuple items are immutable.

* can access individual objects in a tuple by position or index

indices start from zero
record = ("John", 35, "Python Developer")
record[0]
'John'
record[1]
35
record[2]
'Python Developer'

## DFS

DFS > BFS for word search problems because it is more memory efficient

[dfs and matrices](https://www.lavivienpost.com/depth-first-search-and-matrix/)

[dfs on a 2D array](https://www.geeksforgeeks.org/depth-first-traversal-dfs-on-a-2d-array/)

[direction vectors and validator functions](https://medium.com/@ojhasaurabh2099/traversing-a-grid-using-dfs-ac7a391f7af8)

* a validator function is necessary to make sure that the generated coordinate doesn't go out of bounds

* direction vectors are used to traverse the adjacent cells of a given cell in a given order
ex) (x, y) 
adjacent cells (x-1, y), (x, y+1), (x+1, y), (x, y-1)
direction vectors (-1, 0), (0, 1), (1, 0), (0, -1) 
left, down, right, up
* as y increases, it goes down the page and as y decreases it goes up the page

         [x, y-1]
[x-1,y]  [x,y]     [x+1, y]
         [x, y+1]

## Trie Data Structure
[Geeks for Geeks Trie Data Structure](https://www.geeksforgeeks.org/advantages-trie-data-structure/)

Trie (also known as a prefix tree) - tree-based data structure that stores an array of sequences

advantages: fast search, space-efficient, auto-complete, efficient insertion and deletion, compact representation

* maximum number of children of a node is the size of the alphabet

### Trie Code to Work for a 5x5 Grid

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word

def find_words(board, dictionary):
    trie = Trie()
    for word in dictionary:
        trie.insert(word)

    valid_words = {}  # Using a dictionary to store words and their paths

    def dfs(x, y, prefix, path, visited):
        if trie.search(prefix):
            valid_words[prefix] = path

        if not (0 <= x < len(board)) or not (0 <= y < len(board[0])) or (x, y) in visited:
            return
        
        visited.add((x, y))
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            new_x, new_y = x + dx, y + dy
            dfs(new_x, new_y, prefix + board[x][y], path + [(5*x) + y + 1], visited)  # Convert (x, y) to a number
        visited.remove((x, y))

    for i in range(len(board)):
        for j in range(len(board[0])):
            dfs(i, j, '', [], set())

    return valid_words

### Example usage:
board = [['a', 't', 'e', 'm', 'p'],
         ['s', 'r', 'n', 'o', 't'],
         ['i', 'o', 'l', 'i', 'o'],
         ['a', 'b', 'c', 'd', 'e'],
         ['f', 'g', 'h', 'i', 'j']]

dictionary = {"ate", "at", "tea", "sat", "in", "or", "ion", "lion"}  # Using a set for dictionary

result = find_words(board, dictionary)

**Print the grid**
print("Grid:")
for row in board:
    print(" ".join(row))

**Print the list of possible words and their paths**
print("\nFound Words and Their Paths:")
for word, path in result.items():
    print(word, path)

## TL, DL and Gem Detection 
**TL**

print(img_color_percent('block_11.jpg', 40))

- I was unable to consistently detect the TL symbol in the image due to the low image quality of the characters themselves and there not being much of a difference in the pixel percentages between TL and DL. 

**DL**

dl = img_color_percent('cropped_dl.jpg', 40)

[Array bisection algorithm](https://docs.python.org/3/library/bisect.html)

-  bisect insort assumes the list is already sorted