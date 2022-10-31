from random import randint
import pygame, sys, time
from pygame import Vector2
from Particle import Particle

FPS = 144
WIDTH = 600
HEIGHT = 600

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.mixer.music.set_volume(0.7)
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

        for i in range(0, randint(200, 500)):
            self.particles.append(Particle(time.time(), time.time()+(randint(1, 10)/10), self.particles_color, randint(1, 3), Vector2(self.pos.x, self.explosion_height), randint(-200, 200), Vector2(randint(-100, 100), randint(-100, 100))))

    def update(self, dt):
        self.velocity.x += self.acceleration.x * dt
        self.velocity.y += self.acceleration.y * dt

        self.pos.x += self.velocity.x * dt
        self.pos.y += self.velocity.y * dt

    def render(self, surf):
        pygame.draw.rect(surf, self.color, pygame.Rect((self.pos.x - (self.w/2)), ((self.pos.y - (self.h/2))), self.w, self.h))

    def kill(self):
        self.exploding = self.pos.y <= self.explosion_height
        return self.exploding

    def explode(self, dt, surf):
        for particle in self.particles.copy():
            particle.update(dt)
            particle.render(surf)

            if particle.dead():
                self.particles.remove(particle)


fireworks = list()
exploding_firework = list()
prev_time = time.time()

while True:

    now = time.time()
    delta_time = now - prev_time
    prev_time = now

    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            fireworks.append(Firework(Vector2(randint(0, WIDTH), HEIGHT), (HEIGHT-100), 100))
            launch_sound.play()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                fireworks.append(Firework(Vector2(randint(0, WIDTH), HEIGHT), (HEIGHT-100), 100))
                launch_sound.play()

    screen.fill((25, 25, 25))

    for firework in fireworks.copy():
        firework.update(delta_time)
        firework.render(screen)

        if firework.kill():
            fireworks.remove(firework)
            exploding_firework.append(firework)
            exp_sound.play()
    
    for firework in exploding_firework:
        firework.explode(delta_time, screen)


    pygame.display.set_caption('Fireworks   FPS: %.2f' % clock.get_fps())
    pygame.display.flip()
    clock.tick(FPS)