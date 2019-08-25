from tkinter import Tk, Frame, Listbox, Scrollbar, StringVar, Entry, Button, END, RIGHT, LEFT, Y
from socket import socket, AF_INET, SOCK_STREAM
from threading import Thread


def recieve_message():
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            message_list.insert(END, message)
        except:
            pass


def send_message(event=None): 
    if message.get() == "{quit}":
        client_socket.send(bytes("{quit}", "utf-8"))
        client_socket.close()
        
    client_socket.send(bytes(message.get(), "utf-8"))
    message_list.insert(END, message.get())
    message.set("")
    

def on_closing(event=None):
    message.set("{quit}")
    send_message()


server_host = "DESKTOP-P7B1FVT"
server_port = 12345
client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect((server_host, server_port))


root = Tk()
root.minsize(400, 380)
root.title("Chat")

main_frame = Frame(root)
top_separator = Frame(main_frame, height=30)
mid_separator = Frame(main_frame, height=15)

message_list_frame = Frame(main_frame)
scroll = Scrollbar(message_list_frame)
message_list = Listbox(message_list_frame, width=54, height=15, yscrollcommand=scroll.set, font="Arial 10", relief="flat")
scroll.config(command=message_list.yview)

message_field = Frame(main_frame)
message = StringVar()
text_field = Entry(message_field, textvariable=message, width=40, relief="flat", font="Arial 10")
text_field.bind("<Return>", send_message)
send_button = Button(message_field, width=5, height=1, text="send", relief="flat", font="Arial 10")

main_frame.pack()
top_separator.pack()
message_list_frame.pack()
scroll.pack(side=RIGHT, fill=Y)
message_list.pack()
mid_separator.pack()
message_field.pack()
text_field.pack(side=LEFT)
send_button.pack(side=LEFT)

root.protocol("WM_DELETE_WINDOW", on_closing)


if __name__ == "__main__":
    receive_thread = Thread(target=recieve_message)
    receive_thread.start()
    root.mainloop()