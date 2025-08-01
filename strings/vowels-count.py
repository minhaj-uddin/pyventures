def count_vowels(text):
    """ Count the number of vowels in the given text. """
    vowels = set("aeiouAEIOU")
    return sum(1 for char in text if char in vowels)


def main():
    user_input = input("Enter a string: ").strip()

    if not user_input:
        print("Input cannot be empty.")
        return

    vowel_count = count_vowels(user_input)
    print(f"Number of vowels in the input: {vowel_count}")


if __name__ == "__main__":
    main()
