# functions to update words in the "dictionary" - collins.txt
import bisect
import string


def removeWord(word):
    word = word.lower()

    # skip lines to be removed
    with open("collins.txt", 'r+') as file:
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
        print("Word Removed: " + word + "\n") if inDictionary else print("Word does not appear.\n")
        
        file.close()


def addWord(word):
    with open("test_dict.txt", 'r+') as file:
        word_list= file.readlines()
        bisect.insort(word_list, word.lower()+"\n")
        file.seek(0)
        file.truncate()
        file.writelines(word_list[:])
        print("Word Added: " + word)

    file.close()


# removeWord("RUn")
addWord("doggy")