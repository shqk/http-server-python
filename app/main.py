import socket  # noqa: F401


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
    data = client_socket.recv(1024)
    request_line = data.split(b"\r\n")

    # Récupérer le chemin URL => deuxième élement d'une requête

    if data and len(request_line) > 1:
        url_path = data.split(b" ")[1]
        if url_path != b"/":
            client_socket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n", "utf-8"))


    if not data:
        response = client_socket.send(bytes("HTTP/1.1 404 Not Found\r\n\r\n", "utf-8"))

    # print("Data decoded: ", data.decode("utf-8", errors="replace"))
    print("Data: ", data)

    client_socket.send(bytes("HTTP/1.1 200 OK\r\n\r\n", "utf-8"))


if __name__ == "__main__":
    main()
