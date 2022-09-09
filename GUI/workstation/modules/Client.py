try:
    import socket
except ImportError:
    print("[Client.py] socket import failed.")

try:
    import time
except ImportError:
    print("[Client.py] time import failed.")
    
    
HEADER = 64
PORT = 5050
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "DISCONNECT"
TRACKING_STATS_IN = "TRACKING-STATS-IN"
TRACKING_STATS_OUT = "TRACKING-STATS-OUT"
GET_ERROR_LIST = "GET-ERROR-LIST"
SENDING_RFID = "C-S-RFID"
RECEIVING_RFID = "S-C-RFID"
TRACKING_ERROR_IN = "TRACKING-ERROR-IN"
TRACKING_ERROR_OUT = "TRACKING-ERROR-OUT"
ADD_TO_QUEUE = "RFID-QUEUE-ADD"
SAVE_TO_DATABASE = "saveData"
#SERVER = "169.254.0.102"
SERVER = socket.gethostbyname(socket.gethostname())
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

    # setting and formatting the message length
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)

    # representing the message length in bytes, related to the header-size
    send_length += b" " * (HEADER - len(send_length))

    # if there are arguments to process
    if msg == SENDING_RFID:
    #if len(args) != 0:
        # encode the argument on pos 0
        args0 = args[0].encode(FORMAT)

        # save the length of the argument on pos 0
        args0_length = len(args0)

        # format the length of the argument into a send-able format
        send_length_args0 = str(args0_length).encode(FORMAT)
        send_length_args0 += b" " * (HEADER - len(send_length_args0))

        # send the length of the message and the message itself afterwards
        client.send(send_length)
        client.send(message)

        # send the length of the message and the message itself afterwards
        client.send(send_length_args0)
        client.send(args0)

        # returning the next_station back to the application that called this client function
        next_station = client.recv(2048).decode(FORMAT)
        return next_station

    elif msg == TRACKING_STATS_IN or msg == TRACKING_STATS_OUT or msg == TRACKING_ERROR_IN or msg == TRACKING_ERROR_OUT:
        # encode the argument on pos 0
        args0 = args[0].encode(FORMAT)

        # save the length of the argument on pos 0
        args0_length = len(args0)

        # format the length of the argument into a send-able format
        send_length_args0 = str(args0_length).encode(FORMAT)
        send_length_args0 += b" " * (HEADER - len(send_length_args0))

        # encode the argument on pos 0
        args1 = args[1].encode(FORMAT)

        # save the length of the argument on pos 0
        args1_length = len(args1)

        # format the length of the argument into a send-able format
        send_length_args1 = str(args1_length).encode(FORMAT)
        send_length_args1 += b" " * (HEADER - len(send_length_args1))

        # send the length of the message and the message itself afterwards
        client.send(send_length)
        client.send(message)

        # send the length of the message and the message itself afterwards
        client.send(send_length_args0)
        client.send(args0)

        # send the length of the message and the message itself afterwards
        client.send(send_length_args1)
        client.send(args1)

    elif msg == GET_ERROR_LIST:
        # if len(args) != 0:
        # encode the argument on pos 0
        args0 = args[0].encode(FORMAT)

        # save the length of the argument on pos 0
        args0_length = len(args0)

        # format the length of the argument into a send-able format
        send_length_args0 = str(args0_length).encode(FORMAT)
        send_length_args0 += b" " * (HEADER - len(send_length_args0))

        # send the length of the message and the message itself afterwards
        client.send(send_length)
        client.send(message)

        # send the length of the message and the message itself afterwards
        client.send(send_length_args0)
        client.send(args0)

        # returning the next_station back to the application that called this client function
        error_list = client.recv(2048).decode(FORMAT)
        return error_list

    else:
        # sending the message length and the message itself afterwards (for any other messages)
        client.send(send_length)
        client.send(message)


def get_ip_address():
    ip_address = socket.gethostbyname("WorkstationX.local")
    return ip_address
