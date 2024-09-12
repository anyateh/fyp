#!/usr/bin/env python3

from socket import AF_INET, SOCK_DGRAM, socket

def main() -> None:
    # I have a Linux system named "emily", don't judge!
    ip      = "emily.local"
    port    = 5000
    
    message = b"Hi Emily! Here is some cake."

    sock = socket(AF_INET, SOCK_DGRAM)
    sock.sendto(message, (ip, port))

if __name__ == '__main__':
    main()