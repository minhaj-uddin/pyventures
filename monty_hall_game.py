import random


def get_user_input():
    while True:
        try:
            initial_choice = int(input("Choose a door (0, 1, or 2): "))
            if initial_choice in [0, 1, 2]:
                return initial_choice
            else:
                print("Invalid choice. Please enter 0, 1, or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def play_monty_hall(switch: bool) -> bool:
    doors = [0, 0, 0]
    car_position = random.randint(0, 2)
    doors[car_position] = 1
    print(doors)

    initial_choice = get_user_input()

    available_doors = [i for i in range(
        3) if i != initial_choice and doors[i] == 0]
    print(f"available_doors: {available_doors}")

    monty_opens = random.choice(available_doors)
    print(f"Monty opens door {monty_opens} showing a goat.")

    if switch:
        final_choice = next(i for i in range(3) if i !=
                            initial_choice and i != monty_opens)
    else:
        final_choice = initial_choice

    return doors[final_choice] == 1


def main():
    wins = 0
    trials = 0

    print("Welcome to the Monty Hall Game!\n")

    while True:
        choice = input(
            "Do you want to switch doors? (yes/no/quit): ").strip().lower()
        if choice == 'quit':
            break
        elif choice not in ('yes', 'no'):
            print("Please enter 'yes', 'no', or 'quit'.\n")
            continue

        switch = (choice == 'yes')
        result = play_monty_hall(switch)

        trials += 1
        if result:
            wins += 1
            print("🎉 You won the car!")
        else:
            print("🐐 You got a goat.")

        print(
            f"Current stats: {wins} wins out of {trials} trials ({(wins/trials)*100:.2f}% win rate)\n")

    print(f"\nFinal stats: {wins} wins in {trials} games.")
    print(f"Overall win rate: {(wins/trials)*100:.2f}%")
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
