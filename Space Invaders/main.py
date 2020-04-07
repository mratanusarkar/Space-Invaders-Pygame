import pygame
import random
import math

# game constants
WIDTH = 800
HEIGHT = 600

# global variables
running = True
score = 0
highest_score = 0
life = 3
kills = 0
difficulty = 1
level = 1
initial_player_velocity = 3.0
initial_enemy_velocity = 1.0
weapon_shot_velocity = 5.0

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
bullet_dy = weapon_shot_velocity
fired = False


def bullet(x, y):
    global fired
    if fired:
        window.blit(bullet_img, (x, y))


# laser beam
laser_img = pygame.image.load("res/images/beam.png")  # 24 x 24 px image
laser_width = 24
laser_height = 24
laser_x = enemy_x + enemy_width / 2 - laser_width / 2
laser_y = enemy_y + laser_height / 2
laser_dx = 0
laser_dy = weapon_shot_velocity
beamed = False
shoot_probability = 0.3
shoot_timer = 0
relaxation_time = 100


def laser(x, y):
    global beamed
    if beamed:
        window.blit(laser_img, (x, y))


def scoreboard():
    x_offset = 10
    y_offset = 10
    # sent font type and size
    font = pygame.font.SysFont("calibre", 16)

    # render font
    score_sprint = font.render("SCORE : " + str(score), True, (255, 255, 255))
    highest_score_sprint = font.render("HI-SCORE : " + str(highest_score), True, (255, 255, 255))
    level_sprint = font.render("LEVEL : " + str(level), True, (255, 255, 255))
    difficulty_sprint = font.render("DIFFICULTY : " + str(difficulty), True, (255, 255, 255))
    life_sprint = font.render("LIFE LEFT : " + str(life) + " | " + ("@ " * life), True, (255, 255, 255))

    # place the font sprites on the screen
    window.blit(score_sprint, (x_offset, y_offset))
    window.blit(highest_score_sprint, (x_offset, y_offset + 20))
    window.blit(level_sprint, (x_offset, y_offset + 40))
    window.blit(difficulty_sprint, (x_offset, y_offset + 60))
    window.blit(life_sprint, (x_offset, y_offset + 80))


def collision_check(object1_x, object1_y, object1_diameter, object2_x, object2_y, object2_diameter):
    x1_cm = object1_x + object1_diameter / 2
    y1_cm = object1_y + object1_diameter / 2
    x2_cm = object2_x + object2_diameter / 2
    y2_cm = object2_y + object2_diameter / 2
    distance = math.sqrt(math.pow((x2_cm - x1_cm), 2) + math.pow((y2_cm - y1_cm), 2))
    return distance < ((object1_diameter + object2_diameter) / 2)


def respawn():
    global enemy_x
    global enemy_y
    enemy_x = random.randint(0, (WIDTH - enemy_width))
    enemy_y = random.randint(((HEIGHT / 10) * 1 - (enemy_height / 2)), ((HEIGHT / 10) * 4 - (enemy_height / 2)))


def kill_enemy():
    global fired
    global bullet_x
    global bullet_y
    global score
    global kills
    global difficulty
    fired = False
    bullet_x = player_x + player_width / 2 - bullet_width / 2
    bullet_y = player_y + bullet_height / 2
    score = score + 10 * difficulty
    kills += 1
    if kills % 10 == 0:
        difficulty += 1
    print("Score:", score)
    print("level:", level)
    print("difficulty:", difficulty)
    respawn()


def rebirth():
    global player_x
    global player_y
    player_x = (WIDTH / 2) - (player_width / 2)
    player_y = (HEIGHT / 10) * 9 - (player_height / 2)


def gameover():
    global running
    global score
    global highest_score

    if score > highest_score:
        highest_score = score

    # console display
    print("----------------")
    print("GAME OVER !!")
    print("----------------")
    print("you died at")
    print("Level:", level)
    print("difficulty:", difficulty)
    print("Your Score:", score)
    print("----------------")
    print("Try Again !!")
    print("----------------")
    running = False


def kill_player():
    global beamed
    global laser_x
    global laser_y
    global life
    beamed = False
    laser_x = enemy_x + enemy_width / 2 - laser_width / 2
    laser_y = enemy_y + laser_height / 2
    life -= 1
    print("Life Left:", life)
    if life > 0:
        rebirth()
    else:
        gameover()


# game loop begins
def destroy_weapons():
    global fired
    global beamed
    global bullet_x
    global bullet_y
    global laser_x
    global laser_y
    fired = False
    beamed = False
    bullet_x = player_x + player_width / 2 - bullet_width / 2
    bullet_y = player_y + bullet_height / 2
    laser_x = enemy_x + enemy_width / 2 - laser_width / 2
    laser_y = enemy_y + laser_height / 2


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
    # bullet firing
    if (SPACE_BAR_PRESSED or UP_ARROW_KEY_PRESSED) and not fired:
        fired = True
        bullet_x = player_x + player_width / 2 - bullet_width / 2
        bullet_y = player_y + bullet_height / 2
    # laser beaming
    if not beamed:
        shoot_timer += 1
        if shoot_timer == relaxation_time:
            shoot_timer = 0
            random_chance = random.randint(0, 100)
            if random_chance <= (shoot_probability * 100):
                beamed = True
                laser_x = enemy_x + enemy_width / 2 - laser_width / 2
                laser_y = enemy_y + laser_height / 2
    # enemy movement
    enemy_x += enemy_dx * float(2 ** (difficulty - 1))
    # bullet movement
    if fired:
        bullet_y -= bullet_dy
    # laser movement
    if beamed:
        laser_y += laser_dy

    # collision check
    bullet_enemy_collision = collision_check(bullet_x, bullet_y, bullet_width, enemy_x, enemy_y, enemy_width)
    if bullet_enemy_collision:
        kill_enemy()
    laser_player_collision = collision_check(laser_x, laser_y, laser_width, player_x, player_y, player_width)
    if laser_player_collision:
        kill_player()
    enemy_player_collision = collision_check(enemy_x, enemy_y, enemy_width, player_x, player_y, player_width)
    if enemy_player_collision:
        kill_enemy()
        kill_player()
    bullet_laser_collision = collision_check(bullet_x, bullet_y, bullet_width, laser_x, laser_y, laser_width)
    if bullet_laser_collision:
        destroy_weapons()

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
    # laser
    if laser_y > HEIGHT:
        beamed = False
        laser_x = enemy_x + enemy_width / 2 - laser_width / 2
        laser_y = enemy_y + laser_height / 2

    # create frame by placing objects on the surface
    scoreboard()
    laser(laser_x, laser_y)
    enemy(enemy_x, enemy_y)
    bullet(bullet_x, bullet_y)
    player(player_x, player_y)

    # render the display
    pygame.display.update()
