import random
import json

dice_counter = 0  # Number of times dice were rolled

while True:
    choice = input('Roll the dice? (y/n): ').lower()
    if choice == 'y':
        while True:
            num_dice_input = input('How many dice would you like to roll? ')
            if num_dice_input.isdigit() and int(num_dice_input) > 0:
                dice_total = 0
                num_dices = int(num_dice_input)
                print('You rolled:', num_dices)

                total_dice_rolled = 0  # Total number of individual dice rolled
                roll_history = []  # To store all entire roll results
                current_roll = []  # To store all current roll results

                for _ in range(num_dices):
                    die1 = random.randint(1, 6)
                    die2 = random.randint(1, 6)
                    dice_total += (die1 + die2)
                    current_roll.append((die1, die2))
                    print(f'({die1}, {die2})')

                dice_counter += 1
                roll_history.append(current_roll)
                total_dice_rolled += num_dices
                dice_average = dice_total/num_dices

                print(f"Total rolls this session: {dice_counter}")
                print(f"Total individual dice rolled: {total_dice_rolled}")
                print(f"Total dice sum this session: {dice_total}")
                print(f"Total dice average this session: {dice_average}")

                session_data = {
                    "total_rolls": dice_counter,
                    "total_dice_rolled": total_dice_rolled,
                    "total_dice_sum": dice_total,
                    "total_dice_avg": dice_average,
                    "roll_history": roll_history
                }

                with open("dice_roll_history.json", "a") as file:
                    json.dump(session_data, file, indent=2)
                    file.write("\n")

                print('Session data saved to "dice_roll_history.json".')
                break
            else:
                print('Please enter a number greater than 0.')

    elif choice == 'n':
        print(
            f'Thanks for playing! You rolled the dice {dice_counter} times this session.')
        break
    else:
        print('Invalid choice! Please enter "y" or "n".')
