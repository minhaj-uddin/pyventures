import time
from multiprocessing import Pool, cpu_count


def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


def main():
    print(cpu_count())
    numbers = [35, 36, 37]
    start = time.time()

    with Pool(processes=cpu_count()) as pool:
        results = pool.map(fibonacci, numbers)

    for n, result in zip(numbers, results):
        print(f"Fibonacci({n}) = {result}")

    print(f"✅ Done in {time.time() - start:.2f} seconds.")


if __name__ == '__main__':
    main()
