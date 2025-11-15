from abc import ABC, abstractmethod
from typing import Tuple
import pygame


class GameObject(ABC):

    def __init__(
        self,
        x: float,
        y: float,
        size: float = 8.0,
        speed: float = 260.0,
        color: Tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        self.x = x
        self.y = y
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.angle = 0.0
        self.size = size
        self.speed = speed
        self.color = color

    def update(self, dt: float) -> None:
        # Move object according to its velocity
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None:
        pass
