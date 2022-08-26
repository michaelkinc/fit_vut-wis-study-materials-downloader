from connection import Connection
from downloader import Downloader
from termcolor import colored
import sys
import getopt


def run():
    path = parse_args()
    (username, password) = get_credentials()
    connection = Connection(username, password)
    downloader = Downloader(connection, path)
    downloader.download()


def get_credentials() -> (str, str):
    username = input(colored("Your login: ", "yellow"))
    password = input(colored("WIS password: ", "yellow"))
    print("-----------------------------------------------------------")
    return username, password


def parse_args():
    argv = sys.argv[1:]
    opts, args = getopt.getopt(argv, "p:")
    path = None
    for opt, arg in opts:
        if opt in ['-p']:
            path = arg
    return path


if __name__ == '__main__':
    run()
