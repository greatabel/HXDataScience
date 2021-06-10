import socket
import os
from threading import Thread
import multiprocessing
import subprocess
import time


def open_client(x=""):
    try:
        os.system(
            "gnome-terminal -e 'bash -c \"workon samaritan0; sqoop version;\"'"
            .format(x))
        print('# test bash', '#'*20)
        time.sleep(3)
        os.system(
            "gnome-terminal -e 'bash -c \"source samaritan0; sqoop version;\"'"
            .format(x))
    except OSError:
        print("Can't open {}.py".format(x))


def main():
    open_client("")

if __name__ == "__main__":
    main()


