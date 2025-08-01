def even_odd_numbers(n):
    if n % 2 == 0:
        print(f"{n} is an even number.")
    else:
        print(f"{n} is an odd number.")


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
    even_odd_numbers(input_number)


if __name__ == '__main__':
    main()
