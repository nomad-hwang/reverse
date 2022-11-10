import logging
import subprocess
import time
from bastion.util.cmd import cmd

from bastion.util.tail import tail


def main():
    ret = subprocess.run("lsof -i -n", capture_output=True, shell=True)
    print('lsof -n', ret)
    ret = subprocess.run(["ls", "-al"], capture_output=True)
        
    # for line in tail("/config/logs/openssh/current"):
    #     print(line.strip())

    while True:
        print("Hello World")
        time.sleep(1)

    # debug1: Allocated listen port

    # Accepted password for testuser from 192.168.48.1 port 44088 ssh2
    # Accepted publickey for testuser from

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s | %(levelname)-8s | %(message)s"
    )
    main()
