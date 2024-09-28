#!/usr/bin/env python3

from socket import AF_INET, SOCK_STREAM, socket

def main() -> None:
    # I have a Linux system named "emily", don't judge!
    ip      = "emily.local"
    port    = 5000

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind((ip, port))
    sock.listen(1)
    connection, addr = sock.accept()

    while True:
        data = connection.recv(1024)
        print("Received message:")
        print(data)
        if data:
            break

if __name__ == '__main__':
    main()
