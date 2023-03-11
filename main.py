import math
import pygame
import random
from pygame import mixer

#Initialize Pygame
pygame.init()

#initialize screen
screen = pygame.display.set_mode((800,600))

#Title Icon
pygame.display.set_caption("WAR ATTACK")
icono = pygame.image.load("avionDeCombate.png")
pygame.display.set_icon(icono)

#points
points = 0
font = pygame.font.Font('Molot.otf',32)
text_x = 10
text_y = 10
startGame_text = pygame.font.Font('Molot.otf',80)
endGame_text = pygame.font.Font('Molot.otf',80)
instructions_text = pygame.font.Font('Molot.otf',20)
press_spacebar_text = pygame.font.Font('Molot.otf',40)

#music settings
mixer.music.load('backGroundMusic.wav')
mixer.music.set_volume(0.4)
mixer.music.play(-1)

#Player
img_player = pygame.image.load("protagonista.png")
player_x = 368
player_y = 500
player_x_movement = 0

#enemy variables
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_movement = []
enemy_y_movement = []
enemysQuantity = 12

for e in range (enemysQuantity):
    img_enemy.append(pygame.image.load("enemigo.png"))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 200))
    enemy_x_movement.append(0.3)
    enemy_y_movement.append(20)

#bullet
img_bullet = pygame.image.load("bala.png")
bullet_x = 0
bullet_y = 500
bullet_x_movement = 0
bullet_y_movement = 1
bullet_On =  False

#menu boolean
main_menu = True

#start menu
def start_game():
    showStartGameText = startGame_text.render("WAR ATTACK!",True,(255,255,255))
    showInstructionsText = instructions_text.render("Prevent the skulls from reaching the bottom of the screen!", True, (255, 255, 255))
    showPressSpacebarText = press_spacebar_text.render("Press Spacebar to Start!", True, (255, 255, 255))
    screen.blit(showStartGameText,(150,200))
    screen.blit(showInstructionsText, (90, 300))
    screen.blit(showPressSpacebarText, (150, 350))

def final_text():
    showEndGameText = endGame_text.render("YOU LOOSE",True,(255,0,0))
    screen.blit(showEndGameText,(200,200))

#show points function
def show_points(x,y):
    text = font.render(f"Points: {points}",True,(255,255,255))
    screen.blit(text,(x,y))

#set player png
def player(x,y):
    screen.blit(img_player,(x,y))

#set enemy png
def enemy(x,y,ene):
    screen.blit(img_enemy[e],(x,y))

def shoot_bullet(x,y):
    global bullet_On
    bullet_On = True
    screen.blit(img_bullet,(x + 16, y + 10))

def isCollision (x_1, y_1 ,x_2 ,y_2):
    distance = math.sqrt(math.pow(x_2 - x_1, 2) + math.pow(y_2 - y_1, 2))
    if distance < 27:
        return True
    else:
        return False

#Create Screen
playing = True
while playing:

    #Set background RGB
    screen.fill((0, 137, 255))

    #show main menu screen
    if main_menu:
        start_game()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main_menu = False

        pygame.display.update()

    else:

        #game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

            #player movement
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_movement -= 0.5
                elif event.key == pygame.K_RIGHT:
                    player_x_movement += 0.5
                elif event.key == pygame.K_SPACE and not bullet_On:
                    bullet_noise = mixer.Sound('disparo.mp3')
                    bullet_noise.play()
                    bullet_x = player_x
                    shoot_bullet(bullet_x,bullet_y)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_movement = 0

        #change player ubication
        player_x += player_x_movement

        #player limits of the screen
        if player_x <=0:
            player_x = 0
        elif player_x >= 736:
            player_x = 736

        player(player_x, player_y)

        #change enemy ubication
        for e in range(enemysQuantity):

            #endgame
            if enemy_y[e] > player_y -10:
                for k in range(enemysQuantity):
                    enemy_y[k] = 1500
                final_text()
                break

            enemy_x[e] += enemy_x_movement[e]

            #enemy limits of the screen
            if enemy_x[e] <=0:
                enemy_x_movement[e] += 0.4
                enemy_y[e] += enemy_y_movement[e]
            elif enemy_x[e] >= 736:
                enemy_x_movement[e] -= 0.4
                enemy_y[e] += enemy_y_movement[e]

            # Collision
            collision = isCollision(enemy_x[e], enemy_y[e], bullet_x, bullet_y)
            if collision:
                bullet_hit = mixer.Sound('golpe.mp3')
                bullet_hit.play()
                bullet_y = 500
                bullet_On = False
                points += 10
                enemy_x[e] = random.randint(0, 736)
                enemy_y[e] = random.randint(50, 200)

            enemy(enemy_x[e], enemy_y[e],e)

        #bullet limits of the screen
        if bullet_y <= 0:
            bullet_y = 500
            bullet_On = False
        if bullet_On:
            shoot_bullet(bullet_x,bullet_y)
            bullet_y -= bullet_y_movement


        show_points(text_x,text_y)

        #update game
        pygame.display.update()