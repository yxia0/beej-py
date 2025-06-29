"""A simple HTTP Client."""

import socket
import sys


def http_get(address: str, port: str) -> str:
    # construct minimum GET HTTP message
    request = f"GET / HTTP/1.1\r\nHost: {address}\r\nConnection: close\r\n\r\n"
    request_in_bytes = request.encode("ISO-8859-1")

    # ask os for a socket, this will be our connection,
    # but it is not connected to anything yet
    sock = socket.socket()

    sock.connect((address, int(port)))
    sock.sendall(request_in_bytes)

    resp_str = ""
    # Loop until we receive all response data
    while True:
        d = sock.recv(1024)  # 1KB
        if len(d) == 0:
            # no more response data to read!
            break

        else:
            # decode response
            resp_str += d.decode("ISO-8859-1")

    sock.close()
    return resp_str


if __name__ == "__main__":
    target_address = sys.argv[1]
    target_port = sys.argv[2]
    if target_port:
        if not target_port.isdigit():
            raise ValueError("Port value is invalid!")
    else:
        target_port = "80"

    response = http_get(target_address, target_port)
    print(response)
