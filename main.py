from connection import Connection
from downloader import Downloader


def run():
    (username, password) = get_credentials()
    connection = Connection(username, password)
    Downloader(connection)


def get_credentials() -> (str, str):
    username = input("Your login: ")
    password = input("WIS password: ")
    return username, password


if __name__ == '__main__':
    run()
