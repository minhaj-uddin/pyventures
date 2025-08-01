import random


def generate_card_number(length=16):
    # Generate all digits except the last (check digit)
    number = [random.randint(0, 9) for _ in range(length - 1)]
    print(number)

    # Compute check digit
    def calculate_check_digit(digits):
        total = 0

        # Reverse for Luhn processing
        for i in range(len(digits) - 1, -1, -1):
            digit = digits[i]
            if (len(digits) - i) % 2 == 1:
                digit *= 2
                if digit > 9:
                    digit -= 9
            total += digit
        check_digit = (10 - (total % 10)) % 10
        return check_digit

    check_digit = calculate_check_digit(number)
    number.append(check_digit)
    return ''.join(map(str, number))


print("Generated valid Luhn number:", generate_card_number())
