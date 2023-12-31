# Imports
import sys
import pygame
import threading
import socket

# specify network ip and port here
ip = "localhost"
port = 0

# user input for server ip and port
if ip == 'localhost':
    ip = input("Enter IP: ")
if port == 0:
    port = int(input("Enter port: "))

# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 1200, 800
screen = pygame.display.set_mode((width, height))

font = pygame.font.SysFont('Arial', 30)

# global variables
buttons = []

message = []

my_turn = False

player_number = -1
player_colour = '#333333'

# used for receive_msg_thread
game_ended = False


# button class - the board GUI is populated with 256 buttons
class Button():
    def __init__(self, x, y, width, height, id, buttonText='Button', onclickFunction=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.Pressed = False
        self.id = id
        self.other_player = False

        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': player_colour,
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        buttons.append(self)

    def remote_change_colour(self, colour: str):
        self.fillColors['pressed'] = colour
        self.Pressed = True
        self.other_player = True

    def process(self):
        global my_turn
        global game_ended
        global player_colour

        mousePos = pygame.mouse.get_pos()

        if self.Pressed:
            # update player colour
            if not self.other_player:
                self.fillColors['pressed'] = player_colour

            self.buttonSurface.fill(self.fillColors['pressed'])
        else:
            self.buttonSurface.fill(self.fillColors['normal'])

        # take some action only when mouse is on the button
        if my_turn and not game_ended:
            if self.buttonRect.collidepoint(mousePos):
                if not self.Pressed:
                    self.buttonSurface.fill(self.fillColors['hover'])

                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    # make it one press only button
                    if not self.Pressed:
                        self.Pressed = True
                        self.onclickFunction(self)
                        my_turn = False

        # display
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


# Message box to display to user their player number/colour and which player's turn is it
class MsgBox():
    def __init__(self, x, y, width, height, buttonText='Button'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.Pressed = False
        self.other_player = False
        self.msg = buttonText
        self.text_colour = (20, 20, 20)

        self.fillColors = {
            'normal': '#ffffff',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(self.msg, True, self.text_colour)

        message.append(self)

    def change_msg(self, msg: str):
        self.msg = msg

    def change_txt_colour(self, colour: str):
        h = colour.lstrip('#')
        self.text_colour = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

    def process(self):

        self.buttonSurface.fill(self.fillColors['normal'])
        self.buttonSurf = font.render(self.msg, True, self.text_colour)

        # display
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


# sends message with pressed button data and corresponding player id to server
def send_msg(button):
    global conn
    global game_ended

    if game_ended:
        return

    # msg format is like below
    msg = f"pressed {player_number} {button.id}"
    conn.conn.sendall(bytes(msg, encoding='utf8'))


# a testing function for onclickFunction in button
def send_msg_test(button):
    print(f"pressed {player_number} {button.id}")


# receives message from server about game status (e.g. game ended, assigned player number/colour, who's turn is it)
def process_msg(msg):
    # tell function to use global variable
    global player_number
    global player_colour
    global game_ended
    global my_turn
    global message
    global buttons

    d_msg = msg.decode()
    print(d_msg)
    command = d_msg.split(" ")

    # if tree for token process, ignore irrelevant message
    if command[0] == "end":
        message[1].change_msg(f"Game over")
        game_ended = True
    elif command[0] == "player#":
        player_number = int(command[1])
        message[0].change_msg(f"You are P{player_number}")
    elif command[0] == "player_colour":
        player_colour = command[1]
        message[0].change_txt_colour(player_colour)
    elif command[0] == "player_turn":
        # sever notify all clients who are the next one to play
        if player_number == int(command[1]):
            my_turn = True
            message[1].change_msg(f"Your turn")
        else:
            my_turn = False
            message[1].change_msg(f"Please wait for P{command[1]}")
    elif command[0] == "remote_press":
        # someone else pressed a button
        button_id = int(command[1])
        colour = command[2]
        buttons[button_id - 1].remote_change_colour(colour)
    elif command[0] == "display":
        # change the display message
        msg = " ".join(command[1:])
        message[2].change_msg(msg)


# connect to server, the variable 'conn' should be a global variable (need to test)
class Network():
    def __init__(self):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # get ip from user

        self.conn.connect((ip, port))

        # we do need receive function to be a blocking call
        # self.conn.setblocking(False)

        # start threads
        # send is handled by buttons' onclickFunction
        # self.send_thread = threading.Thread(target=self.send)
        # self.send_thread.start()

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

    # send message to server
    # send is handled by buttons' onclickFunction
    # def send(self):
    #     global conn
    #
    #     while True:
    #         for button in buttons:
    #             if button.Pressed:
    #                 # send message to server
    #                 send_msg(button)
    #
    #         fpsClock.tick(fps)

    # receive message from server
    def receive(self):
        global game_ended

        # we need to end this thread, by a signal
        while not game_ended:
            try:
                data = self.conn.recv(1024)
                # process message
                process_msg(data)
            except:
                pass
            # fpsClock should only appear in the main game loop
            # fpsClock.tick(fps)
        # close the connection
        self.conn.close()


conn = Network()

# initialize map (16x16)
for i in range(16):
    for j in range(16):
        Button(i * 50, j * 50, 50, 50, i * 16 + j + 1, buttonText=str(i * 16 + j + 1), onclickFunction=send_msg)

# initialize msg box
# player number
MsgBox(850, 50, 300, 100, "Please wait")
# notification
MsgBox(850, 200, 300, 100, "Please wait")
# msg box
MsgBox(850, 350, 300, 150, "")

# Game loop.
while True:
    screen.fill((80, 80, 60))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # wait until thread is completely executed
            conn.receive_thread.join()
            sys.exit()

    for object in buttons:
        object.process()

    for object in message:
        object.process()

    pygame.display.flip()
    fpsClock.tick(fps)
