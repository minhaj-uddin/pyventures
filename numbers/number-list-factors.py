def get_factors(number):
    """Return a list of factors of the given number."""
    if number < 1:
        raise ValueError("Number must be a positive integer.")
    return [i for i in range(1, number + 1) if number % i == 0]


def main():
    try:
        num = int(input("Enter a positive integer: "))
        factors = get_factors(num)
        print(f"Factors of {num}: {factors}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
