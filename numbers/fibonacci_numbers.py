def fibonacci_sequence(n):
    a, b = 0, 1
    fib_sequence = []
    for _ in range(n):
        fib_sequence.append(a)
        a, b = b, a + b
    return fib_sequence


try:
    input_number = int(input("Please enter a positive number: "))
    if input_number < 0:
        print("Number not valid.")
    else:
        sequence = fibonacci_sequence(input_number)
        for number in sequence:
            print(f"fibonacci_number: {number}")
except ValueError:
    print("Invalid input. Please enter a valid integer.")
