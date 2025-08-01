def validate_card_number(card_number):
    digits = [int(d) for d in str(card_number)]
    checksum = 0

    for i in range(len(digits) - 1, -1, -1):
        digit = digits[i]
        if (len(digits) - i) % 2 == 0:
            digit *= 2
            if digit > 9:
                digit -= 9
        checksum += digit

    return checksum % 10 == 0


def main():
    card_number = "4539148803436467"
    validate_result = validate_card_number(card_number)
    print(f"Card number {card_number} is valid: {validate_result}")


if __name__ == "__main__":
    main()
