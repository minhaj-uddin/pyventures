def are_anagrams(str1, str2):
    """ Check if two strings are anagrams of each other. """
    def clean_string(s):
        return sorted([char.lower() for char in s if char.isalnum()])

    return clean_string(str1) == clean_string(str2)


def main():
    s1 = input("Enter the first string: ").strip()
    s2 = input("Enter the second string: ").strip()

    if not s1 or not s2:
        print("Both strings must be non-empty.")
        return

    if are_anagrams(s1, s2):
        print("The strings are anagrams.")
    else:
        print("The strings are not anagrams.")


if __name__ == "__main__":
    main()
