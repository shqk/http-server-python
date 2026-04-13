import socket  # noqa: F401
import re
import threading

def handle_client(client_socket : socket.socket) -> None:
    status_line = b"HTTP/1.1 404 Not Found\r\n"
    request_headers_list = []
    request_headers = {}
    method = b""
    url_path = b""
    version = b""
    request_line = b''
    response_headers = b''
    response_body = b''

    if (data := client_socket.recv(1024)) and (b"\r\n\r\n" in data):
        request_line_headers, body = data.split(b"\r\n\r\n", maxsplit=1)

        print("request_line_headers: ", request_line_headers)
        print("Body: ", body)


        if request_line_headers:
            request_line, *request_headers_list = request_line_headers.split(b"\r\n")

        print("Only request line: ", request_line)
        print("Only headers: ", request_headers_list)


    if request_line:
    
        request_line_splitted = request_line.split(b" ")

        if request_headers_list:
            # Utilisation du max_split pour split au premier ":"
            for header in request_headers_list:
                if b":" in header:
                    k, v = header.split(b':', maxsplit=1)
                    request_headers[k.lower()] = v.strip()
        print("Headers dictionnary: ", request_headers)

        if len(request_line_splitted) == 3:
            method, url_path, version = request_line_splitted
        
        if method != b"GET":
            pass

        else:
            if url_path == b"/":
                status_line = b"HTTP/1.1 200 OK"
                response_headers = b''
                response_body = b''

            elif url_path == b"/user-agent":
                if request_headers.get(b"user-agent"):
                    status_line = b"HTTP/1.1 200 OK"
                    response_headers = b"Content-Type: text/plain\r\n" + b"Content-Length: " + str(len(request_headers.get(b"user-agent"))).encode("ascii") + b"\r\n"
                    response_body = request_headers.get(b"user-agent")


            elif url_path.startswith(b"/echo/"):
                status_line = b"HTTP/1.1 200 OK"
                to_echo = url_path[len(b"/echo/"):]
                response_headers = b"Content-Type: text/plain\r\n" + b"Content-Length: " + str(len(to_echo)).encode("ascii") + b"\r\n"
                response_body = to_echo
            
        response = status_line + b"\r\n" + response_headers + b"\r\n" + response_body
        client_socket.sendall(response)


def main():

    # server_socket écoute les demandes de connexions entrantes (une sorte de réceptionniste)
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    # Ici le serveur accepte la connexion et alloue un canal dédié avec .accept stocké dans le socket_client
    # (avec par lequel la communication va s'effectuer ; lien entre le socket du navigateur et un socket créé par le serveur en conséquence pour communiquer)
    while True:
        client_socket, client_adress = server_socket.accept()  # wait for client
        print("Client address: ", client_adress)
        threading.Thread(target=handle_client, args=(client_socket,)).start()





if __name__ == "__main__":
    main()
