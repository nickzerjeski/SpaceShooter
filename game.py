import math
import random
from typing import List, Optional

import pygame

from asteroid import Asteroid
from game_object import GameObject
from player import Player
from projectile import Projectile


class Game:
    objects: List[GameObject] = []

    def __init__(self) -> None:
        # Initialize the game
        pygame.init()
        self.game_over = False
        self.score = 0
        pygame.display.set_caption("Space Shooter")
        self.width = 800
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()

        # Time accumulator to control asteroid spawning
        self.asteroid_spawn_timer = 0.0
        # Spawn roughly every 1.5 seconds (can be tweaked)
        self.asteroid_spawn_interval = 0.5

        # Spawn Player
        Game.objects.append(Player(self.width / 2, self.height / 2, size=14.0, speed=260.0))

    def _spawn_asteroid(self) -> None:
        # Choose randomly from where an asteroid spawn and what its
        # size and speed is
        side = random.choice(["top", "bottom", "left", "right"])
        size = random.uniform(12.0, 36.0)
        speed = random.uniform(200.0, 300.0)

        # Set spawn position and angle based on spawn side
        if side == "top":
            x = random.uniform(0, self.width)
            y = -size
            angle = random.uniform(math.radians(60), math.radians(120))
        elif side == "bottom":
            x = random.uniform(0, self.width)
            y = self.height + size
            angle = random.uniform(-math.radians(120), -math.radians(60))
        elif side == "left":
            x = -size
            y = random.uniform(0, self.height)
            angle = random.uniform(-math.radians(30), math.radians(30))
        else:
            x = self.width + size
            y = random.uniform(0, self.height)
            angle = math.pi + random.uniform(-math.radians(30), math.radians(30))

        Game.objects.append(Asteroid(x, y, angle=angle, size=size, speed=speed))

    def _get_objects_hit(self) -> List[GameObject]:
        projectiles = [o for o in Game.objects if isinstance(o, Projectile)]
        asteroids = [o for o in Game.objects if isinstance(o, Asteroid)]
        player = next(o for o in Game.objects if isinstance(o, Player))

        objects_hit: List[GameObject] = []

        # Projectile hits Asteroid
        for asteroid in asteroids:
            for projectile in projectiles:
                dx = asteroid.x - projectile.x
                dy = asteroid.y - projectile.y
                radius_sum = asteroid.size + projectile.size

                if dx * dx + dy * dy <= radius_sum * radius_sum:
                    objects_hit.append(asteroid)
                    self.score += 1
                    break

        # Asteroid hits player
        for asteroid in asteroids:
            dx = asteroid.x - player.x
            dy = asteroid.y - player.y
            radius_sum = asteroid.size + player.size

            if dx * dx + dy * dy <= radius_sum * radius_sum:
                self.game_over = True
                break

        return objects_hit

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

        if new_objects:
            Game.objects.extend(new_objects)

        # Update spawn timer and create new asteroids at fixed intervals
        self.asteroid_spawn_timer += dt
        while self.asteroid_spawn_timer >= self.asteroid_spawn_interval:
            self._spawn_asteroid()
            self.asteroid_spawn_timer -= self.asteroid_spawn_interval

        # Remove objects that are outside the boundary
        # and asteroids that got hit by a projectile
        objects_to_remove = self._get_objects_hit()
        Game.objects = [
            o for o in Game.objects
            if o not in objects_to_remove and
               not (o.x + o.size < 0 or
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
            while running and not self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break

                # Run the game on 120 FPS
                dt = self.clock.tick(120) / 1000.0
                self._update(dt)
                self._render()
        finally:
            if self.game_over:
                print(f"Game over! Score: {self.score}")
            pygame.quit()

# Entry Point
if __name__ == "__main__":
    Game().run()
