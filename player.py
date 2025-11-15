import math
from typing import List, Tuple
import pygame

from game_object import GameObject


class Player(GameObject):

    def __init__(self, x: float, y: float, size: float, speed: float) -> None:
        super().__init__(x, y, size=size, speed=speed)
        self.has_shot = False

    def _handle_input(self, keys) -> None:
        # Simple WASD controls
        up = keys[pygame.K_w]
        left  = keys[pygame.K_a]
        down  = keys[pygame.K_s]
        right = keys[pygame.K_d]
        shoot = keys[pygame.K_SPACE]

        dx = int(right) - int(left)
        dy = int(down)  - int(up)

        # Movement and direction logic was handled by ChatGPT (don't wanted to do the maths)
        if dx or dy:
            inv_len = 1.0 / max(1e-9, math.hypot(dx, dy))  # normalize diagonals
            self.velocity_x = dx * inv_len * self.speed
            self.velocity_y = dy * inv_len * self.speed
            # Base triangle points "up"; add +π/2 to rotate tip toward velocity
            self.angle = math.atan2(self.velocity_y, self.velocity_x) + math.pi / 2.0
        else:
            self.velocity_x = self.velocity_y = 0.0

        if shoot:
            self.has_shot = True


    # Triangle shape of player was also calculated by ChatGPT
    def _triangle_points(self) -> List[Tuple[float, float]]:
        s = self.size
        tip = (0.0, -s)
        bl  = (-0.75 * s, 0.9 * s)
        br  = ( 0.75 * s, 0.9 * s)

        c = math.cos(self.angle)
        d = math.sin(self.angle)
        cx = self.x
        cy = self.y

        def rot(px: float, py: float) -> Tuple[float, float]:
            # Rotate and translate
            return cx + px * c - py * d, cy + px * d + py * c

        return [rot(*tip), rot(*bl), rot(*br)]

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self._handle_input(keys)
        super().update(dt)

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.polygon(surface, self.color, self._triangle_points(), width=0)
