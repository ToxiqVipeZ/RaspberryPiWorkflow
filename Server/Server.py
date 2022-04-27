import socket
import threading

from Database import insertRecord


HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT"
RECEIVING_RFID = "C-S-RFID"
SENDING_RFID = "S-C-RFID"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
receive_rfid = False


def handle_client(conn, addr):
    print(f"[NEW CONNETION] {addr} connected \n")
    # waiting for client-data, gets executed after a message is received:
    connected = True
    while connected:
        # msg_length receives information about the data length (HEADER) and decodes it as (FORMAT)
        msg_length = conn.recv(HEADER).decode(FORMAT)

        if msg_length:
            msg_length = int(msg_length)

            # msg receives the message with size (msg_length) and decodes it as (FORMAT)
            msg = conn.recv(msg_length).decode(FORMAT)

            if msg == RECEIVING_RFID:
                receive_rfid = True

            if receive_rfid is True:
                if msg != RECEIVING_RFID:

                    ############# HIER CODE AN DATENBANK ###############
                    station = msg[:2]
                    workflow_procedure = msg[2:5]

                    print(workflow_procedure)
                    print(station)

                    insertRecord.main(workflow_procedure, station)
                    receive_rfid = False


            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}]{msg}")

    conn.close()


def start():

    server.listen()
    print(f"Waiting for a client to connect to {SERVER} \n")
    # waiting for a client to establish a connection:
    while True:

        # server.accept() gets client address information into conn, addr
        conn, addr = server.accept()

        # starting a new thread to run the connection parallel
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

        print(f" Aktive Verbindungen: {threading.active_count() - 1} \n")

print("Server startet ...")
start()
