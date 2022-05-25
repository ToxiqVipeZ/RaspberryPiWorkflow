import socket

HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT"
SENDING_RFID = "C-S-RFID"
RECEIVING_RFID = "S-C-RFID"
ADD_TO_QUEUE = "RFID-QUEUE-ADD"
SAVE_TO_DATABASE = "saveData"
SERVER = "192.168.137.1"
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

    # if there are arguments to process
    if len(args) != 0:

        # encode the argument on pos 0
        args0 = args[0].encode(FORMAT)

        # save the length of the argument on pos 0
        args0_length = len(args0)

        # format the length of the argument into a send-able format
        send_length_args0 = str(args0_length).encode(FORMAT)
        send_length_args0 += b" " * (HEADER - len(send_length_args0))

    # setting and formatting the message length
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)

    # representing the message length in bytes, related to the header-size
    send_length += b" " * (HEADER - len(send_length))

    # if the received message equals SENDING_RFID
    print(msg)
    if msg == SENDING_RFID:

        # send the length of the message and the message itself afterwards
        client.send(send_length)
        client.send(message)

        # send the length of the message and the message itself afterwards
        client.send(send_length_args0)
        client.send(args0)

        # returning the next_station back to the application that called this client function
        next_station = client.recv(2048).decode(FORMAT)
        return next_station

    # if the received message equals ADD_TO_QUEUE
    if msg == ADD_TO_QUEUE:

        # send the length of the message and the message itself afterwards
        client.send(send_length)
        client.send(message)

        print(send_length_args0)
        print(args0)
        # send the length of the message and the message itself afterwards
        client.send(send_length_args0)
        client.send(args0)

    else:
        # sending the message length and the message itself afterwards (for any other messages)
        client.send(send_length)
        client.send(message)

    send(DISCONNECT_MESSAGE)
