import random


def read_words(filename='words.txt'):
    try:
        with open(filename, 'r') as file:
            return [word.strip().lower() for word in file if word.strip()]
    except FileNotFoundError:
        print(f'{filename} does not exist.')
        return []


def filter_words_by_difficulty(words, level):
    if level == 'easy':
        return [word for word in words if len(word) <= 4]
    elif level == 'medium':
        return [word for word in words if 5 <= len(word) <= 6]
    elif level == 'hard':
        return [word for word in words if len(word) >= 7]
    else:
        return []


def choose_difficulty():
    while True:
        choice = input(
            "Choose difficulty - Easy (E), Medium (M), Hard (H): ").strip().lower()
        if choice in ['e', 'easy']:
            return 'easy'
        elif choice in ['m', 'medium']:
            return 'medium'
        elif choice in ['h', 'hard']:
            return 'hard'
        else:
            print("Invalid input. Please choose E, M, or H.")


def display_word(secret_word, guessed_words):
    print(''.join(letter if letter in guessed_words else '_' for letter in secret_word))


def get_guess(guessed_words):
    while True:
        guess = input('Enter a letter: ').lower()
        if len(guess) != 1:
            print('Please enter only one letter.')
        elif not guess.isalpha():
            print('Only letters (a-z) are allowed.')
        elif guess in guessed_words:
            print('You already guessed that letter.')
        else:
            return guess


def is_word_guessed(secret_word, guessed_words):
    return all(letter in guessed_words for letter in secret_word)


def play_single_game(filtered_words):
    secret_word = random.choice(filtered_words)
    guessed_words = set()
    attempts = 6

    print("\nNew Game Started!")
    while attempts > 0:
        display_word(secret_word, guessed_words)
        guess = get_guess(guessed_words)
        guessed_words.add(guess)

        if guess in secret_word:
            print('Good guess!')
            if is_word_guessed(secret_word, guessed_words):
                print(f'Congratulations! You guessed the word: {secret_word}')
                return True
        else:
            attempts -= 1
            print(f'Wrong guess! Attempts left: {attempts}')

    print(f'Game over! The word was: {secret_word}')
    return False


def play_session():
    words = read_words()
    if not words:
        return

    difficulty = choose_difficulty()
    filtered_words = filter_words_by_difficulty(words, difficulty)

    if not filtered_words:
        print(f'No words found for difficulty "{difficulty}".')
        return

    wins, losses = 0, 0

    while True:
        won = play_single_game(filtered_words)
        if won:
            wins += 1
        else:
            losses += 1

        print(f'\nScore: {wins} Win(s), {losses} Loss(es)')
        again = input('Play again? (y/n): ').strip().lower()
        if again != 'y':
            print('Thanks for playing!')
            break


if __name__ == '__main__':
    play_session()
