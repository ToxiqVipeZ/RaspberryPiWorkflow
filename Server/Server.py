import socket
import threading

import StationSwapper
from ServerHandler import ServerHandler

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT"
TRACKING_STATS_IN = "TRACKING-STATS-IN"
TRACKING_STATS_OUT = "TRACKING-STATS-OUT"
RECEIVING_RFID = "C-S-RFID"
SENDING_RFID = "S-C-RFID"
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


class Server:
    receive_rfid_mode = False
    receive_stats_mode = False
    message_queue = [0, 1]
    message_queue_counter = 0
    receive_status = ""

    def add_to_queue(self, production_number):
        print("Versuche Produktionsnummer: " + production_number + " zur Warteschlange hinzuzufügen.")

    @staticmethod
    def switch_station(msg):
        # splitting the received information
        station = msg[:2]
        workflow_procedure = msg[2:5]
        variation = msg[5:]

        # passing the information to the stationSwapper, which gives back the next station
        next_station = StationSwapper.main(workflow_procedure, station, variation)

        # sending the next station back to the client
        return next_station.encode(FORMAT)

    def track_stats(self, message_queue, received_status):
        rfid = message_queue[0]
        station = message_queue[1]

        if received_status == "IN":
            ServerHandler().station_in(rfid, station)
        elif received_status == "OUT":
            ServerHandler().station_out(rfid, station)


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

                # starting receive_stats_mode
                if msg == TRACKING_STATS_IN:
                    self.receive_stats_mode = True
                    self.receive_status = "IN"
                elif msg == TRACKING_STATS_OUT:
                    self.receive_stats_mode = True
                    self.receive_status = "OUT"
                # if in receive_stats_mode
                if self.receive_stats_mode is True:
                    # excluding the first message, so that only the arguments in args join into this section
                    if msg != TRACKING_STATS_IN and msg != TRACKING_STATS_OUT:
                        message_queue_counter = 0
                        self.message_queue[message_queue_counter] = msg
                        message_queue_counter += 1
                        # exiting the receive_stats_mode
                        if message_queue_counter == 2:
                            self.track_stats(self.message_queue, self.receive_status)
                            self.message_queue = [0, 1]
                            message_queue_counter = 0
                            self.receive_status = ""
                            self.receive_stats_mode = False

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
