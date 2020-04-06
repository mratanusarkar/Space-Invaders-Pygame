import pygame
import random
import math

# game constants
WIDTH = 800
HEIGHT = 600

# global variables
running = True
initial_player_velocity = 3.0
initial_enemy_velocity = 1.0
bullet_velocity = 6.0

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

# create background
background_img = pygame.image.load("res/images/background.jpg")  # 800 x 600 px image

# create player
player_img = pygame.image.load("res/images/spaceship.png")  # 64 x 64 px image
player_width = 64
player_height = 64
player_x = (WIDTH / 2) - (player_width / 2)
player_y = (HEIGHT / 10) * 9 - (player_height / 2)
player_dx = initial_player_velocity
player_dy = 0


def player(x, y):
    window.blit(player_img, (x, y))


# create enemy
enemy_img = pygame.image.load("res/images/enemy.png")  # 64 x 64 px image
enemy_width = 64
enemy_height = 64
enemy_x = random.randint(0, (WIDTH - enemy_width))
enemy_y = random.randint(((HEIGHT / 10) * 1 - (enemy_height / 2)), ((HEIGHT / 10) * 4 - (enemy_height / 2)))
enemy_dx = initial_enemy_velocity
enemy_dy = (HEIGHT / 10) / 2


def enemy(x, y):
    window.blit(enemy_img, (x, y))


# bullet
bullet_img = pygame.image.load("res/images/bullet.png")  # 32 x 32 px image
bullet_width = 32
bullet_height = 32
bullet_x = player_x + player_width / 2 - bullet_width / 2
bullet_y = player_y + bullet_height / 2
bullet_dx = 0
bullet_dy = bullet_velocity
fired = False


def bullet(x, y):
    global fired
    if fired:
        window.blit(bullet_img, (x, y))


# game loop begins
while running:
    # background
    window.fill((0, 0, 0))
    window.blit(background_img, (0, 0))

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
    # player spaceship movement
    if RIGHT_ARROW_KEY_PRESSED:
        player_x += player_dx
    if LEFT_ARROW_KEY_PRESSED:
        player_x -= player_dx
    if (SPACE_BAR_PRESSED or UP_ARROW_KEY_PRESSED) and not fired:
        fired = True
        bullet_x = player_x + player_width / 2 - bullet_width / 2
        bullet_y = player_y + bullet_height / 2
    # enemy movement
    enemy_x += enemy_dx
    # bullet movement
    bullet_y -= bullet_dy

    # boundary check: 0 <= x <= WIDTH, 0 <= y <= HEIGHT
    # player spaceship
    if player_x < 0:
        player_x = 0
    if player_x > WIDTH - player_width:
        player_x = WIDTH - player_width
    # enemy
    if enemy_x <= 0:
        enemy_dx = abs(enemy_dx) * 1
        enemy_y += enemy_dy
    if enemy_x >= WIDTH - enemy_width:
        enemy_dx = abs(enemy_dx) * -1
        enemy_y += enemy_dy
    # bullet
    if bullet_y < 0:
        fired = False
        bullet_x = player_x + player_width / 2 - bullet_width / 2
        bullet_y = player_y + bullet_height / 2

    # create frame by placing objects on the surface
    enemy(enemy_x, enemy_y)
    bullet(bullet_x, bullet_y)
    player(player_x, player_y)

    # render the display
    pygame.display.update()
