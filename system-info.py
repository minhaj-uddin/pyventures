import psutil
import platform
from datetime import datetime


def format_bytes(bytes_num: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:.2f} {unit}"
        bytes_num /= 1024.0
    return f"{bytes_num:.2f} PB"


def get_system_info() -> None:
    print("=== System Information ===")
    print(f"Platform       : {platform.system()} {platform.release()}")
    print(f"Architecture   : {platform.machine()}")
    print(
        f"CPU Cores      : {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count()} logical")
    print(f"CPU Usage      : {psutil.cpu_percent(interval=1)}%")
    print(
        f"Memory         : {format_bytes(psutil.virtual_memory().used)} used / {format_bytes(psutil.virtual_memory().total)} total")
    print(
        f"Disk Usage     : {format_bytes(psutil.disk_usage('/').used)} used / {format_bytes(psutil.disk_usage('/').total)} total")
    print(
        f"Boot Time      : {datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')}")
    print()


def get_top_processes(limit: int = 5) -> None:
    print(f"=== Top {limit} Processes by Memory Usage ===")
    processes = []

    for proc in psutil.process_iter(['pid', 'name', 'username', 'memory_info', 'cpu_percent']):
        try:
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Sort by memory usage
    processes = sorted(
        processes, key=lambda p: p['memory_info'].rss, reverse=True)

    for proc in processes[:limit]:
        mem_usage = format_bytes(proc['memory_info'].rss)
        print(f"PID: {proc['pid']:<6} Name: {proc['name'][:20]:<20} "
              f"User: {proc['username'][:15]:<15} "
              f"Memory: {mem_usage:<10} CPU: {proc['cpu_percent']}%")
    print()


def main() -> None:
    get_system_info()
    get_top_processes()


if __name__ == '__main__':
    main()
