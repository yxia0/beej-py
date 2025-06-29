import os.path
import socket
from dataclasses import dataclass

@dataclass
class HTTPRequestHeader:
    request_type: str
    request_target: str
    host: str



def parse_request_header(raw_header: str) -> HTTPRequestHeader:
    header_by_line = raw_header.split("\r\n")
    request_type, request_target, http_version = header_by_line[0].split(" ")
    host = header_by_line[1].split("Host: ")[1]
    return HTTPRequestHeader(request_type, request_target, host)

def run_server():
    listen_sock = socket.socket()

    # Magic line:
    # This will prevent an “Address already in use” error on the bind() in certain circumstances.
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    listen_sock.bind(('', 28333))
    listen_sock.listen()

    while True:
        new_conn = listen_sock.accept()
        new_socket = new_conn[0]

        full_request_header = ""
        while True:
            # recv will return an empty string only when the client closes its
            # connection; but the client will be waiting for the response, so
            # it will not close the connection!! so empty string never gets returned
            # unless the client crashes or something.
            request_bytes = new_socket.recv(1024)
            request_str = request_bytes.decode("ISO-8859-1")

            if "\r\n\r\n" in request_str:
                remaining_header, request_body = request_str.split("\r\n\r\n")
                full_request_header += remaining_header
                break
            else:
                full_request_header += request_str

        header_object = parse_request_header(full_request_header)

        file_path = os.path.normpath(os.path.join("data", header_object.request_target))
        file_type = os.path.splitext(file_path)[1]
        














if __name__ == "__main__":



        response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: 6\r\nConnection: close\r\n\r\nHello!"
        response_bytes = response.encode("ISO-8859-1")

        new_socket.sendall(response_bytes)
        new_socket.close()
        print(f"Response sent: Connection closed!")









