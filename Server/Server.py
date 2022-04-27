import socket
import threading

from Database import stationSwapper


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
    """
    Executes after a client has connected
    :param conn: connect & data information
    :param addr: address information
    """

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

            # starting receive_rfid mode
            if msg == RECEIVING_RFID:
                receive_rfid = True

            # if in receive rfid mode
            if receive_rfid is True:

                # excluding the first message, so that only the arguments in args join into this section
                if msg != RECEIVING_RFID:

                    # splitting the received information
                    station = msg[:2]
                    workflow_procedure = msg[2:5]

                    # passing the information to the stationSwapper, which gives back the next statin
                    next_station = stationSwapper.main(workflow_procedure, station)

                    # sending the next station back to the client
                    conn.send(next_station.encode(FORMAT))

                    # exiting the rfid mode
                    receive_rfid = False

            # killing the thread (stopping the connection) when the message from the client is the DISCONNECT_MESSAGE
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"From client: {addr}, received message: {msg}")

    conn.close()


def start():
    """
    starting the server
    """
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
