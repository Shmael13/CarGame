import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Car Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (100, 100, 100)

# Car properties
car_width = 50
car_height = 100
car_x = WIDTH // 2 - car_width // 2
car_y = HEIGHT - car_height - 20
car_speed = 8  # Constant car speed

# Obstacle properties
obstacle_width = 100
obstacle_height = 100
obstacle_speed = 5
obstacles = []

# Road properties
road_width = WIDTH
road_height = HEIGHT
road_y = 0
road_speed = 5

# Game properties
clock = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 36)

# Speed increase properties
speed_increase_interval = 10  # Increase speed every 10 points
speed_increase_amount = 0.5

# Load and scale images
car_img = pygame.image.load("car.png")
car_img = pygame.transform.scale(car_img, (car_width, car_height))
obstacle_img = pygame.image.load("obstacle.png")
obstacle_img = pygame.transform.scale(obstacle_img, (obstacle_width, obstacle_height))
road_img = pygame.image.load("black.png")
road_img = pygame.transform.scale(road_img, (road_width, road_height))

def draw_car(x, y):
    window.blit(car_img, (x, y))

def draw_obstacle(x, y):
    window.blit(obstacle_img, (x, y))

def draw_road(y):
    window.blit(road_img, (0, y))
    window.blit(road_img, (0, y - road_height))

def game_over():
    game_over_text = font.render("Game Over! Score: " + str(score), True, RED)
    window.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2))
    pygame.display.update()
    pygame.time.wait(2000)

def main():
    global score, car_x, road_y, obstacle_speed, road_speed
    game_exit = False

    while not game_exit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and car_x > 0:
            car_x -= car_speed
        if keys[pygame.K_RIGHT] and car_x < WIDTH - car_width:
            car_x += car_speed

        # Keep the car within the screen boundaries
        car_x = max(0, min(WIDTH - car_width, car_x))

        # Move the road
        road_y += road_speed
        if road_y >= road_height:
            road_y = 0

        # Create new obstacles
        if len(obstacles) < 5 and random.randint(1, 30) == 1:
            obstacle_x = random.randint(0, WIDTH - obstacle_width)
            obstacle_y = -obstacle_height
            obstacles.append([obstacle_x, obstacle_y])

        # Move and remove obstacles
        for obstacle in obstacles:
            obstacle[1] += obstacle_speed
            if obstacle[1] > HEIGHT:
                obstacles.remove(obstacle)
                score += 1

                # Increase speed every 10 points
                if score % speed_increase_interval == 0:
                    obstacle_speed += speed_increase_amount
                    road_speed += speed_increase_amount

        # Check for collisions
        for obstacle in obstacles:
            if car_y < obstacle[1] + obstacle_height and car_y + car_height > obstacle[1]:
                if car_x < obstacle[0] + obstacle_width and car_x + car_width > obstacle[0]:
                    game_over()
                    game_exit = True

        # Draw everything
        draw_road(road_y)
        draw_car(car_x, car_y)
        for obstacle in obstacles:
            draw_obstacle(obstacle[0], obstacle[1])

        # Display score
        score_text = font.render("Score: " + str(score), True, RED)
        window.blit(score_text, (10, 10))

        # Display current speed
        speed_text = font.render(f"Speed: {obstacle_speed:.1f}", True, RED)
        window.blit(speed_text, (10, 50))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()