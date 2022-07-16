import socket

HEADER = 2048
PORT = 5555
FORMAT = 'utf-8'
END = "end"
Pressed = "Pressed"
SERVER = socket.gethostbyname(socket.gethostname())

ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    print(client.recv(HEADER).decode(FORMAT))


#send("IPandPort")
print(client.recv(HEADER).decode(FORMAT))
input()
print(client.recv(HEADER).decode(FORMAT))
send("Pressed")
send("player#")
