# importing required libraries.
import socket
from threading import Thread

# define IP and port for server.
host = "localhost"
port = 8080

clients = {}  # clients dict to store information about clients connection.

# create socket object
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# set configuration so that many clients can request on one single port.
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# bind the IP and port to the socket object.
sock.bind((host, port))


# function to get name and broadcast to all others.
def handle_clients(conn):
    # get client's name from it's connection
    name = conn.recv(1024).decode()

    # send the client a welcome message
    welcome = f"Welcome {name}. Good to see you :)"
    conn.send(bytes(welcome, "utf8"))

    # create a message of recently added clients
    msg = name + " has recently joined us"

    # send the message to the all connected clients.
    broadcast(bytes(msg, "utf8"))

    # save the newly added clients info to the dictionary
    clients[conn] = name

    # receive message from client in loop and broadcast it.
    while True:
        msg = conn.recv(1024)
        broadcast(msg, name + ":")


# send the message to the all connected clients.
def broadcast(msg, prefix=""):
    for client in clients:  # clients is dict that save client's connection info
        client.send(bytes(prefix, "utf8") + msg)


def accept_client_connection():
    while True:  # accept client's request
        client_conn, client_address = sock.accept()  # accept client request
        print(client_address, " has Connected")

        # send a welcome message to the client and ask for name from it.
        client_conn.send(bytes("Welcome to the chat room, Please type your name to continue", "utf8"))

        # start the handle clients function in a thread.
        Thread(target=handle_clients, args=(client_conn,)).start()


if __name__ == "__main__":
    # server is listening........
    sock.listen(3)  # here we are accepting max of three clients at once.
    print("listening on port : ", port, "......")

    # start the accept function into thread for handle multiple request at once.
    t = Thread(target=accept_client_connection)

    t.start()  # start thread
    t.join()  # thread wait for main thread to exit.
