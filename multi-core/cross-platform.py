import os
import psutil
import platform
from multiprocessing import Pool


def square(n):
    pid = os.getpid()
    system = platform.system()

    if system == 'Linux':
        try:
            core = os.sched_getcpu()
            print(f"[{system}] Processing {n} on CPU core {core} (PID: {pid})")
        except AttributeError:
            print(f"[{system}] os.sched_getcpu() not available (PID: {pid})")
    elif system == 'Windows' or system == 'Darwin':
        if psutil:
            p = psutil.Process(pid)
            affinity = p.cpu_affinity()
            print(
                f"[{system}] Processing {n} (PID: {pid}) allowed on cores: {affinity}")
        else:
            print(
                f"[{system}] psutil not installed, cannot check core affinity (PID: {pid})")
    else:
        print(f"[Unknown OS] Processing {n} (PID: {pid})")

    return n * n


if __name__ == '__main__':
    numbers = [1, 2, 3, 4, 5]

    with Pool(processes=4) as pool:
        results = pool.map(square, numbers)

    print("Squared Results:", results)
