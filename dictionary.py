# functions to update words in the "dictionary" - collins.txt
import string

def removeWord(word):
    word = word.lower()

    # skip lines to be removed
    with open("test_dict.txt", 'r+') as file:
        inDictionary = False
        lines = file.readlines()
        # move to beginning of file
        file.seek(0)
        file.truncate()

        #iterate over each line
        for line in lines:
            # each word has newline character
            if line != word + "\n":
                file.write(line)
            elif line == word + "\n":
                inDictionary = True
        print("Word Removed: " + word) if inDictionary else print("Word does not appear.")
        
        file.close()


def addWord(my_dictionary, word):
    pass


removeWord("RUn")