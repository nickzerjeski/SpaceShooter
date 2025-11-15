import math
from typing import List
from game_object import GameObject
from player import Player
import pygame

from projectile import Projectile


class Game:
    objects: List[GameObject] = []

    def __init__(self) -> None:
        # Initialize the game
        pygame.init()
        pygame.display.set_caption("Space Shooter")
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # Spawn Player
        Game.objects.append(Player(self.width / 2, self.height / 2, size=14.0, speed=260.0))

    def _update(self, dt: float) -> None:
        # Use a new list to prevent editing the original list while looping it
        new_objects: List[GameObject] = []

        # Update all objects
        for obj in Game.objects:
            obj.update(dt)

            # Add a projectile to new_objects when player shoots
            if isinstance(obj, Player) and obj.has_shot:
                ux = math.sin(obj.angle)
                uy = -math.cos(obj.angle)
                offset = obj.size + 2.0
                px = obj.x + ux * offset
                py = obj.y + uy * offset
                new_objects.append(Projectile(px, py, obj.angle))
                obj.has_shot = False

        # Add the projectiles to Game object list
        if new_objects:
            Game.objects.extend(new_objects)

        # Remove objects that are outside the boundary
        # TODO: Game over if object is Player
        Game.objects = [
            o for o in Game.objects
            if not (o.x + o.size < 0 or
                    o.x - o.size > self.width or
                    o.y + o.size < 0 or
                    o.y - o.size > self.height)
        ]

    def _render(self) -> None:
        # Consider https://www.pygame.org/docs/ref/display.html
        # for further understanding

        # Draws everything to the back buffer
        self.screen.fill((0, 0, 0))
        for obj in Game.objects:
            obj.draw(self.screen)

        # Switches front and back buffer to make newly drawn objects visible
        pygame.display.flip()

    def run(self) -> None:
        # Main loop of the game
        try:
            running = True
            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break

                # Run the game on 120 FPS
                dt = self.clock.tick(120) / 1000.0
                self._update(dt)
                self._render()
        finally:
            pygame.quit()


# Entry Point
if __name__ == "__main__":
    Game().run()
