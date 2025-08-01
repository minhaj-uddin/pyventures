import random


def get_range_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Please enter a valid integer.")


print("Welcome to the Number Guessing Game!")
min_val = get_range_input("Enter the minimum number: ")
max_val = get_range_input("Enter the maximum number: ")

while max_val <= min_val:
    print("Maximum must be greater than minimum.")
    max_val = get_range_input("Enter a valid maximum number: ")

guess_count = 0
max_guess_limit = 5
number_to_guess = random.randint(min_val, max_val)

while True:
    try:
        if guess_count >= max_guess_limit:
            print(f"You've reaached maximum guess limit of {max_guess_limit}")
            print(f"Guess number is: {number_to_guess}")
            break

        guess = int(
            input(f'Guess the number between {min_val} and {max_val}: '))
        guess_count += 1

        if guess < number_to_guess:
            print('Too low!')
        elif guess > number_to_guess:
            print('Too high!')
        else:
            print('Congratulations! You guessed the number.')
            break
    except ValueError:
        print('Please enter a valid number.')
