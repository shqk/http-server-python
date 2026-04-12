import socket  # noqa: F401
import re


def main():

    # server_socket écoute les demandes de connexions entrantes (une sorte de réceptionniste)
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)

    # Ici le serveur accepte la connexion et alloue un canal dédié avec .accept stocké dans le socket_client
    # (avec par lequel la communication va s'effectuer ; lien entre le socket du navigateur et un socket créé par le serveur en conséquence pour communiquer)
    client_socket, client_adress = server_socket.accept()  # wait for client

    print("Server socket: ", server_socket)
    print("Client socket: ", client_socket)
    print("Client address: ", client_adress)

    # Server Response Status 200 OK
    # client_socket.send(bytes("HTTP/1.1 200 OK\r\n\r\n", "utf-8"))

    # Extract URL path

    if (data := client_socket.recv(1024)) and (b"\r\n\r\n" in data):
        request_line_headers, body = data.split(b"\r\n\r\n", maxsplit=1)

        print("request_line_headers: ", request_line_headers)
        print("Body: ", body)

        request_line = b''

        if request_line_headers:
            request_line, *headers = request_line_headers.split(b"\r\n")

        print("Only request line: ", request_line)
        print("Only headers: ",headers)

    # Récupérer le chemin URL => deuxième élement d'une requête

    if request_line:
    
        request_line_splitted = request_line.split(b" ")
        headers_dic = {} 

        if headers:
            # Utilisation du max_split pour split au premier ":"
            for header in headers:
                k, v = header.split(b':', maxsplit=1)
                headers_dic[k.lower()] = v.strip()
        print("Headers dictionnary: ", headers_dic)

        if len(request_line_splitted) == 3:
            method, url_path, version = request_line_splitted
        
            if url_path == b"/":
                client_socket.send(bytes("HTTP/1.1 200 OK\r\n\r\n", "utf-8"))

            elif url_path == b"/user-agent":
                if headers_dic[b"user-agent"]:
                    client_socket.send(bytes(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(headers_dic[b"user-agent"])}\r\n\r\n{headers_dic[b"user-agent"].decode("utf-8")}", "utf-8"))

            elif url_path.startswith(b"/echo/"):
                to_echo = url_path[len(b"/echo/"):]
                client_socket.send(bytes(f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: {len(to_echo)}\r\n\r\n{to_echo.decode("utf-8")}", "utf-8"))
            
            else:
                client_socket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n", "utf-8"))


    if not data:
        response = client_socket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n", "utf-8"))

    client_socket.send(bytes("HTTP/1.1 200 OK\r\n\r\n", "utf-8"))


if __name__ == "__main__":
    main()
