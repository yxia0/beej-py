import socket


if __name__ == "__main__":

    listen_sock = socket.socket()

    # Magic line:
    # This will prevent an “Address already in use” error on the bind() in certain circumstances.
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    listen_sock.bind(('', 28333))
    listen_sock.listen()

    while True:
        new_conn = listen_sock.accept()
        new_socket = new_conn[0]


        full_request = ""
        while True:
            # recv will return empty string only when the client closes its
            # connection; but the client will be waiting for the response, so
            # it will not close the connection!! so empty string never gets returned
            # unless the client crashes or something.
            request_bytes = new_socket.recv(1024)
            request_str = request_bytes.decode("ISO-8859-1")
            full_request += request_str

            if "\r\n\r\n" in request_str:
                break

        print(f"Received request: \n{full_request}\n")

        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 6\r\nConnection: close\r\n\r\nHello!"
        response_bytes = response.encode("ISO-8859-1")

        new_socket.sendall(response_bytes)
        new_socket.close()
        print(f"Response sent: Connection closed!")









