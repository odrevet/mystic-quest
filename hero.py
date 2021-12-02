import pygame
from enum import Enum

from pygame import image


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Hero:
    SIZE = 16

    def __init__(self) -> None:
        self.direction = Direction.DOWN
        self.image = pygame.image.load("en/spriteSheetHero/hero.png")
        self.image.set_colorkey((255, 255, 255))
        self.x = 72
        self.y = 42
        self.frame_index = 1
        self.is_moving = False
        self.flip = False

    def draw(self, surface_screen):
        surface_screen.blit(
            pygame.transform.flip(self.image, True, False) if self.flip else self.image,
            (self.x, self.y),
            (0, self.frame_index * self.SIZE, self.SIZE, self.SIZE),
        )
