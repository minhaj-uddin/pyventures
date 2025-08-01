def compute_gcd(a: int, b: int) -> int:
    """Compute the Greatest Common Divisor using the Euclidean algorithm."""
    while b != 0:
        a, b = b, a % b
    return abs(a)


def find_lcm(a: int, b: int) -> int:
    """Return the Least Common Multiple of two integers."""
    if a == 0 or b == 0:
        raise ValueError("LCM is not defined for zero.")
    return abs(a * b) // compute_gcd(a, b)


def main():
    try:
        num1 = int(input("Enter the first number: "))
        num2 = int(input("Enter the second number: "))
        lcm = find_lcm(num1, num2)
        print(f"The LCM of {num1} and {num2} is {lcm}.")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
