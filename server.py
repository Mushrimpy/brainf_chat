import threading
import socket
from brainfuck.converter import TextBrainfuckConverter
import brainfuck.interpreter as interpreter

host = "127.0.0.1"
port = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
clients = []
aliases = []
converter = TextBrainfuckConverter()


def broadcast(message):
    for client in clients:
        client.send(message)


def brainfuck_io(input_string):
    # Pass data through the Brainfuck converter and interpreter.
    bf_code = converter.string_to_bf(input_string)
    result = interpreter.evaluate(bf_code)
    return result["output"]


def handle_client(client):
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            processed_message = brainfuck_io(message)
            broadcast(processed_message.encode("utf-8"))

        except Exception as e:
            # Handle client disconnect
            index = clients.index(client)
            clients.remove(client)
            client.close()
            alias = aliases[index]

            # Notify other clients
            disconnect_message = brainfuck_io(f"{alias} has left the chat room!")
            broadcast(disconnect_message.encode("utf-8"))

            aliases.remove(alias)
            break


def receive():
    print(brainfuck_io("Server is running and listening..."))

    while True:
        client, address = server.accept()

        # Notify of a new connection
        connection_message = brainfuck_io(f"Connection established with {str(address)}")
        print(connection_message)

        client.send(brainfuck_io("alias?").encode("utf-8"))
        alias = client.recv(1024).decode("utf-8")
        aliases.append(alias)
        clients.append(client)

        alias_message = brainfuck_io(f"The alias of this client is {alias}")
        print(alias_message)
        broadcast(
            brainfuck_io(f"{alias} has connected to the chat room").encode("utf-8")
        )
        client.send(brainfuck_io("You are now connected!").encode("utf-8"))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


if __name__ == "__main__":
    receive()
