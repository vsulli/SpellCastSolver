# all board actions

import pyautogui
from pynput import mouse
import re

# need it to be valid so you can sleect any indices you want
# valid_words = {}

board_indices = [[1, 2, 3, 4, 5],
         [6, 7, 8, 9, 10],
         [11, 12, 13, 14, 15],
         [16, 17, 18, 19, 20],
         [21, 22, 23, 24, 25]]

# TODO create function that lets user click for their screen
# from top left to right and down
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

# automatically navigate to positions of letters to form word
# TODO need to finish navigate board to use pyautogui to select each letter
def navigate_board(word_selected, letter_positions, valid_words):
    # list of indices 
    path = valid_words[word_selected][0]

    # move to first letter and left-click
    pyautogui.moveTo(letter_positions[path[0]])
    pyautogui.mouseDown()

    # move to all other letters
    for i in range(1,len(path)):
        pyautogui.moveTo(letter_positions[path[i]])
    pyautogui.mouseUp()

# TODO make function to get positions of areas on screen
    # pyautogui.displayMousePosition()

# TODO complete function to get position of each letter using pynput
# pyautogui can't read/record clicks or keystrokes
# allows user to define center of each letter on their screen
def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))
    if not pressed:
        # Stop listener
        return False
    
def correct_board(game_board):
    print("Correct the board by typing\n" + 
          "in: index letter\n" +
          "Type 'q' to proceed.")
    done = ""
    while done != "q":
        done = input("")
    # match (one number 1-9) or 10-15, 20-25 or 16-19 " " 
    # uppercase letter or lowercase letter
        match = r'(^[1-9]{1}|[12][0-5]|1[6-9]) ([A-Z]|[a-z])' 
        correction = re.findall(match, done)
        if correction:
            index = int(correction[0][0])
            # index, letter
            # [('16', 'G')]
            values = game_board.get(index)
            values[0] = correction[0][1].upper()
            game_board.update({index:values})
            print(game_board.get(index))
            print("Updated letter on board.")

    print("Correct the 2X, DL, gem, TL status of a letter on the board\n" + 
          "by typing: index 2X 1/0, index DL 1/0, index gem 1/0, index TL 1/0\n" +
          "Type 'q' to proceed.")
    done = ""
    while done != "q":
        done = input("")
        # correct gems
        match = r'(^[1-9]{1}|[12][0-5]|1[6-9]) gem ([0-1])'
        correction = re.findall(match, done)
        if correction:
            correct_values(correction, 3, game_board)
            print("Updated gem at index: " + str(correction[0][0]))
            print(game_board[int(correction[0][0])])

        # correct DL
        match = r'(^[1-9]{1}|[12][0-5]|1[6-9]) DL ([0-1])'
        correction = re.findall(match, done)
        if correction:
            correct_values(correction, 2, game_board)
            print("Updated DL at index: " + str(correction[0][0]))
            print(game_board[int(correction[0][0])])

        # correct TL
        match = r'(^[1-9]{1}|[12][0-5]|1[6-9]) TL ([0-1])'
        correction = re.findall(match, done)
        if correction:
            correct_values(correction, 4, game_board)
            print("Updated TL at index: " + str(correction[0][0]))
            print(game_board[int(correction[0][0])])

        # correct 2X
        match = r'(^[1-9]{1}|[12][0-5]|1[6-9]) 2X ([0-1])'
        correction = re.findall(match, done)
        if correction:
            correct_values(correction, 1, game_board)
            print("Updated 2X at index: " + str(correction[0][0]))
            print(game_board[int(correction[0][0])])

# convert game_board to list of letters for trie
def convert_game_board(game_board):
    board_list = []
    num = 1
    for i in range(5):
        sublist = []
        for j in range(5):
            letter = game_board.get(num)[0]
            sublist.append(letter.lower())
            num += 1
        board_list.append(sublist)
    return board_list

# function menu for correcting letters or (2x, DL, gems, TL)
def correct_values(correction, vi, game_board):
    index = int(correction[0][0])
    values = game_board.get(index)
    if correction[0][1] == '0':
        x = False
    else:
        x = True
    values[vi] = x
    game_board.update({index:values})

'''
listener = mouse.Listener(
    on_click=on_click)
listener.start()
'''