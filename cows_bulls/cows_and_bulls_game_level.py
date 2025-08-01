import random


def generate_secret(length):
    digits = list(range(10))
    random.shuffle(digits)
    return ''.join([str(digit) for digit in digits[:length]])


def calculate_cows_and_bulls(secret, guess):
    bulls = sum([1 for i in range(len(secret)) if guess[i] == secret[i]])
    cows = sum([1 for i in range(len(secret)) if guess[i] in secret]) - bulls
    return cows, bulls


def set_difficulty():
    print("Choose your difficulty level:")
    print("1. Easy (4 digits, 20 attempts)")
    print("2. Medium (5 digits, 15 attempts)")
    print("3. Hard (6 digits, 10 attempts)")

    while True:
        choice = input("Enter your choice (1/2/3): ")
        if choice == '1':
            return 4, 20  # 4 digits, 20 attempts
        elif choice == '2':
            return 5, 15  # 5 digits, 15 attempts
        elif choice == '3':
            return 6, 10  # 6 digits, 10 attempts
        else:
            print("Invalid choice. Please select 1, 2, or 3.")


def main():
    length, max_attempts = set_difficulty()
    secret = generate_secret(length)
    print(f"Try to guess the {length}-digit number with unique digits!")
    print(f"You have maximum {max_attempts} attempts.")

    attempts_left = max_attempts

    while attempts_left > 0:
        guess = input(f"Attempts left: {attempts_left}. Guess: ")

        if len(guess) == length and guess.isdigit() and len(set(guess)) == length:
            cows, bulls = calculate_cows_and_bulls(secret, guess)
            print(f'{cows} cows, {bulls} bulls')

            if bulls == length:
                print('Congratulations! You guessed the correct number.')
                break

            attempts_left -= 1
        else:
            print(
                f'Invalid guess. Please enter a {length}-digit number with unique digits.')

    if attempts_left == 0:
        print(
            f"Sorry, you've run out of attempts. The secret number was: {secret}")


if __name__ == '__main__':
    main()
