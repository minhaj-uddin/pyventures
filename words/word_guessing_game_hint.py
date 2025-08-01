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


def use_hint(secret_word, guessed_words):
    unguessed = [letter for letter in set(
        secret_word) if letter not in guessed_words]
    if unguessed:
        hint_letter = random.choice(unguessed)
        guessed_words.add(hint_letter)
        print(f"Hint used! The letter '{hint_letter}' is in the word.")
    else:
        print("No more letters to reveal.")


def get_guess(guessed_words, allow_hint=True):
    while True:
        guess = input("Enter a letter or type 'hint': ").lower()
        if guess == 'hint' and allow_hint:
            return 'hint'
        elif guess == 'hint':
            print('No hints left.')
        elif len(guess) != 1:
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
    attempts_left = 6
    hints_left = 2

    print("\nNew Game Started!")
    while attempts_left > 0:
        display_word(secret_word, guessed_words)
        print(f"Hints left: {hints_left}")
        guess = get_guess(guessed_words, allow_hint=hints_left > 0)

        if guess == 'hint':
            if hints_left > 0:
                use_hint(secret_word, guessed_words)
                hints_left -= 1
                if is_word_guessed(secret_word, guessed_words):
                    print(
                        f'Congratulations! You guessed the word: {secret_word}')
                    return True
            else:
                print('No hints remaining.')
            continue

        guessed_words.add(guess)

        if guess in secret_word:
            print('Good guess!')
            if is_word_guessed(secret_word, guessed_words):
                print(f'Congratulations! You guessed the word: {secret_word}')
                return True
        else:
            attempts_left -= 1
            print(f'Wrong guess! Attempts left: {attempts_left}')

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
