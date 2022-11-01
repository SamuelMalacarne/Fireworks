import pygame, time
from pygame import Vector2

class Particle():
    def __init__(self, age: int, life_time: int, color: tuple, size: int, init_pos: Vector2, velocity: int, direction: Vector2):
        self.life_time = life_time
        self.color = color
        self.size = size
        self.pos = init_pos
        self.velocity = velocity
        self.age = age
        self.direction = direction

    #updates the position of the particle and the age
    def update(self, dt):
        self.pos.x += self.velocity * (self.direction.x / 100) * dt
        self.pos.y += self.velocity * (self.direction.y / 100) * dt
        self.age += dt

    # draws the particle onto the canvas
    def render(self, surf):
        pygame.draw.circle(surf, self.color, self.pos, self.size)

    # checks if the particle reached its lifetime
    def dead(self):
        return self.age >= self.life_time