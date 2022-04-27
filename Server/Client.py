import socket

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT"
SENDING_RFID = "C-S-RFID"
RECEIVING_RFID = "S-C-RFID"
SERVER = "172.29.167.85"
ADDR = (SERVER, PORT)

# set the clients-socket, establish connection to server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg, *args):
    """
    the method to send messages to the server
    :param msg: the message that gets send to the server
    """
    # formatting the message
    message = msg.encode(FORMAT)
    print(args)
    if len(args) != 0:
        args0 = args[0].encode(FORMAT)
        args0_length = len(args0)
        send_length_args0 = str(args0_length).encode(FORMAT)
        send_length_args0 += b" " * (HEADER - len(send_length_args0))
    # setting and formatting the message length
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    # representing the message length in bytes, related to the header-size
    send_length += b" " * (HEADER - len(send_length))

    if msg == SENDING_RFID:
        client.send(send_length)
        client.send(message)
        client.send(send_length_args0)
        client.send(args0)
        next_station = client.recv(2048).decode(FORMAT)
        return next_station
    else:
        # sending the message length and the message itself afterwards
        client.send(send_length)
        client.send(message)

    send(DISCONNECT_MESSAGE)
