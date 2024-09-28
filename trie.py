# TODO need to go through algorithm line by line
# TODO change it to stop searching for words once at least 1 word is found 
# that is 50+ points? after amt time?
# TODO need to modify code to work with dict list
# TODO fix it to calculate TL correctly

import collections

# dictionary to store index: letter, 2x, DL, gem, TL
letter_images = {}

# need it to be valid so you can sleect any indices you want
valid_words = {}

letter_positions = {1:[-610, 449], 2:[-566, 449], 3:[-522, 449], 4:[-478, 449], 5:[-434, 449], 
                    6:[-610, 490], 7:[-566, 490], 8:[-522, 490], 9:[-478, 490], 10:[-434, 490],
                     11:[-610, 531], 12:[-566, 531], 13:[-522, 531], 14:[-478, 531], 15:[-434, 531],
                     16:[-610, 572], 17:[-566, 572], 18:[-522, 572], 19:[-478, 572], 20:[-434, 572],
                     21:[-610, 613], 22:[-566, 613], 23:[-522, 613], 24:[-478, 613], 25:[-434, 613]}

letter_values = {'A': 1, 'B': 4, 'C': 5, 'D': 3, 'E': 1, 'F': 5, 
                        'G': 3, 'H': 4, 'I': 1, 'J': 7, 'K': 6, 'L': 3, 
                        'M': 4, 'N': 2, 'O': 1, 'P': 4, 'Q': 8, 'R': 2, 
                        'S': 2, 'T': 2, 'U': 4, 'V': 5, 'W': 5, 'X': 7, 
                        'Y': 4, 'Z': 8}

def add_dict():
    valid_dict = []
    with open("collins.txt") as f:
        for line in f:
            # need to strip newline character?
            valid_dict.append(line.strip())
    return valid_dict

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        i = 0
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        if i % 1000 == 0:
            print(f"Inserted word: {word}")
        i+=1

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end_of_word
    
def create_trie(dictionary):
    trie = Trie()
    i = 0
    for word in dictionary:
        trie.insert(word)
    return trie

def find_words(board, dictionary, trie, game_board):

    def dfs(x, y, prefix, path, visited):
        i = 0
        if i % 1000 == 0:
            print("Current position:", (x, y))
            print("Current prefix:", prefix)
            print("Current path:", path)
            print("Visited cells:", visited)
        i+=1
        # Check if the current prefix is a valid word
        if trie.search(prefix):
            bool_2x = 0
            tot_val = 0
            points = 0
            # TODO - need to calculate total value by looping through path
            # and retrieving values from letter_values?
            for num in path:
                letter = game_board.get(num)[0]
                points = letter_values.get(letter)

                # if letter has DL then double just that letter
                if game_board.get(num)[2] == 1:
                    points *= 2

                # if letter has TL then triple just that letter
                if game_board.get(num)[4] == 1:
                    points *= 3

                tot_val += points  
            
            # check if any number in path has the 2x
            for num in path:
                if game_board.get(num)[1] == True:
                    tot_val *= 2

            # long word bonus +10 pts
            if len(path) >= 6:
                tot_val += 10

            valid_words[prefix] = [path, tot_val]
            
        visited.add((x, y))

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, -1), (1, 1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < len(board) and 0 <= new_y < len(board[0]) and (new_x, new_y) not in visited:
                new_prefix = prefix + board[new_x][new_y]
                if any(word.startswith(new_prefix) for word in dictionary):  # Check if the new prefix is a valid prefix
                    dfs(new_x, new_y, new_prefix, path + [len(board[0]) * new_x + new_y + 1], visited)
        visited.remove((x, y))

    for i in range(len(board)):
        for j in range(len(board[0])):
            dfs(i, j, board[i][j], [5*i + j + 1], set())

    return valid_words

def search_algo(board, dictionary, trie, game_board):

    result = find_words(board, dictionary, trie, game_board)

    # Print the grid
    print("Grid:")
    for row in board:
        print(" ".join(row))

    # Print the list of possible words and their paths
    print("\nFound Words and Their Paths:")
    # will need to sort words by their total point value
    i = 0
    for word, path in result.items():
        if i % 1000 == 0:
            print(word, path)
        i+=1

    print("\nTop 5 Words")
    print("------------------------------------------")
    # sort all words and paths by points
    # oes [[12, 15, 2], 12]
    sorted_result = sorted(result.items(), key=lambda item: item[1][1], reverse=True)

    top_5_w = []
    for i in range(min(5, len(sorted_result))):
        top_5_w.append(sorted_result[i])
        print(top_5_w[i])
    print("------------------------------------------")
    return top_5_w
    
