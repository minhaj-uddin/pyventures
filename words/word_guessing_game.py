import random


def read_words(filename='words.txt'):
    try:
        with open(filename, 'r') as file:
            return file.read().splitlines()
    except FileNotFoundError:
        print(f'{filename} does not exist.')
        return []


def display_word(secret_word, guessed_letters):
    print(''.join(letter if letter in guessed_letters else '_' for letter in secret_word))


def get_guess(guessed_letters):
    while True:
        guess = input('Enter a letter: ').lower()
        if len(guess) != 1:
            print('Please enter only one letter.')
        elif not guess.isalpha():
            print('Only letters (a-z) are allowed.')
        elif guess in guessed_letters:
            print('You already guessed that letter.')
        else:
            return guess


def is_word_guessed_letters(secret_word, guessed_letters):
    return all(letter in guessed_letters for letter in secret_word)


def play_game():
    words = read_words()
    if not words:
        return

    secret_word = random.choice(words).lower()
    guessed_letters = set()
    attempts = 6

    print("Welcome to the Word Guessing Game!")
    while attempts > 0:
        display_word(secret_word, guessed_letters)
        guess = get_guess(guessed_letters)
        guessed_letters.add(guess)

        if guess in secret_word:
            print('Good guess!')
            if is_word_guessed_letters(secret_word, guessed_letters):
                print(f'Congratulations! You guessed the word: {secret_word}')
                return
        else:
            attempts -= 1
            print(f'Wrong guess! Attempts left: {attempts}')

    print(f'Game over! The word was: {secret_word}')


if __name__ == '__main__':
    play_game()
