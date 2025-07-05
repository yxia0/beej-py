import socket

import time


# copied from https://beej.us/guide/bgnet0/html/split/project-atomic-time.html.
def system_seconds_since_1900():
    """
    The time server returns the number of seconds since 1900, but Unix
    systems return the number of seconds since 1970. This function
    computes the number of seconds since 1900 on the system.
    """

    # Number of seconds between 1900-01-01 and 1970-01-01
    seconds_delta = 2208988800

    seconds_since_unix_epoch = int(time.time())
    seconds_since_1900_epoch = seconds_since_unix_epoch + seconds_delta

    return seconds_since_1900_epoch


def main():
    # connect to time.nist.gov on port 37
    my_socket = socket.socket()
    address_name = "time-a-b.nist.gov"
    ip_address = socket.gethostbyname(address_name)
    print(f"Connecting to {address_name}@{ip_address}")
    my_socket.connect((ip_address, 37))

    data = my_socket.recv(4)
    print(f"{data}")
    nist_time = int.from_bytes(data, "big")
    my_computer_time = system_seconds_since_1900()
    print(f"NIST time  : {nist_time}")
    print(f"System time  : {my_computer_time}")
    my_socket.close()


if __name__ == "__main__":
    main()
