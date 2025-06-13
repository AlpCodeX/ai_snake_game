import pygame
import time
import random


pygame.init()

#Dimesions
width = 640
height = 480
block_size = 20

#Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)

#Directions
up = (0, -1)
down = (0, 1)
left = (-1, 0)
right = (1, 0)


screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()

def draw_block(color,pos):
    rect = pygame.Rect(pos[0], pos[1], block_size, block_size)
    pygame.draw.rect(screen, color, rect)
    
def random_food():
    x = random.randint(0, (width - block_size) // block_size) * block_size
    y = random.randint(0, (height - block_size) // block_size) * block_size
    return (x, y)

def main():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = right
    food = random_food()
    score = 0
    game_over = False
    
    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != down:
                    direction = up
                elif event.key == pygame.K_DOWN and direction != up:
                    direction = down
                elif event.key == pygame.K_LEFT and direction != right:
                    direction = left
                elif event.key == pygame.K_RIGHT and direction != left:
                    direction = right
                

        head = (snake[0][0] + direction[0] * block_size, snake[0][1] + direction [1] * block_size)
        snake.insert(0, head)
        
        #When the snake eats
        if head == food:
            score += 1
            food = random_food()
        else:
            snake.pop()
        
        #If the snake has a collison
        if (head in snake[1:] or
            head[0] < 0 or head[0] >= width or
            head[1] < 0 or head[1] >= height):
            game_over = True
            break
        
        #Drawing in the World
        screen.fill(black)
        for block in snake:
            draw_block(green, block)
        draw_block(red, food)
        pygame.display.update()
        clock.tick(10)
        
    print("Game Over! Score: ", score)
    time.sleep(2)
    pygame.quit()
    
if __name__ == "__main__":
    main()
        
        