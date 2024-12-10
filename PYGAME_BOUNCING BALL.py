import pygame
import sys
import random
import os

# Initialize pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bouncing Ball Game with Levels")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Load background image (make sure you have a 'background.png' in your project directory)
background = pygame.image.load("background.png")  # Replace "background.jpg" with the path to your image
background = pygame.transform.scale(background, (screen_width, screen_height))  # Scale the background to fit the screen

# Load ball image (make sure you have a 'ball.png' or similar image in your project directory)
ball_image = pygame.image.load("ball.png")  # Replace "ball.png" with the path to your ball image
ball_image = pygame.transform.scale(ball_image, (40, 40))  # Resize ball to desired size

# Define ball settings
ball_x = screen_width // 4
ball_y = screen_height // 2
ball_velocity_y = 0  # Initial vertical speed is 0
gravity = 0.2  # Slower gravity (default level 1)
bounce_strength = -5  # Reduced bounce strength for less jump

# Define obstacle settings
obstacle_width = 50
obstacle_velocity_x = 3 # Slower speed at which obstacles move left (default level 1)
obstacles = []  # List to hold obstacles

# Set up font for score and level
font = pygame.font.SysFont(None, 36)

# Clock to control frame rate
clock = pygame.time.Clock()

# Game score and level
score = 0
level = 1
obstacle_gap = 300  # Default obstacle gap

# High score file path
highscore_file = "highscore.txt"

# Function to load the high score from file
def load_highscore():
    if os.path.exists(highscore_file):
        with open(highscore_file, "r") as file:
            return int(file.read().strip())
    return 0  # Default high score is 0 if the file doesn't exist

# Function to save the high score to file
def save_highscore(new_highscore):
    with open(highscore_file, "w") as file:
        file.write(str(new_highscore))

# Function to generate a new obstacle
def create_obstacle():
    height = random.randint(150, 350)  # Smaller random height for top pipe, reduced variation
    top_rect = pygame.Rect(screen_width, 0, obstacle_width, height)  # Top pipe
    bottom_rect = pygame.Rect(screen_width, height + obstacle_gap, obstacle_width, screen_height - height - obstacle_gap)  # Bottom pipe
    # Return a tuple with the Rects and a scored flag set to False initially
    return (top_rect, bottom_rect, False)

# Function to display score, level, and highscore
def display_score_and_level(score, level, highscore):
    score_text = font.render(f"Score: {score}", True, BLUE)
    level_text = font.render(f"Level: {level}", True, BLUE)
    highscore_text = font.render(f"High Score: {highscore}", True, BLUE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (screen_width - 100, 10))
    screen.blit(highscore_text, (10, 50))

# Function to display game over screen
def display_game_over():
    game_over_text = font.render("GAME OVER", True, RED)
    retry_text = font.render("Press R to Retry", True, BLUE)
    screen.blit(game_over_text, (screen_width // 2 - 100, screen_height // 2 - 50))
    screen.blit(retry_text, (screen_width // 2 - 100, screen_height // 2 + 10))

# Load the current high score
highscore = load_highscore()

# Game loop
running = True
game_over = False

while running:
    screen.fill(WHITE)  # Fill screen with white color to clear it every frame

    # Draw background image
    screen.blit(background, (0, 0))  # Blit the background image to the screen at position (0, 0)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        # Control the ball with the spacebar (make it jump)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:  # Make the ball bounce upwards when space is pressed
            ball_velocity_y = bounce_strength  # Reset vertical velocity to make the ball jump

        # Apply gravity to the ball's vertical velocity
        ball_velocity_y += gravity  # Gravity constantly increases the downward velocity

        # Update ball position (y position)
        ball_y += ball_velocity_y  # Change y position based on vertical speed

        # Prevent ball from going out of bounds at the bottom
        if ball_y > screen_height - 40:  # Prevent the ball from going below the screen (size of ball image)
            ball_y = screen_height - 40  # Set ball at the bottom of the screen
            ball_velocity_y *= -0.9  # Reverse the vertical velocity (bounce effect with reduced speed)

        # Prevent ball from going above the top of the screen
        if ball_y < 0:
            ball_y = 0  # Set ball at the top of the screen
            ball_velocity_y = 0  # Stop the upward movement if the ball hits the top

        # Create a new obstacle when needed
        if len(obstacles) == 0 or obstacles[-1][0].x < screen_width - 200:
            obstacles.append(create_obstacle())

        # Move obstacles to the left
        for i, (top, bottom, scored) in enumerate(obstacles):
            top.x -= obstacle_velocity_x
            bottom.x -= obstacle_velocity_x

            # Check if the obstacle passed the ball (for scoring purposes)
            if top.x + obstacle_width < ball_x and not scored:
                # Increment score and mark as scored
                obstacles[i] = (top, bottom, True)
                score += 1  # Increase score when the obstacle is passed

        # Remove obstacles that are out of screen
        obstacles = [obs for obs in obstacles if obs[0].x > -obstacle_width]

        # Check for level change (Level 4 when score reaches 30)
        if score >= 30 and level == 3:
            level = 4  # Change to level 4
            obstacle_velocity_x = 6 # Increase obstacle speed in level 4
            gravity = 0.5  # Increase gravity in level 4
            obstacle_gap = 180  # Reduce the obstacle gap for level 4

        # Check for level change (Level 3 when score reaches 15)
        if score >= 15 and level == 2:
            level = 3  # Change to level 3
            obstacle_velocity_x = 5  # Increase obstacle speed in level 3
            gravity = 0.4  # Increase gravity in level 3
            obstacle_gap = 210  # Reduce the obstacle gap for level 3

        # Check for level change (Level 2 when score reaches 5)
        if score >= 5 and level == 1:
            level = 2  # Change to level 2
            obstacle_velocity_x = 4  # Increase obstacle speed in level 2
            gravity = 0.3  # Increase gravity in level 2
            obstacle_gap = 235  # Reduce the obstacle gap for level 2

        # Update highscore if necessary
        if score > highscore:
            highscore = score
            save_highscore(highscore)

        # Draw the ball (using ball image)
        screen.blit(ball_image, (ball_x - 20, int(ball_y) - 20))  # Adjust the position to center the image

        # Draw the obstacles (top and bottom pipes) in red
        for top, bottom, _ in obstacles:
            pygame.draw.rect(screen, RED, top)  # Top pipe in red
            pygame.draw.rect(screen, RED, bottom)  # Bottom pipe in red

        # Check for collisions between the ball and obstacles
        ball_rect = pygame.Rect(ball_x - 20, ball_y - 20, 40, 40)  # Create a Rect for the ball image
        for top, bottom, _ in obstacles:
            if ball_rect.colliderect(top) or ball_rect.colliderect(bottom):
                game_over = True  # Trigger game over

        # Display the score, level, and high score on the screen
        display_score_and_level(score, level, highscore)

    else:
        # Display game over screen
        display_game_over()

        # Wait for player to press 'R' to restart
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:  # If 'R' is pressed, restart the game
            game_over = False
            score = 0
            level = 1
            ball_y = screen_height // 2
            ball_velocity_y = 0
            obstacles = []
            obstacle_velocity_x = 3
            gravity = 0.2
            obstacle_gap = 300  # Reset the obstacle gap

    # Update the display
    pygame.display.flip()

    # Control the frame rate (60 frames per second)
    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
