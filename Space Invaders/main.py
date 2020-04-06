import pygame

# game constants
HEIGHT = 800
WIDTH = 600

# global variables
running = True

# initialize pygame
pygame.init()

# create display window
window = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("Space Invaders")
window_icon = pygame.image.load("res/images/rocket.png")
pygame.display.set_icon(window_icon)

# game loop begins
while running:

    # window.fill((255, 0, 0))

    for event in pygame.event.get():

        # Quit Event
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()
