# Imports
import sys
import pygame

# Configuration
pygame.init()
fps = 60
fpsClock = pygame.time.Clock()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

font = pygame.font.SysFont('Arial', 30)

buttons = []

my_turn = False


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
            'pressed': '#333333',
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))

        buttons.append(self)

    def remote_change_colour(self, colour: str):
        self.fillColors['pressed'] = colour

    def process(self):
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

        # display
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
            self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)


def myFunction(button):
    print(f'Button {button.id} Pressed')


customButton = Button(30, 30, 400, 100, 1, 'Button One (one Press only)', myFunction)
customButton = Button(30, 180, 400, 100, 2, 'Button Two (one Press only)', myFunction)
customButton = Button(30, 330, 400, 100, 3, 'Button Three (one Press only)', myFunction)

# Game loop.
while True:
    screen.fill((80, 80, 60))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    for object in buttons:
        object.process()

    pygame.display.flip()
    fpsClock.tick(fps)

