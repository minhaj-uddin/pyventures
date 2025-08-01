def to_binary(n: int) -> str:
    """Convert a decimal number to binary representation."""
    if n == 0:
        return '0'
    result = ''
    while n > 0:
        result = str(n % 2) + result
        n //= 2
    return result


def to_octal(n: int) -> str:
    """Convert a decimal number to octal representation."""
    if n == 0:
        return '0'
    result = ''
    while n > 0:
        result = str(n % 8) + result
        n //= 8
    return result


def to_hexa(n: int) -> str:
    """Convert a decimal number to hexadecimal representation."""
    if n == 0:
        return '0'
    hex_digits = '0123456789ABCDEF'
    result = ''
    while n > 0:
        result = hex_digits[n % 16] + result
        n //= 16
    return result


def main():
    try:
        number = int(input("Enter a decimal number: "))
        if number < 0:
            raise ValueError("Only non-negative integers are supported.")
        print(f"Binary: {to_binary(number)}")
        print(f"Octal:  {to_octal(number)}")
        print(f"Hexa:   {to_hexa(number)}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
