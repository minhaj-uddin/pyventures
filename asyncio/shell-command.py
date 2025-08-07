import asyncio
import platform


async def run_shell_command():
    # Cross-platform shell command
    command = "dir" if platform.system() == "Windows" else "ls -l"

    # Run the command in the shell
    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    stdout, stderr = await process.communicate()

    if stdout:
        print("[STDOUT]")
        print(stdout.decode().strip())

    if stderr:
        print("[STDERR]")
        print(stderr.decode().strip())

    print(f"\nCommand exited with return code: {process.returncode}")


async def main():
    await run_shell_command()

if __name__ == "__main__":
    asyncio.run(main())
