#!/usr/bin/env python3

from socket import AF_INET, SOCK_DGRAM, socket

def main() -> None:
    ip      = "127.0.0.1"
    port    = 5000
    
    message = b"This is some text"

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.sendto(message, (ip, port))

if __name__ == '__main__':
    main()