def count_characters(text):
    """ Count the frequency of each character in the given text. """
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    return frequency


def main():
    user_input = input("Enter a string: ").strip()

    if not user_input:
        print("Input cannot be empty.")
        return

    frequencies = count_characters(user_input)

    print("Character frequencies:")
    for char, count in frequencies.items():
        print(f"'{char}': {count}")


if __name__ == "__main__":
    main()
