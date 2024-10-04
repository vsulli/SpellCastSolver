# Spellcast Solver
# 14 January 2024
# Program to automatically find the 
# word with the most amount of points 
# when it's your turn and use pyautogui
# to select those squares

# import necessary packages
import re
import time
import cv2
import mss
import pyautogui, sys
import numpy as np
from PIL import Image, ImageGrab
import extcolors
import pytesseract

# my files to import
from board import *
import config
from dictionary import *
from imageprocessing import *
from trie import *

from collections import defaultdict
from collections import OrderedDict
# from pytesseract import Output
# from imutils import contours


def read_in_dict(filename, word_list):
    # reads in dictionary of valid words and returns list
    with open(filename, "r") as f:
        lines = [line.strip() for line in f]
    return lines


def main():
    user_input = 0
    # read in the valid words to a list
    word_list = []
    word_list = read_in_dict("collins.txt", word_list ) #TODO reset to actual dict

    trie = create_trie(word_list)

    # read in first board
    format_board_image()
    # read letters and store in dict
    read_image(config.game_board)
    
    while user_input != 5:
        # new gameplay loop
        user_input = input("Please make a selection:\n" + 
                        "1) Get Current Board\n" + 
                        "2) Correct Board\n" +
                        "3) Find Best Word\n" +
                        "4) Print Current Board\n" +
                        "5) Update Dictionary\n" +
                        "6) Quit\n")
        match user_input:
            case "1":
                # process image
                format_board_image()
                # read letters and store in dict
                read_image(config.game_board)
            case "2": 
                # correct letters, gems, DL, 2X status
                correct_board(config.game_board)
            case "3": 
                # need to convert the game_board to list of lists
                board_list = convert_game_board(config.game_board)

                # gets top 5 words
                top_5 = search_algo(board_list, word_list, trie, config.game_board)
                word_selected = input("Enter the word you would like to play: \n")
                
                # uses pyautogui to select word on monitor
                navigate_board(word_selected, letter_positions, valid_words)
                
                # add to user's total points
                config.user_points += valid_words[word_selected][1]
                print("------------------------------------------")
                print("You added: " + str(valid_words[word_selected][1]) + " points.")
                print("Total points: " + str(config.user_points))
                print("------------------------------------------")

            case "4": 
                print("INDEX LETTER  2X  DL  GEM  TL \n" + 
                "------------------------------------------")
                for i in range(1, 26):
                    if config.game_board.get(i)[1] | config.game_board.get(i)[2] | config.game_board.get(i)[3]:
                        print(i, config.game_board.get(i))
                    else:
                        print(i, config.game_board.get(i)[0])
                print("------------------------------------------\n")
                board_list = convert_game_board(config.game_board)
                for row in board_list:
                    print(" ".join(row))
                    
                print("------------------------------------------\n")
            case "5": 
                user_input2 = -1
                while user_input2 != "1" or user_input2 != "2":
                # TODO
                    user_input2 = input("Would you like to add(1) or remove words(2) from the dictionary?\n")
                    match user_input2:
                        # add new words to dictionary
                        case "1":
                            pass
                            break
                        # remove words from dictionary
                        case "2":
                            word = input("Type the word to remove from the dictionary: ")
                            removeWord(word)
                            break
                        case _:
                            print("Invalid input.")
                            
                
            # TODO add option to change default locations of letters
            case "6": 
                return
            
            # default invalid input
            case _:
                print("Invalid input. Please select from the options above.")
            

main()

