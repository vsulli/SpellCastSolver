# SPELLCAST SOLVER



# Project Overview

- inserts all the words in the dictionary into trie and prints to console
- shows to the screen a b&w image of the curretn board in discord
- cuts out 26 block images as jpg for character recognition
- prints to the console what blocks were recognized as and whether it detected 2x, DL, gem or TL
- prints to the console a representation of the board with their indices and letter as recognized with computer vision


# TODO LIST

# CHANGES
- option to try new ocr on a single row, single column or single square?

* computer vision - recognize playing area
* recognize the squares

* dictionary with values of letters and the letter
{A: 1, B: 4, C: 5, D: 3, E: 1, F: 5, G: 3, H: 4, I: 1, J: 7, K: 6, L: 3, M: 4, N: 2, O: 1, P: 4, Q: 8, R: 2, S: 2, T: 2, U: 4, V: 5, W: 5, X: 7, Y: 4, Z: 8}

* prioritize tiles with gems

* how to handle if it's "almost" a word - just need to swap 1 (do that if you have at least 3 gems)

# Optical Character Recognition
https://pyimagesearch.com/2020/08/17/ocr-with-keras-tensorflow-and-deep-learning/

# ocring video streams
https://pyimagesearch.com/2022/03/07/ocring-video-streams/

# spellcast solver - collins.txt from Oli Bomby on Github
https://raw.githubusercontent.com/OliBomby/SpellCastSolver/master/SpellCastSolverLib/collins.txt

* 279,494 total words 

Python Tuples

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
>>> record[0]
'John'
>>> record[1]
35
>>> record[2]
'Python Developer'


Pseudocode for traversing the board to get valid words:

start from source node top left
right first (then diagonal and down)
get letter of source node, get letter of right node
check to see if in word_list - use binary search?
if it is, store it in possibilities list? [word, point value] - only keep top 5?
while valid word, keep going in that direction, if not, try all other valid directions

https://www.lavivienpost.com/depth-first-search-and-matrix/

https://medium.com/@ojhasaurabh2099/traversing-a-grid-using-dfs-ac7a391f7af8

** MEDIUM ARTICLE --> DIRECTION VECTORS & VALIDATOR FUNCTIONS


DEPTH FIRST TRAVERSAL ON A 2D ARRAY

https://www.geeksforgeeks.org/depth-first-traversal-dfs-on-a-2d-array/

* direction vectors are used to traverse the adjacent cells of a given cell in a given order
ex) (x, y) 
adjacent cells (x-1, y), (x, y+1), (x+1, y), (x, y-1)
direction vectors (-1, 0), (0, 1), (1, 0), (0, -1) up, left, down, right order

** Geeks for Geeks
Example code for DFS
https://www.geeksforgeeks.org/depth-first-traversal-dfs-on-a-2d-array/


Desired Output for Checking Grid

1-> 2 (check if valid)
continue

1->7
1-> 6
2-> 1
2->3
2->8
2->7
2->6
----------------------
13->7
13->8
13->9
13->14
13->19
13->18
13->17
13->12 

* possibly look into adjacency lists?

BFS seems closer to what I need
1 6 7 2 11 12 13 8 3 16 17 18 19 14 9 4 21 22 23 24 25 20 15 10 5 

* way to change start? 
since the parameters are row and column, can change start easily 
* how do I continue a chain? linked list?
https://www.geeksforgeeks.org/construct-linked-list-2d-matrix/

* how to do this for diagonal ones?
https://www.geeksforgeeks.org/construct-a-doubly-linked-linked-list-from-2d-matrix/ 

Trie Data Structure
https://www.geeksforgeeks.org/advantages-trie-data-structure/
Trie (also known as tree) - tree-based data structure used to store an associative array where the keys are sequences
advantages: fast search, space-efficient, auto-complete, efficient insertion and deletion, compact representation

* maximum number of children of a node is the size of the alphabet

GRID-BASED DFS ALGORITHM
if dx == 0 and dy == 0:
    continue
** explore neighboring cells around the current cell 

DFS > BFS for word search problem because it is more memory efficient

Code to work for a 5x5 grid

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

# Example usage:
board = [['a', 't', 'e', 'm', 'p'],
         ['s', 'r', 'n', 'o', 't'],
         ['i', 'o', 'l', 'i', 'o'],
         ['a', 'b', 'c', 'd', 'e'],
         ['f', 'g', 'h', 'i', 'j']]

dictionary = {"ate", "at", "tea", "sat", "in", "or", "ion", "lion"}  # Using a set for dictionary

result = find_words(board, dictionary)

# Print the grid
print("Grid:")
for row in board:
    print(" ".join(row))

# Print the list of possible words and their paths
print("\nFound Words and Their Paths:")
for word, path in result.items():
    print(word, path)




##  differences 

     dfs(new_x, new_y, prefix + board[x][y], path + [(5*x) + y + 1], visited)  # Convert (x, y) to a number
        visited.remove((x, y))


    if not (0 <= x < len(board)) or not (0 <= y < len(board[0])) or (x, y) in visited:


    * Need to add a check before adding to the prefix - where if the resulting combination of letters does not exist in the dictionary, it will stop going down that path 



    Improving Readability by separating out functions into files

    board-actions.py
    - read in board
    - display board
    - update/correct board

    * change file location for where board is read from

    ** Need to go back to reading live image of discord spellcast & saving new image of board
    

    # testing the difference in thresholds / white percentages for TL vs DL crop
# TL
print(img_color_percent('block_11.jpg', 40))

# DL
print(img_color_percent('C:/Users/paro/Coding Projects/SpellCastSolver/sample_board_1 - DL, 2X/block_1.jpg', 40))


THINGS TO FIX: 
- need to reset result list when finding words?
- previously played words showing up in top 5 words list


- option to reset points
- option to remove word from dictionary
- calculate gems as you pick them up or read gem section

- detect TL
- fix letter detection for similar ones (n/m, w/m, v/y, o/q, i/t)
- different modes: automatically play game or allow user to enter word

* summarize for every 1000 entries with print statements to speed up


* naming cropped images incorrectly for indices 11-15


* have to use conda to use cv2
* TODO need to finish 5 - update dictionary