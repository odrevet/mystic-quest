import pygame
from enum import Enum


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Hero(pygame.sprite.Sprite):
    SIZE = 16

    def __init__(self, x, y) -> None:
        self.direction = Direction.DOWN
        self.image = pygame.image.load("en/spriteSheetHero/hero.png")
        self.image.set_colorkey((255, 255, 255))
        self.x = x
        self.y = y
        self.frame_index = 1
        self.is_moving = False
        self.flip = False
        self.bounding_box = pygame.Rect(
            x, y + self.SIZE // 2, self.SIZE, self.SIZE // 2
        )

        self.hp = 19
        self.mp = 6
        self.gold = 50

        self.animations = [
            [3, 4],
            [5, 6],
            [1, 2],
            [5, 6],
        ]

    def draw(self, surface_screen):
        surface_screen.blit(
            pygame.transform.flip(self.image, True, False) if self.flip else self.image,
            (self.x, self.y),
            (0, self.frame_index * self.SIZE, self.SIZE, self.SIZE),
        )

        # if __debug__:
        #    pygame.draw.rect(surface_screen, (42, 42, 42), self.bounding_box)

    def update(self):
        self.bounding_box.x = self.x
        self.bounding_box.y = self.y + self.SIZE // 2

        # update hero location
        if self.is_moving:
            if self.direction == Direction.UP:
                self.y -= 1
                self.frame_index = self.animations[0][0]
            if self.direction == Direction.RIGHT:
                self.x += 1
                self.frame_index = self.animations[1][0]
            if self.direction == Direction.DOWN:
                self.y += 1
                self.frame_index = self.animations[2][0]
            if self.direction == Direction.LEFT:
                self.x -= 1
                self.frame_index = self.animations[3][0]
