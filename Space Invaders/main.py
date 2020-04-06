import pygame

# game constants
WIDTH = 800
HEIGHT = 600

# global variables
running = True

# initialize pygame
pygame.init()

# Input key states (keyboard)
LEFT_ARROW_KEY_PRESSED = 0
RIGHT_ARROW_KEY_PRESSED = 0
UP_ARROW_KEY_PRESSED = 0
SPACE_BAR_PRESSED = 0

# create display window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
window_icon = pygame.image.load("res/images/alien.png")
pygame.display.set_icon(window_icon)

# create player
player_img = pygame.image.load("res/images/spaceship.png")  # 64 x 64 px image
player_x = (WIDTH / 2) - (64 / 2)               # 370
player_y = (HEIGHT / 10) * 9 - (64 / 2)         # 480
player_dx = 0.1
player_dy = 0


def player(x, y):
    window.blit(player_img, (x, y))


# game loop begins
while running:
    # background
    window.fill((0, 0, 0))

    # register events
    for event in pygame.event.get():
        # Quit Event
        if event.type == pygame.QUIT:
            running = False

        # Keypress Down Event
        if event.type == pygame.KEYDOWN:
            # Left Arrow Key down
            if event.key == pygame.K_LEFT:
                print("LOG: Left Arrow Key Pressed Down")
                LEFT_ARROW_KEY_PRESSED = 1
            # Right Arrow Key down
            if event.key == pygame.K_RIGHT:
                print("LOG: Right Arrow Key Pressed Down")
                RIGHT_ARROW_KEY_PRESSED = 1
            # Up Arrow Key down
            if event.key == pygame.K_UP:
                print("LOG: Up Arrow Key Pressed Down")
                UP_ARROW_KEY_PRESSED = 1
            # Space Bar down
            if event.key == pygame.K_SPACE:
                print("LOG: Space Bar Pressed Down")
                SPACE_BAR_PRESSED = 1

        # Keypress Up Event
        if event.type == pygame.KEYUP:
            # Right Arrow Key up
            if event.key == pygame.K_RIGHT:
                print("LOG: Right Arrow Key Released")
                RIGHT_ARROW_KEY_PRESSED = 0
            # Left Arrow Key up
            if event.key == pygame.K_LEFT:
                print("LOG: Left Arrow Key Released")
                LEFT_ARROW_KEY_PRESSED = 0
            # Up Arrow Key up
            if event.key == pygame.K_UP:
                print("LOG: Up Arrow Key Released")
                UP_ARROW_KEY_PRESSED = 0
            # Space Bar up
            if event.key == pygame.K_SPACE:
                print("LOG: Space Bar Released")
                SPACE_BAR_PRESSED = 0

    # manipulate game objects based on events and player actions
    if RIGHT_ARROW_KEY_PRESSED:
        player_x += player_dx
    if LEFT_ARROW_KEY_PRESSED:
        player_x -= player_dx

    # create frame by placing objects on the surface
    player(player_x, player_y)

    # render the display
    pygame.display.update()
