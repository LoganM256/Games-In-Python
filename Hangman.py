import random
from words import words
import string

def get_valid_word(words):
    word = random.choice(words) #takes in a list and randomly chooses an item from it
    while '-' in word or ' ' in word:
        word = random.choice(words)
    return word.upper()

def hangman():
    word = get_valid_word(words)
    word_letters = set(word) #keeps track of what has already been guessed in the word
    alphabet = set(string.ascii_uppercase)
    used_letters = set() #what the user has guessed
    #get the user input until the set is empty

    lives = 6

    while len(word_letters) > 0 and lives > 0:
        #what letters they have already used to keep track
        #.join turns this iterable set into a string seperated by whatever it was before the .join
        print(f'You have {lives} lives left. You have used these letters: ', ' '.join(used_letters))

        #we need to tell the user what the current word is (W - R D)
        word_list = [letter if letter in used_letters else '-' for letter in word]
        print('Current word: ', ' '.join(word_list))

        user_letter = input("Guess a letter: ").upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter) 
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives = lives - 1 #takes a life away
                print("Letter is not in the word.")
        elif user_letter in used_letters:
            print("You have already guessed that character. Please try again.")
        else:
            print("Invalid character or incorrect word. Please try again.")
    if lives == 0:
        print(f"You died! The word was, {word}.")
    else:
        print(f'Congrats!, you figured out the word {word}!')
#we get here once the len(word_letters) == 0

hangman()
