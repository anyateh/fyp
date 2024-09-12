#!/usr/bin/env python3

from socket import AF_INET, SOCK_DGRAM, socket

def main() -> None:
    # I have a Linux system named "emily", don't judge!
    ip      = "emily.local"
    port    = 5000

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.bind((ip, port))

    while True:
        data, addr = sock.recvfrom(1024)
        print("Received message:")
        print(data)

if __name__ == '__main__':
    main()