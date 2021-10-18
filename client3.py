# import required libraries
import socket
from threading import Thread
import tkinter
from tkinter import *


# receive messages in loop and display in tkinter window
def receive():
    while True:
        try:
            msg = s.recv(1024).decode()  # receive messages and decode it into string.
            msg_list.insert(tkinter.END, msg)  # insert new message at the end.
        except Exception:
            print("There is an Error Receiving Message")

# get message from tkinter entry field and send the message to the server
def send():
    msg = my_msg.get() # get message from entry field.
    my_msg.set("") # make the entry field blank, for new messages
    s.send(bytes(msg, "utf8")) # send message to the server in encode form.


window = Tk()
window.title("Chat Application")
window.configure(bg="green")

message_frame = Frame(window, height=100, width=100, bg='white')
message_frame.pack()

my_msg = StringVar()
my_msg.set("")

scroll_bar = Scrollbar(message_frame)
msg_list = Listbox(message_frame, height=15, width=100, bg="white", yscrollcommand=scroll_bar.set)
scroll_bar.pack(side=RIGHT, fill=Y)
msg_list.pack(side=LEFT, fill=BOTH)
msg_list.pack()

entry_field = Entry(window, textvariable=my_msg, fg="black", width=50)
entry_field.pack()

send_button = Button(window, text="Send", font="Aerial", fg="black", bg="blue", command=send)
send_button.pack()

host = "localhost"
port = 8080

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))

receive_thread = Thread(target=receive)
receive_thread.start()

mainloop()
