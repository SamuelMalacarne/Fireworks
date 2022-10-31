import pygame, time
from pygame import Vector2

class Particle():
    def __init__(self, age: int, life_time: int, color: tuple, size: int, init_pos: Vector2, velocity: int, direction: Vector2):
        self.life_time = life_time
        self.color = color
        self.size = size
        self.pos = init_pos
        self.velocity = velocity
        self.acceleration = Vector2(0, 500)
        self.age = age
        self.direction = direction

    def update(self, dt):
        # # self.direction.x += self.acceleration.x * dt
        # if self.direction.y < 0:
        #     self.direction.y += self.acceleration.y * dt
        # # else:
        # #     self.direction.y -= self.acceleration.y * dt

        self.pos.x += self.velocity * (self.direction.x / 100) * dt
        self.pos.y += self.velocity * (self.direction.y / 100) * dt
        self.age += dt

    def render(self, surf):
        pygame.draw.circle(surf, self.color, self.pos, self.size)

    def dead(self):
        return self.age >= self.life_time