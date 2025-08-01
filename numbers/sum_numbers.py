def sum_numbers(n):
    total = 0
    for i in range(1, n+1):
        total += i
    return total


def get_user_input():
    while True:
        try:
            input_number = int(input("Please enter a positive number: "))
            if input_number < 0:
                print("Number not valid, it must be non-zero integer.")
            else:
                return input_number
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def main():
    input_number = get_user_input()
    total = sum_numbers(input_number)
    print(f"Total sum of numbers: {total}")


if __name__ == '__main__':
    main()
