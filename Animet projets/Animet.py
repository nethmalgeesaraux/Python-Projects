import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Particle Firework")

# Colors
BLACK = (0, 0, 0)
COLOR_PALETTE = [
    (255, 0, 0),     # Red
    (0, 255, 0),     # Green
    (0, 0, 255),     # Blue
    (255, 255, 0),   # Yellow
    (255, 0, 255),   # Magenta
    (0, 255, 255),   # Cyan
    (255, 165, 0),   # Orange
    (255, 255, 255)  # White
]

# --- Particle Class ---
class Particle:
    def __init__(self, x, y, color, vel_x, vel_y, lifetime):
        self.x = x
        self.y = y
        self.color = color
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.lifetime = lifetime
        self.radius = 2

    def update(self):
        self.vel_y += 0.05  # gravity
        self.x += self.vel_x
        self.y += self.vel_y
        self.lifetime -= 1

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

# --- Firework Class ---
class Firework:
    def __init__(self, x, y, launch_color):
        self.x = x
        self.y = y
        self.launch_color = launch_color
        self.particles = []
        self.exploded = False
        self.rocket_vel_y = -random.randint(5, 10)
        self.explosion_point = random.randint(150, 250)

    def explode(self):
        self.exploded = True
        num_particles = 300
        for _ in range(num_particles):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 5)
            vel_x = speed * math.cos(angle) * 1.5
            vel_y = speed * math.sin(angle) * 0.8
            color = random.choice(COLOR_PALETTE)
            lifetime = random.randint(60, 120)
            self.particles.append(Particle(self.x, self.y, color, vel_x, vel_y, lifetime))

    def update(self):
        if not self.exploded:
            self.y += self.rocket_vel_y
            if self.y <= self.explosion_point:
                self.explode()
        else:
            for particle in self.particles:
                particle.update()
            self.particles = [p for p in self.particles if p.lifetime > 0]

    def draw(self, surface):
        if not self.exploded:
            pygame.draw.circle(surface, self.launch_color, (int(self.x), int(self.y)), 3)
        else:
            for particle in self.particles:
                particle.draw(surface)

# --- Main Loop ---
fireworks = []
running = True
clock = pygame.time.Clock()
outer_circle_radius = 280
outer_circle_center = (WIDTH // 2, HEIGHT // 2)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            new_firework = Firework(
                x=random.randint(WIDTH // 4, 3 * WIDTH // 4),
                y=HEIGHT,
                launch_color=(255, 0, 0)
            )
            fireworks.append(new_firework)

    for firework in fireworks:
        firework.update()

    fireworks = [f for f in fireworks if f.particles or not f.exploded]

    screen.fill(BLACK)
    pygame.draw.circle(screen, (255, 255, 255), outer_circle_center, outer_circle_radius, 1)

    for firework in fireworks:
        firework.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
