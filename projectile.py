import math
import pygame

from game_object import GameObject


class Projectile(GameObject):

    def __init__(self, x: float, y: float, angle: float, speed: float = 480.0, size: float = 4.0) -> None:
        super().__init__(x, y, size=size, speed=speed)
        self.velocity_x = math.sin(angle) * self.speed
        self.velocity_y = -math.cos(angle) * self.speed
        self.angle = angle

    def update(self, dt: float) -> None:
        super().update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        # Small filled circle
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), int(self.size))
