import pygame
import random
import math
from pygame import mixer
import time


WIDTH = 800
HEIGHT = 600

running = True
pause_state = 0
score = 0
highest_score = 0
life = 3
kills = 0
difficulty = 1
level = 1
max_kills_to_difficulty_up = 5
max_difficulty_to_level_up = 5
initial_player_velocity = 3.0
initial_enemy_velocity = 1.0
weapon_shot_velocity = 5.0
single_frame_rendering_time = 0
total_time = 0
frame_count = 0
fps = 0

player = type('Player', (), {})()
bullet = type('Bullet', (), {})()
enemies = []
lasers = []

pygame.init()

LEFT_ARROW_KEY_PRESSED = 0
RIGHT_ARROW_KEY_PRESSED = 0
UP_ARROW_KEY_PRESSED = 0
SPACE_BAR_PRESSED = 0
ENTER_KEY_PRESSED = 0
ESC_KEY_PRESSED = 0

window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
window_icon = pygame.image.load("res/images/alien.png")
pygame.display.set_icon(window_icon)

pause_sound = None
level_up_sound = None
weapon_annihilation_sound = None
game_over_sound = None

background_img = pygame.image.load("res/images/background.jpg")
background_music_paths = ["res/sounds/Space_Invaders_Music.ogg",
                          "res/sounds/Space_Invaders_Music_x2.ogg",
                          "res/sounds/Space_Invaders_Music_x4.ogg",
                          "res/sounds/Space_Invaders_Music_x8.ogg",
                          "res/sounds/Space_Invaders_Music_x16.ogg",
                          "res/sounds/Space_Invaders_Music_x32.ogg"]


def init_background_music():
    if difficulty == 1:
        mixer.quit()
        mixer.init()
    if difficulty <= 6:
        mixer.music.load(background_music_paths[difficulty - 1])
    else:
        mixer.music.load(background_music_paths[5])
    mixer.music.play(-1)


class Player:
    def __init__(self, img_path, width, height, x, y, dx, dy, kill_sound_path):
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.kill_sound_path = kill_sound_path
        self.kill_sound = mixer.Sound(self.kill_sound_path)

    def draw(self):
        window.blit(self.img, (self.x, self.y))


class Enemy:
    def __init__(self, img_path, width, height, x, y, dx, dy, kill_sound_path):
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.kill_sound_path = kill_sound_path
        self.kill_sound = mixer.Sound(self.kill_sound_path)

    def draw(self):
        window.blit(self.img, (self.x, self.y))


class Bullet:
    def __init__(self, img_path, width, height, x, y, dx, dy, fire_sound_path):
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.fired = False
        self.fire_sound_path = fire_sound_path
        self.fire_sound = mixer.Sound(self.fire_sound_path)

    def draw(self):
        if self.fired:
            window.blit(self.img, (self.x, self.y))


class Laser:
    def __init__(self, img_path, width, height, x, y, dx, dy, shoot_probability, relaxation_time, beam_sound_path):
        self.img_path = img_path
        self.img = pygame.image.load(self.img_path)
        self.width = width
        self.height = height
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.beamed = False
        self.shoot_probability = shoot_probability
        self.shoot_timer = 0
        self.relaxation_time = relaxation_time
        self.beam_sound_path = beam_sound_path
        self.beam_sound = mixer.Sound(self.beam_sound_path)

    def draw(self):
        if self.beamed:
            window.blit(self.img, (self.x, self.y))


def scoreboard():
    x_offset = 10
    y_offset = 10
    font = pygame.font.SysFont("calibre", 16)

    score_sprint = font.render("SCORE : " + str(score), True, (255, 255, 255))
    hightst_score_sprint = font.render("HI-SCORE : " + str(highest_score), True, (255, 255, 255))
    level_sprint = font.render("LEVEL : " + str(level), True, (255, 255, 255))
    difficulty_sprint = font.render("DIFFICULTY : " + str(difficulty), True, (255, 255, 255))
    life_sprint = font.render("LIFE LEFT : " + str(life) + " | " + ("@ " * life), True, (255, 255, 255))

    fps_sprint = font.render("FPS : " + str(fps), True, (255, 255, 255))
    frame_time_in_ms = round(single_frame_rendering_time * 1000, 2)
    frame_time_sprint = font.render("FT : " + str(frame_time_in_ms) + " ms", True, (255, 255, 255))

    window.blit(score_sprint, (x_offset, y_offset))
    window.blit(hightst_score_sprint, (x_offset, y_offset + 20))
    window.blit(level_sprint, (x_offset, y_offset, + 40))
    window.blit(difficulty.sprint, (x_offset, y_offset + 60))
    window.blit(life_sprint, (x_offset, y_offset + 80))
    window.blit(fps_sprint, (WIDTH - 80, y_offset))
    window.blit(frame_time_sprint, (WIDTH - 80, y_offset + 20))


def collision_check(object1, object2):
    x1_cm = object1.x + object1.width / 2
    y1_cm = object1.y + object1.width / 2
    x2_cm = object2.x + object2.width / 2
    y2_cm = object2.y + object2.width / 2
    distance = math.sqrt(math.pow((x2_cm - x1_cm), 2) + math.pow((y2_cm - y1_cm), 2))
    return distance < ((object1.width + object2.width) / 2)


def level_up():
    global life
    global level
    global difficulty
    global max_difficulty_to_level_up
    level_up_sound.play()
    level += 1
    life += 1
    difficulty = 1
    if level % 3 == 0:
        player.dx += 1
        bullet.dy += 1
        max_difficulty_to_level_up += 1
        for each_laser in lasers:
            each_laser.shoot_probability += 0.1
            if each_laser.shoot_probability > 1.0:
                each_laser.shoot_probability = 1.0
    if max_difficulty_to_level_up > 7:
        max_difficulty_to_level_up = 7
    font = pygame.font.SysFont("freesansbold", 64)
    gameover_sprint = font.render("LEVEL UP", True, (255, 255, 255))
    window.blit(gameover_sprint, (WIDTH / 2 - 120, HEIGHT / 2 - 32))
    pygame.display.update()
    init_game()
    time.sleep(1.0)

def respawn(enemy_obj):
    enemy_obj.x = random.randint(0, (WIDTH - enemy_obj.width))
    enemy_obj.y = random.randint(((HEIGHT / 10) * 1 - (enemy_obj.height / 2)),
                                 ((HEIGHT / 10) * 4 - (enemy_obj.height / 2)))


def kill_enemy(player_obj, bullet_obj, enemy_obj):
    global score
    global kills
    global difficulty
    bullet_obj.fired = False
    enemy_obj.kill_sound.play()
    bullet_obj.x = player_obj.x + player_obj.width / 2 - bullet_obj.width / 2
    bullet_obj.y = player_obj.y + bullet_obj.height / 2
    score = score + 10 * difficulty * level
    kills += 1
    if kills % max_kills_to_difficulty_up == 0:
        difficulty += 1
        if (difficulty == max_difficulty_to_level_up) and ( life != 0):
            level_up()
        init_background_music()
    print("Score:", score)
    print("level:", level)
    print("difficulty:", difficulty)
    respawn(enemy_obj)


def rebirth(player_obj):
    player_obj.x = (WIDTH / 2) - (player_obj.width / 2)
    player_obj.y = (HEIGHT / 10) * 9 - (player_obj.height / 2)


def gameover_screen():
    scoreboard()
    font= pygame.font.SysFont