import pygame 
import sys
import random

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (67, 235, 52)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

square_x = screen_width/2
square_y = screen_height/2
square_size = 50

treasure_x = random.randrange(0, screen_width)
treasure_y = random.randrange(0, screen_height)
treasure_size = 50

enemy_size = 50
enemy_x = enemy_size
enemy_y = enemy_size
enemy_speed = 2

# [ [0, 0], [100, 50] ]
bullets = []
bullet_size = 30
bullet_speed = 5

score = 0

shoot_cooldown = 1_000
game_time = 3_000
shoot_time = pygame.time.get_ticks() - shoot_cooldown
start_ticks = pygame.time.get_ticks()
clock = pygame.time.Clock()

def shoot_bullet(direction):
    global shoot_time
    now = pygame.time.get_ticks()
    if now - shoot_time > shoot_cooldown:
        bullets.append([square_x, square_y, direction])
        shoot_time = pygame.time.get_ticks()

def move_bullets():
    # Aqui movere las balas
    # bullets = [ [0, 0, up], [100, 50, left], [300, 450, down], [150, 345, right] ]
    for bullet in bullets:
        if bullet[2] == "up":
            bullet[1] -= bullet_speed
        elif bullet[2] == "down":
            bullet[1] += bullet_speed
        elif bullet[2] == "left":
            bullet[0] -= bullet_speed
        elif bullet[2] == "right":
            bullet[0] += bullet_speed

def draw_bullets():
    for bullet in bullets:
        if bullet [2] == "up" or bullet[2] == "down":
            pygame.draw.rect(screen, BLACK, (bullet[0], bullet[1], bullet_size/3, bullet_size))
        if bullet [2] == "left" or bullet[2] == "right":
            pygame.draw.rect(screen, BLACK, (bullet[0], bullet[1], bullet_size, bullet_size/3))

running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        square_x -= 5
    if keys[pygame.K_d]:
        square_x += 5
    if keys[pygame.K_w]:
        square_y -= 5
    if keys[pygame.K_s]:
        square_y += 5

    if keys[pygame.K_UP]:
        shoot_bullet("up")
    if keys[pygame.K_DOWN]:
        shoot_bullet("down")
    if keys[pygame.K_LEFT]:
        shoot_bullet("left")
    if keys[pygame.K_RIGHT]:
        shoot_bullet("right")

    move_bullets()

    if enemy_x > square_x:
        enemy_x -= enemy_speed
    if enemy_x < square_x:
        enemy_x += enemy_speed
    if enemy_y > square_y:
        enemy_y -= enemy_speed
    if enemy_y < square_y:
        enemy_y += enemy_speed

    if square_x < treasure_x + treasure_size and square_x > treasure_x - treasure_size and square_y < treasure_y + treasure_size and square_y > treasure_y - treasure_size:
        treasure_x = random.randrange(0, screen_width)
        treasure_y = random.randrange(0, screen_height)
        score += 1

    if square_x < enemy_x + enemy_size and square_x > enemy_x - enemy_size and square_y < enemy_y + enemy_size and square_y > enemy_y - enemy_size:
        enemy_x = random.randrange(0, screen_width)
        enemy_y = random.randrange(0, screen_height)
        score -= 1

    for bullet in bullets:
        if bullet[0] < enemy_x + enemy_size and bullet[0] > enemy_x - enemy_size and bullet[1] < enemy_y + enemy_size and bullet[1] > enemy_y - enemy_size:
            enemy_x = random.randrange(0, screen_width)
            enemy_y = random.randrange(0, screen_height)
            score += 1
    
    # Tiempo restante
    playing_time = (pygame.time.get_ticks() - start_ticks) // 1000
    time_left = game_time - playing_time
    if time_left <= 0:
        running = False

    screen.fill(WHITE)
    pygame.draw.rect(screen, BLUE, (square_x, square_y, square_size, square_size))
    pygame.draw.circle(screen, GREEN, (treasure_x, treasure_y), treasure_size, 100)
    pygame.draw.circle(screen, RED, (enemy_x, enemy_y), enemy_size, 100)
    draw_bullets()


    font = pygame.font.SysFont("monospace", 35)
    time_text = font.render(f"Tiempo: {time_left}", True, BLACK)
    score_text = font.render(f"Puntuacion: {score}", True, BLACK)
    screen.blit(score_text, (10, 50))
    screen.blit(time_text, (10, 20))
    pygame.display.flip()