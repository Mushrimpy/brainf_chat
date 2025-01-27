import threading
import socket
from utils import brainfuck_io


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "127.0.0.1"
port = 8080

client.connect((host, port))

alias_message = brainfuck_io("Choose an alias:")
print(alias_message, end=" ")
alias = input()


def client_receive():
    while True:
        try:
            message = client.recv(1024).decode("utf-8")
            if message == "alias?":
                client.send(alias.encode("utf-8"))
            else:
                print(message)
        except:
            error_message = brainfuck_io("Error!")
            print(error_message)
            client.close()
            break


def client_send():
    while True:
        message = f'{alias}: {input("")}'
        client.send(message.encode("utf-8"))


if __name__ == "__main__":
    receive_thread = threading.Thread(target=client_receive)
    receive_thread.start()

    send_thread = threading.Thread(target=client_send)
    send_thread.start()
