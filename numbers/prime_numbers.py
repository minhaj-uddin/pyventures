def get_user_input():
    while True:
        try:
            num = int(input("Enter a positive integer: "))
            if num <= 0:
                print("Please enter a number greater than 0.")
            else:
                return num
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def is_prime(n):
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True


def get_primes_up_to(limit):
    return [num for num in range(2, limit + 1) if is_prime(num)]


def main():
    number = get_user_input()
    primes = get_primes_up_to(number)
    print(f"Prime numbers up to {number}:")
    print(primes)


if __name__ == '__main__':
    main()
