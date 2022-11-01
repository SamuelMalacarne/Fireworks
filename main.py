from random import randint
import pygame, sys, time
from pygame import Vector2
from Particle import Particle

# GLOBAL VARIABLES
FPS = 144
WIDTH = 600
HEIGHT = 600

# INITIALISE PYGAME AND CREATE PYGAME OBJECTS
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.mixer.music.set_volume(0.5)
exp_sound = pygame.mixer.Sound('exploding-firework-sound.mp3')
launch_sound = pygame.mixer.Sound('launching-firework-sound.mp3')
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 3000)


class Firework():
    def __init__(self, init_pos, max_explosion_height, min_explosion_height):
        self.pos = init_pos
        self.color = 'white'
        self.acceleration = Vector2(0, -1500)
        self.velocity = Vector2(0, -10)
        self.explosion_height = randint(min_explosion_height, max_explosion_height)
        self.w = 2
        self.h = 6
        self.exploding = False

        self.particles = list()
        self.particles_color = (randint(0, 255), randint(0, 255), randint(0, 255))

        # add 200 to 500 paticle to a particle class
        for i in range(0, randint(200, 501)):
            self.particles.append(Particle(time.time(), time.time()+(randint(1, 10)/10), self.particles_color, randint(1, 3), Vector2(self.pos.x, self.explosion_height), randint(-200, 200), Vector2(randint(-100, 100), randint(-100, 100))))

    # update the rocket position
    def update(self, dt):
        self.velocity.x += self.acceleration.x * dt
        self.velocity.y += self.acceleration.y * dt

        self.pos.x += self.velocity.x * dt
        self.pos.y += self.velocity.y * dt

    # draws the rocket onto the canvas
    def render(self, surf):
        pygame.draw.rect(surf, self.color, pygame.Rect((self.pos.x - (self.w/2)), ((self.pos.y - (self.h/2))), self.w, self.h))

    # checks if the rocked reached its explosion height (which idicates its max height)
    def kill(self):
        self.exploding = self.pos.y <= self.explosion_height
        return self.exploding

    # draws the particles onto the canvas, and delete them if they are dead
    def explode(self, dt, surf):
        # if all the particles died stop the firework explosion
        if len(self.particles) == 0:
            self.exploding = False

        for particle in self.particles.copy():
            particle.update(dt)
            particle.render(surf)

            if particle.dead():
                self.particles.remove(particle)

# initialise variables
fireworks = list()
exploding_firework = list()
prev_time = time.time()

# game loop
while True:

    # calculate delta time
    now = time.time()
    delta_time = now - prev_time
    prev_time = now

    for event in pygame.event.get():
        
        # check if the user closes the window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # check if the screen update happened
        if event.type == SCREEN_UPDATE:
            # adds a firework to the fireworks list
            fireworks.append(Firework(Vector2(randint(0, WIDTH), HEIGHT), (HEIGHT-300), 100))
            launch_sound.play()

        # check if a key's pressed
        if event.type == pygame.KEYDOWN:

            # check if the space bar is pressed
            if event.key == pygame.K_SPACE:
                # adds a firework to the fireworks list
                fireworks.append(Firework(Vector2(randint(0, WIDTH), HEIGHT), (HEIGHT-300), 100))
                launch_sound.play()

    # clean the canvas
    screen.fill((25, 25, 25))

    # update each firework
    for firework in fireworks.copy():
        # update firework position and render it
        firework.update(delta_time)
        firework.render(screen)

        # if the firework should be killed
        if firework.kill():
            # remove the firework from the fireworks list so it won't be rendered nor updated again
            fireworks.remove(firework)
            # add the firework to the exploding fireworks
            exploding_firework.append(firework)
            exp_sound.play()
    
    # render all the particles of the exploding firework
    for firework in exploding_firework.copy():
        firework.explode(delta_time, screen)

        # if the firework is no longer exploding remove it from the exploding firework list
        if not firework.exploding:
            exploding_firework.remove(firework)

    
    pygame.display.set_caption('Fireworks   FPS: %.2f' % clock.get_fps())
    pygame.display.flip()
    clock.tick(FPS)