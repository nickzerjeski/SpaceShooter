import math
import random
from typing import List, Tuple

import pygame

from game_object import GameObject


class Asteroid(GameObject):

    def __init__(
        self,
        x: float,
        y: float,
        angle: float,
        size: float,
        speed: float,
    ) -> None:
        super().__init__(x, y, size=size, speed=speed)

        # Set movement based on spawn angle and speed
        self.velocity_x = math.cos(angle) * self.speed
        self.velocity_y = math.sin(angle) * self.speed
        self.angle = angle

        # Small rotational speed so asteroids spin a bit
        self.rotation_speed = random.uniform(-0.5, 0.5)

    def _polygon_points(self) -> List[Tuple[float, float]]:
        # Create points of the polygon
        base_points = [
            (0.0 * self.size, -1.0 * self.size),
            (0.6 * self.size, -0.7 * self.size),
            (1.0 * self.size, -0.1 * self.size),
            (0.8 * self.size, 0.7 * self.size),
            (0.2 * self.size, 1.0 * self.size),
            (-0.6 * self.size, 0.8 * self.size),
            (-1.0 * self.size, 0.1 * self.size),
            (-0.7 * self.size, -0.7 * self.size),
        ]

        c = math.cos(self.angle)
        d = math.sin(self.angle)
        cx = self.x
        cy = self.y

        def rot(px: float, py: float) -> Tuple[float, float]:
            # Rotate and translate
            return cx + px * c - py * d, cy + px * d + py * c

        return [rot(px, py) for (px, py) in base_points]

    def update(self, dt: float) -> None:
        super().update(dt)
        self.angle += self.rotation_speed * dt

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.polygon(surface, self.color, self._polygon_points(), width=0)

