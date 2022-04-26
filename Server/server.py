import socket
import threading

PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNETION] {addr} connected")

    # waiting for client-data, gets executed after a message is received:
    connected = True
    while connected:
        msg = conn.recv()


def start():

    server.listen()

    # waiting for a client to establish a connection:
    while True:

        # server.accept() gets client address information into conn, addr
        conn, addr = server.accept()

        # starting a new thread to run the connection parallel
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f" Aktive Verbindungen: {threading.active_count() - 1}")

print("Server startet ...")
start()
