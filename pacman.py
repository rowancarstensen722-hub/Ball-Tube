import pygame
import sys
import random

pygame.init()

# ---------------------
# Window Settings
# ---------------------
WIDTH = 400
HEIGHT = 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ball Tube")

# Colors
BLUE = (135, 206, 235)
RED = (0, 0, 0)
GREEN = (0, 200, 0)
GRAY = (139, 69, 19)

clock = pygame.time.Clock()
FPS = 60

# ---------------------
# Bird Settings
# ---------------------
bird_x = 80
bird_y = HEIGHT // 2
bird_radius = 18
gravity = 0.4
velocity = 0
jump_strength = -20

# ---------------------
# Floor Settings
# ---------------------
FLOOR_HEIGHT = 40

# ---------------------
# Pipes
# ---------------------
pipe_width = 70
gap_size = 250
pipe_speed = 3
pipes = []

def create_pipe():
    gap_y = random.randint(140, HEIGHT - 200)
    top_rect = pygame.Rect(WIDTH, 0, pipe_width, gap_y - gap_size // 2)
    bottom_rect = pygame.Rect(WIDTH, gap_y + gap_size // 2, pipe_width, HEIGHT - FLOOR_HEIGHT)
    return top_rect, bottom_rect

pipes.append(create_pipe())

# Score
score = 0
font = pygame.font.SysFont("arial", 32)


def reset_game():
    global bird_y, velocity, pipes, score
    bird_y = HEIGHT // 2
    velocity = 0
    pipes = [create_pipe()]
    score = 0


running = True
while running:
    clock.tick(FPS)

    # ---------------------
    # Input
    # ---------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                velocity = jump_strength
            if event.key == pygame.K_r:
                reset_game()

    # ---------------------
    # Bird Movement
    # ---------------------
    velocity += gravity
    bird_y += velocity

    # bird rectangle
    bird_rect = pygame.Rect(bird_x - bird_radius, bird_y - bird_radius,
                            bird_radius * 2, bird_radius * 2)

    # ---------------------
    # Pipes Movement
    # ---------------------
    for i, (top, bottom) in enumerate(pipes):
        top.x -= pipe_speed
        bottom.x -= pipe_speed

        if top.x < -pipe_width:
            pipes.pop(i)
            pipes.append(create_pipe())
            score += 1

    # ---------------------
    # Collision
    # ---------------------

    for top, bottom in pipes:

        # Bird landing safely on top of bottom pipe?
        standing_on_pipe = (
            bird_rect.bottom >= bottom.top - 5 and
            bird_rect.bottom <= bottom.top + 10 and
            bird_rect.right > bottom.left and
            bird_rect.left < bottom.right and
            velocity >= 0
        )

        if standing_on_pipe:
            bird_y = bottom.top - bird_radius * 2
            velocity = 0
            break

        # Bird hitting pipe sides? (DIE)
        if bird_rect.colliderect(top) or bird_rect.colliderect(bottom):
            reset_game()

    # Hit the floor (safe landing)
    if bird_rect.bottom >= HEIGHT - FLOOR_HEIGHT:
        bird_y = HEIGHT - FLOOR_HEIGHT - bird_radius * 2
        velocity = 0

    # Hit sky (die)
    if bird_y < 0:
        reset_game()

    # ---------------------
    # DRAW
    # ---------------------
    WIN.fill(BLUE)

    # Bird
    pygame.draw.circle(WIN, RED, (bird_x, int(bird_y)), bird_radius)

    # Pipes
    for top, bottom in pipes:
        pygame.draw.rect(WIN, GREEN, top)
        pygame.draw.rect(WIN, GREEN, bottom)

    # Floor
    pygame.draw.rect(WIN, GRAY, (0, HEIGHT - FLOOR_HEIGHT, WIDTH, FLOOR_HEIGHT))

    # Score
    WIN.blit(font.render(f"Score: {score}", True, RED), (10, 10))

    pygame.display.update()

