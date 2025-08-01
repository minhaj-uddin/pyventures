import num2words as n2w


def get_number():
    while True:
        try:
            number = float(input('Enter the number: '))
            return number
        except ValueError:
            print('Invalid amount')


def main():
    number_in_digits = get_number()
    number_in_words = n2w.num2words(number_in_digits)
    print(str(number_in_words).capitalize())


if __name__ == "__main__":
    main()
