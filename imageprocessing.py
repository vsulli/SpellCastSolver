# handles all the computer vision processing of game board image
import cv2
import extcolors
from PIL import Image, ImageGrab
import numpy as np
import pytesseract

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def remove_noise(image):
    return cv2.medianBlur(image,5)

def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def get_colors(img_path):
    img = Image.open(img_path).convert("RGBA")
    return extcolors.extract_from_image(img, tolerance=33, limit=10)

# to check if gem exists
def img_color_pink(img_path, threshold):
    # pink ranges
    # R 180-255
    # G 35-160 
    # B 125-255

    colors = get_colors(img_path)
    total_pixels = colors[1]

    for index, color in colors[0]:
        if round(color / total_pixels * 100) >= 1:
            percent = round(color / total_pixels * 100)
            # if R, G, & B are in the range of "pink"
            if index[0] in range(180,256) and index[1] in range(35,160) and index[2] in range(125,255):
                return True
    return False

def img_color_percent(img_path, threshold):
    white = 0
    250 <= white <= 255
    colors = get_colors(img_path)
    total_pixels = colors[1]

    for index, color in colors[0]:
        if round(color / total_pixels * 100) >= 1:
            percent = round(color / total_pixels * 100)
            # if color is white 
            if (index == (255, 255, 255) or index == (251, 251, 251)) and percent >= threshold:
                # return true if it meets threshold for variable
                return True
    return False

def zoom_at(img, zoom=1, angle=0, coord=None):
    cy, cx = [i/2 for i in img.shape[:-1]] if coord is None else coord[::-1]
    rot_mat = cv2.getRotationMatrix2D((cx, cy), angle, zoom)
    result = cv2.warpAffine(img, rot_mat, img.shape[1::-1], flags=cv2.INTER_LINEAR)
    return result

def change_box(img, original_text):
    w1 = 12
    h1 = 30
    box = (w1, w1, h1, h1)
    # 5 attempts
    for i in range(5):
        new_letter2 = img.crop(box)
        myconfig = r"--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        new_letter = pytesseract.image_to_string(new_letter2, lang='eng', config=myconfig)
        
        if len(new_letter.strip()) == 1:
            return new_letter

        # adjust size of cropped box to better detect letter
        else: 
            w1 += 1
            h1 += 1
        
    # if wasn't able to detect just one letter, return second letter 
    if len(original_text) > 1:
        return original_text[1]
    return ""
            
def format_board_image():
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
    # just getting the board image
    # -636, 420(top, left)     -411, 640 (bottom, right)
    mon = {'top': 420, 'left': -636, 'width':225, 'height': 225}
    
    # bbox = (x1, y1, x2, y2)-643, 397, -406, 629
    screen = ImageGrab.grab(bbox = (-636, 424, -418, 637), all_screens=True)
    screen.save('current_b_c.png')
    current_b_c = screen.save('current_b_g.png')

    img = cv2.imread('current_b_g.png')
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    color_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # blur = cv2.GaussianBlur(gray_image, (5,5), 0)
    thresh = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    edged = cv2.Canny(thresh, 30, 200)

    # working on getting rid of more noise
    kernel = np.ones((2,2), np.uint8)
    erosion = cv2.erode(thresh, kernel, iterations = 1)
    invert = 255 - erosion

    color = cv2.cvtColor(erosion, cv2.COLOR_GRAY2RGB)
    color_copy = color.copy()

    # creating larger copy
    ratio = color.shape[0] / color.shape[1]
    img = cv2.resize(color, (1100, int(1100 * ratio)))
    # cv2.imshow('test', img)

    # cropping based on contour               
    contours2, hierarchy = cv2.findContours(image=erosion, mode=cv2.RETR_CCOMP, method=cv2.CHAIN_APPROX_NONE) 
    
    # TODO make own function
    # commenting out section that saves letter cutouts
    i = 26
    for c in contours2:
        if cv2.contourArea(c) > 200:
            # get bounding rectangle
            x, y, w, h = cv2.boundingRect(c)
            # save a cropped image for each contour
            cv2.imwrite('block_{}.jpg'.format(i), erosion[y:y+h, x:x+w])
            cv2.imwrite('colored_letter_images\\block_{}.jpg'.format(i), color_image[y:y+h, x:x+w])
            i -= 1

    # draw the rectangles
    copy = cv2.drawContours(color_copy, contours2, -1, (0, 255, 0), 1)

    cv2.imshow('Processed', gray_image) # copy
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def read_image(game_board):
    # read through all images
    print("INDEX LETTER  2X  DL  GEM  TL \n" + 
          "------------------------------------------")
    for i in range(1, 26):
        new_letter = Image.open('block_{}.jpg'.format(i))
        new_letterc = Image.open('colored_letter_images\\block_{}.jpg'.format(i))

        # reset to defaults
        x2 = False
        dl = False
        gem = False
        tl = False

        # check 2x - right corner
        box = (26,1,38,13)
        cropped_2x = new_letter.crop(box)
        cropped_2x.save('cropped_2x.jpg')
        x2 = img_color_percent('cropped_2x.jpg', 40)

        # can either be DL or TL, but not both - exclusive or
        # check DL - left corner
        # crop(left, top, right, bottom)
        box = (5,4,15,15)
        cropped_dl = new_letter.crop(box)
        cropped_dl.save('cropped_dl.jpg')
        dl = img_color_percent('cropped_dl.jpg', 40)

        #TODO add check for TL by getting a crop of corner
        # how to comapre to DL? 

        # check gem - bottom left corner
        box = (5,21,12,33)
        cropped_gem = new_letterc.crop(box)
        cropped_gem.save('cropped_gem.jpg')
        gem = img_color_pink('cropped_gem.jpg', 3)

        w1 = 11
        h1 = 29

        box = (w1,w1,h1,h1)
        new_letter2 = new_letter.crop(box)
        new_letter2.save('cropped_letter.jpg')
        img = cv2.imread('cropped_letter.jpg')
        myconfig = r"--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        text = pytesseract.image_to_string(new_letter2, lang='eng', config=myconfig)

        
        # 2 chars detected, change box size 
        # try again 
        if len(text.strip()) != 1:
            text = change_box(new_letter, text)
            
        # add all info to letter dict
        game_board[i] = [text.strip(), x2, dl, gem, tl]

        # TODO make function to print dictionary of letters with bools
        if game_board.get(i)[1] | game_board.get(i)[2] | game_board.get(i)[3]:
            print(i, game_board.get(i))
        else:
            print(i, game_board.get(i)[0])
        
        
        '''
        cv2.imshow('Letter', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows
        '''

    print('------------------------------------------')
    count = 1
    for k in game_board:
        print (' {0}:{1} | '.format(k, game_board.get(k)[0]), end="")
        # print(k, game_board.get(k)[0])
        if count % 5 == 0:
            print("\n")
        count += 1

