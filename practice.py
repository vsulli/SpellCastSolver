
def set_vars():
    # have to keep track globally
    global user_gems
    user_gems = 0

    # player's total points
    global user_points
    user_points = 0 

    '''
    # dictionary with list as value
    # from top left to right and down
    # each letter image (key) is from index 1-25 
    # values: [0] letter(str),[1] 2X(bool), [2] DL(bool), [3] gem(bool), [4] TL(bool)
    # get the letter value by checking letter_values dict 
    # move to other location by checking letter_positions dict
    '''
    global game_board
    game_board = {}

def navigate_board():
    global user_points
    user_points += 10


def main():
    print(user_points)
    navigate_board()
    print(user_points)


set_vars()
main()