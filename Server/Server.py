import socket
import threading

from Database import StationSwapper

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT"
RECEIVING_RFID = "C-S-RFID"
SENDING_RFID = "S-C-RFID"
QUEUE_REQUEST = "QUEUE-REQUEST"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


class Server:
    receive_rfid_mode = False
    add_to_queue_mode = False

    def add_to_queue(self, production_number):
        print("Versuche Produktionsnummer: " + production_number + " zur Warteschlange hinzuzufügen.")


    @staticmethod
    def switch_station(msg):
        # splitting the received information
        station = msg[:2]
        workflow_procedure = msg[2:5]
        variation = msg[5:]

        # passing the information to the stationSwapper, which gives back the next statin
        next_station = StationSwapper.main(workflow_procedure, station, variation)

        # sending the next station back to the client
        return next_station.encode(FORMAT)

    def handle_client(self, conn, addr):
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

            # if the received message got a length
            if msg_length:
                msg_length = int(msg_length)

                # msg receives the message with size (msg_length) and decodes it as (FORMAT)
                msg = conn.recv(msg_length).decode(FORMAT)

                # starting receive_rfid_mode
                if msg == RECEIVING_RFID:
                    self.receive_rfid_mode = True
                # if in receive rfid mode
                if self.receive_rfid_mode is True:
                    # excluding the first message, so that only the arguments in args join into this section
                    if msg != RECEIVING_RFID:
                        conn.send(self.switch_station(msg))
                        # exiting the receive_rfid_mode
                        self.receive_rfid_mode = False

                # starting add_to_queue_mode
                if msg == QUEUE_REQUEST:
                    self.add_to_queue_mode = True
                if self.add_to_queue_mode is True:
                    if msg != QUEUE_REQUEST:
                        self.add_to_queue(msg)
                        self.add_to_queue_mode = False

                # killing the thread when the message from the client equals the DISCONNECT_MESSAGE
                if msg == DISCONNECT_MESSAGE:
                    conn.close()
                    connected = False

                print(f"From client: {addr}, received message: {msg}")

        conn.close()

    def main(self):
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
            thread = threading.Thread(target=self.handle_client, args=(conn, addr))
            thread.start()

            print(f" Aktive Verbindungen: {threading.active_count() - 1} \n")

    print("Server startet ...")


Server().main()
