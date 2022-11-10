import subprocess
from typing import Generator


def tail(filename: str) -> Generator[str, None, None]:
    proc = subprocess.Popen(
        ["tail", "-F", "-n", "+1", filename], stdout=subprocess.PIPE
    )
    while True:
        line = proc.stdout.readline()
        if line:
            yield line.decode("utf-8")
        else:
            break
