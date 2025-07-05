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


def extension_to_content_type(extension: str) -> str:
    if extension == ".txt":
        return "text/plain"
    elif extension == ".html":
        return "text/html"
    elif extension == ".jpg":
        return "image/jpeg"
    elif extension == ".gif":
        return "image/gif"
    else:
        return "unknown"


def construct_response(
    status_code: int,
    content_type: str | None = None,
    content_len: int | None = None,
    payload: bytes | None = None,
) -> bytes:
    if status_code == 200:
        resp = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\nContent-Length: {content_len}\r\bConnection: close\r\n\r\n".encode(
            "ISO-8859-1"
        )
        if payload:
            resp = resp + payload
        return resp
    elif status_code == 404:
        return "HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\nContent-Length: 13\r\bConnection: close\r\n\r\n404 not found".encode(
            "ISO-8859-1"
        )
    else:
        raise


def generate_home_html(files: list[str]) -> str:
    def generate_link(file: str) -> str:
        return f"<li><a href='{file}'>{file}</a></li>"

    return (
        """
    <!DOCTYPE html>
    <html>
    <body>
    
    <h1>Available Contents</h1>
    <ol>
    """
        + "\n".join([generate_link(f) for f in files])
        + """
    </ol>
    
    </body>
    </html>
    """
    )


def run_server():
    listen_sock = socket.socket()

    # Magic line:
    # This will prevent an “Address already in use” error on the bind() in certain circumstances.
    listen_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    listen_sock.bind(("", 28333))
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

        # Feature: list all files in the data directory
        if header_object.request_target == "/":
            files = os.listdir("data")
            payload = generate_home_html(files).encode("ISO-8859-1")
            status = 200
            content_type = extension_to_content_type(".html")

        # Serve requested files as response
        else:
            file_path = os.path.normpath(
                os.path.join("data", header_object.request_target.lstrip("/"))
            )
            print(f"request target is {header_object.request_target}")
            print(f"file path is {file_path}")
            file_extension = os.path.splitext(file_path)[1]
            content_type = extension_to_content_type(file_extension)

            # read file data, which will be the payload in response.
            payload = b""
            try:
                with open(file_path, "rb") as fp:
                    payload = fp.read()
                    status = 200
            except FileNotFoundError:
                status = 404

        server_response = construct_response(
            status, content_type, content_len=len(payload), payload=payload
        )

        new_socket.send(server_response)
        new_socket.close()


if __name__ == "__main__":
    run_server()
