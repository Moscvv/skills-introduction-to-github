import pygame
from pygame import mixer 
import random
import time
import sys 
import json

# Basic Game Structure 
# Initializing Pygame
pygame.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Screen dimensions
WIDTH = 800
HEIGHT = 600

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Clock to control game speed
clock = pygame.time.Clock()

#snake
class Snake:
    def __init__(self):
        self.size = 20
        self.x = WIDTH // 2 
        self.y = HEIGHT // 2 
        self.dx = self.size # Movement in x-direction
        self.dy = 0         # Movement in y-direction  
        self.body = [(self.x, self.y)]  # List of snake segments
        self.length = 1

    def move(self):
        # Update head position
        self.x += self.dx
        self.y += self.dy

        # Add new head to body
        self.body.insert(0, (self.x, self.y))    

        # Remove tail if longer than lenght
        if len(self.body) > self.length:
            self.body.pop()

    def draw(self):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0], segment[1], self.size, self.size))  

    def change_direction(self, dx, dy):
        # Prevent reversing direction
        if self.dx != -dx and self.dy != -dy:
            self.dx = dx
            self.dy = dy

#food
class Food:
    def __init__(self, snake):
        self.size = 20
        self.snake = snake
        self.respawn()  # Initialize position using respawn()

    def respawn(self):
        while True:
            self.x = random.randint(0, (WIDTH - self.size) // self.size) * self.size
            self.y = random.randint(0, (HEIGHT - self.size) // self.size) * self.size
        # Check if new position collides with snake
            if (self.x, self.y) not in self.snake.body:
                break
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self):
        pygame.draw.rect(screen, RED, self.rect)


# Sound/Music
eat_sound = mixer.Sound("nya.wav")
game_over_sound = mixer.Sound("game_over.wav") 

# Start background music (loop forever)
pygame.mixer.music.load("background.wav")  # Replace with your file
pygame.mixer.music.set_volume(0.5)  # Optional: 50% volume



#Game Loop and Logic
def game_loop():
    pygame.mixer.music.play(-1)  # Start/restart music (-1 = loop forever)
    snake = Snake()
    food = Food(snake)
    score = 0
    font = pygame.font.Font(None, 36)
    game_over = False
    

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                game_over_sound.play()
                

            #Keyboard controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake.change_direction(-snake.size, 0)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(snake.size, 0)
                elif event.key == pygame.K_UP:
                    snake.change_direction(0, -snake.size)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(0, snake.size)      

        # Move snake
        snake.move()

        # Collision with food
        snake_head_rect = pygame.Rect(snake.x, snake.y, snake.size, snake.size)
        if snake_head_rect.colliderect(food.rect):
            snake.length += 1
            score += 10
            food.respawn()
            eat_sound.play() # eat sound

        # Collision with walls
        if (snake.x <0 or snake.x >= WIDTH or
            snake.y <0 or snake.y >= HEIGHT):
            game_over = True
            game_over_sound.play()
            pygame.mixer.music.stop() # Stoping background music  
            
        # Collision with self    
        for segment in snake.body[1:]:
            if snake.body[0] == segment:
                game_over = True
                game_over_sound.play()
                pygame.mixer.music.stop() # Stoping background music  
                

        # Drawing everything
        screen.fill(BLACK)
        snake.draw()
        food.draw()

        # Score display
        text = font.render(f'Score: {score}', True, WHITE)
        screen.blit(text, (10, 10))

        pygame.display.update()
        clock.tick(10) #Controls game speed (lower = slower)

    high_score = read_high_score()
    if score > high_score:
        write_high_score(score)

    return score  # Return the final score to use in the game over screen

# Start game screen
def start_screen():
    pygame.event.clear()
    screen.fill(BLACK)
    title_font = pygame.font.Font(None, 74)
    text_font = pygame.font.Font(None, 36)
    
    # Title
    title = title_font.render("SNAKE GAME", True, GREEN)
    title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    screen.blit(title, title_rect)
    
    # Instructions
    text = text_font.render("Press SPACE to Start", True, WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    screen.blit(text, text_rect)
    
    pygame.display.update()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

# Game Over Screen
def game_over_screen(score):
    pygame.event.clear()
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    #Game Over Text
    text = font.render('GAME OVER', True, RED)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
    screen.blit(text, text_rect)

    score_text = small_font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))
    screen.blit(score_text, score_rect)

    #Restart Promt
    restart_text = small_font.render('Press SPACE to Restart or Q to Quit', True, WHITE)
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 80))
    screen.blit(restart_text, restart_rect)

    # High Score Display
    high_score = read_high_score()
    hs_text = small_font.render(f"High Score: {high_score}", True, WHITE)
    hs_rect = hs_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
    screen.blit(hs_text, hs_rect)

    # Adjust positions of other elements
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 20))  # Move down
    restart_rect = restart_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 120))  # Adjust spacing

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.stop()  # Stop before restarting
                    waiting = False
                if event.key == pygame.K_q:
                    pygame.mixer.music.stop() 
                    pygame.quit()
                    sys.exit()    

# High Score System
def read_high_score():
    try:
        with open("high_score.txt", "r") as f:
            content = f.read().strip()
            if not content:
                return 0
            return int(content)
    except (FileNotFoundError, ValueError, PermissionError):
        return 0        
    

def write_high_score(score):
    with open("high_score.txt", "w") as f:
        f.write(str(score))

# Start the game  
while True:
    start_screen()          # Show start screen
    final_score = game_loop()  # Play the game
    game_over_screen(final_score)  # Show game over screen with score                                  
