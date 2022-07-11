# Imports
import sys
import pygame
import threading
import socket

# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

font = pygame.font.SysFont('Arial', 30)


# global variables
buttons = []

message = []

my_turn = True

player_number = -1
player_colour = '#333333'

# used for receive_msg_thread
game_ended = False


class Button():
    def __init__(self, x, y, width, height, id, buttonText='Button', onclickFunction=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.Pressed = False
        self.id = id

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

    def process(self):
        global my_turn

        mousePos = pygame.mouse.get_pos()

        if self.Pressed:
            self.buttonSurface.fill(self.fillColors['pressed'])
        else:
            self.buttonSurface.fill(self.fillColors['normal'])

        # take some action only when mouse is on the button
        if my_turn:
            if self.buttonRect.collidepoint(mousePos):
                if not self.Pressed:
                    self.buttonSurface.fill(self.fillColors['hover'])

                if pygame.mouse.get_pressed(num_buttons=3)[0]:
                    # make it one press only button
                    if not self.Pressed:
                        self.Pressed = True
                        self.onclickFunction(self)
                        # my_turn = False

        # display
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


def send_msg(button):
    global conn

    # msg format is like below
    msg = f"pressed {player_number} {button.id}"
    conn.sendall(bytes(msg))


def send_msg_test(button):
    print(f"pressed {player_number} {button.id}")


def process_msg(msg):
    # tell function to use global variable
    global player_number
    global player_colour
    global game_ended
    global my_turn

    msg.decode()
    command = msg.split(" ")
    if command[0] == "end":
        game_ended = True
    elif command[0] == "player#":
        player_number = int(command[1])
    elif command[0] == "player_colour":
        player_colour = command[1]
    elif command[0] == "player_turn":
        # sever notify all clients who are the next one to play
        if player_number == command[1]:
            my_turn = True
    elif command[0] == "remote_press":
        # someone else pressed a button
        button_id = int(command[1])
        colour = command[2]
        buttons[button_id - 1].remote_change_colour(colour)
    elif command[0] == "display":
        # change the display message
        message[0].buttonSurf = font.render(command[1], True, (20, 20, 20))


def receive_msg_thread():
    global conn

    while not game_ended:
        data = conn.recv(1024)
        process_msg(data)


# for test only
customButton = Button(30, 30, 400, 100, 1, 'Button One (one Press only)', send_msg_test)
customButton = Button(30, 180, 400, 100, 2, 'Button Two (one Press only)', send_msg_test)
customButton = Button(30, 330, 400, 100, 3, 'Button Three (one Press only)', send_msg_test)


# main tasks starts


# initialize map
# for testing, please use send_msg_test instead of send_msg


# connect to server, the variable 'conn' should be a global variable


# put the connection into a thread
# t1 = threading.Thread(target=receive_msg_thread)

# starting thread 1
# t1.start()

# Game loop.
while True:
    screen.fill((80, 80, 60))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            # wait until thread 1 is completely executed
            # t1.join()
            sys.exit()

    for object in buttons:
        object.process()

    for object in message:
        object.process()

    pygame.display.flip()
    fpsClock.tick(fps)

