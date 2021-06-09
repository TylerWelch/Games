import pygame
from pygame.locals import *
import random

pygame.init()


#blank game window
screen_width = 600
screen_height = 600

#window
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake Game')

# varibles
cell_size = 10
direction = 1
update_snake = 0
food = [0,0]
new_food = True
new_piece = [0, 0]
score = 0
game_over = False
clicked = False

font = pygame.font.SysFont(None, 40)

#colors
background = (255, 200, 175)
body_inside = (50, 175, 25)
body_outside = (100, 200, 200)
red = (255, 0, 0)
blue = (0, 0, 255)
food_color = (255, 50, 50)

#snake
snake_position = [[int(screen_width / 2), int(screen_height / 2)]]
snake_position.append([int(screen_width / 2), int(screen_height / 2) + cell_size])
snake_position.append([int(screen_width / 2), int(screen_height / 2) + cell_size* 2])
snake_position.append([int(screen_width / 2), int(screen_height / 2) + cell_size * 3])

#play again square
again_rect = Rect(screen_width // 2 -80, screen_height // 2, 160, 50)

#functions
def draw_screen():
    screen.fill(background)

def draw_score():
    score_text = 'Score: ' + str(score)
    score_img = font.render(score_text, True, blue)
    screen.blit(score_img, (0,0))

def check_gameover(game_over):
    #eaten self
    head_count = 0
    for segment in snake_position:
        if snake_position[0] == segment and head_count > 0:
            game_over = True
        head_count += 1

    #out of bounds
    if snake_position[0][0] < 0 or snake_position[0][0] > screen_width or snake_position[0][1] < 0 or snake_position[0][1] > screen_height:
        game_over = True

    return game_over

def draw_gameover():
    over_text = 'Game Over!'
    over_image = font.render(over_text, True, blue)
    pygame.draw.rect(screen, red, (screen_width // 2 - 80, screen_height // 2 - 60, 160, 50))
    screen.blit(over_image, (screen_width // 2 - 80, screen_height // 2 - 50))

    again_text = 'Play Again?'
    again_image = font.render(again_text, True, blue)
    pygame.draw.rect(screen, red, again_rect)
    screen.blit(again_image,(screen_width // 2 - 80, screen_height // 2 +10))

run = True
while run:

    draw_screen()
    draw_score()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != 3:
                direction = 1
            if event.key == pygame.K_RIGHT and direction != 4:
                direction = 2
            if event.key == pygame.K_DOWN and direction != 1:
                direction = 3
            if event.key == pygame.K_LEFT and direction != 2:
                direction = 4

    #make food
    if new_food == True:
        new_food = False
        food[0]= cell_size * random.randint(0, (screen_width / cell_size) - 1)
        food[1]= cell_size * random.randint(0, (screen_height / cell_size) - 1)
    
    #draw food
    pygame.draw.rect(screen, food_color, (food[0], food[1], cell_size, cell_size))
    
    #if food eaten
    if snake_position[0] == food:
        new_food = True
        # add to tail
        new_piece = list(snake_position[-1])
        if direction == 1:
            new_piece[1] += cell_size
        if direction == 3:
            new_piece[1] -= cell_size
        if direction == 2:
            new_piece[0] -= cell_size
        if direction == 4:
            new_piece[0] += cell_size
        
        #add to snake
        snake_position.append(new_piece)
        #increase score
        score += 1


    if game_over == False:
        if update_snake > 99:
            update_snake = 0
            snake_position = snake_position[-1:] + snake_position[:-1]
            #start heading up
            if direction == 1:
                snake_position[0][0] = snake_position[1][0]
                snake_position[0][1] = snake_position[1][1] - cell_size
            if direction == 3:
                snake_position[0][0] = snake_position[1][0]
                snake_position[0][1] = snake_position[1][1] + cell_size
            if direction == 2:
                snake_position[0][1] = snake_position[1][1]
                snake_position[0][0] = snake_position[1][0] + cell_size
            if direction == 4:
                snake_position[0][1] = snake_position[1][1]
                snake_position[0][0] = snake_position[1][0] - cell_size
            game_over = check_gameover(game_over)


    if game_over == True:
        draw_gameover()
        if event.type == pygame.MOUSEBUTTONDOWN and clicked == False:
            clicked = True
        if event.type == pygame.MOUSEBUTTONUP and clicked == True:
            clicked = False
			#reset variables
            game_over = False
            update_snake = 0
            food = [0, 0]
            new_food = True
            new_piece = [0, 0]
            #define snake variables
            snake_position = [[int(screen_width / 2), int(screen_height / 2)]]
            snake_position.append([int(screen_width / 2), int(screen_height / 2) + cell_size])
            snake_position.append([int(screen_width / 2), int(screen_height / 2) + cell_size* 2])
            snake_position.append([int(screen_width / 2), int(screen_height / 2) + cell_size * 3])
            direction = 1 #1 is up, 2 is right, 3 is down, 4 is left
            score = 0

    head = 1
    for x in snake_position:
        if head == 0:
            pygame.draw.rect(screen, body_outside, (x[0], x[1], cell_size, cell_size))
            pygame.draw.rect(screen, body_inside, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
        if head == 1:
            pygame.draw.rect(screen, body_outside, (x[0], x[1], cell_size, cell_size))
            pygame.draw.rect(screen, red, (x[0] + 1, x[1] + 1, cell_size - 2, cell_size - 2))
            head = 0

    pygame.display.update()

    update_snake += 1

pygame.quit()

