import pygame
from constants import *

class Ship(pygame.sprite.Sprite):
    # This class represents the ship. It derives from the "Sprite" class in Pygame

    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
        # Load the image of the ship
        self.image = pygame.image.load("img/ship.png").convert_alpha() #convert alpha to make sure transparent
        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

    # Functions for moving the ship
    def moveRight(self, pixels):
        self.rect.x += pixels
        self.image = pygame.image.load("img/shipRight.png").convert_alpha()


    def moveLeft(self, pixels):
        self.rect.x -= pixels
        self.image = pygame.image.load("img/shipLeft.png").convert_alpha()

    def default(self):
        self.image = pygame.image.load("img/ship.png").convert_alpha()

class Enemy(pygame.sprite.Sprite):
    # This class represents the enemies that will come down in waves
    def __init__(self, value, colour):
        # Call the parent class
        super().__init__()

        # Load the image of the enemy
        if colour == "green":
            self.image = pygame.image.load("img/enemyGreen.png").convert_alpha()
        elif colour == "blue":
            self.image = pygame.image.load("img/enemyBlue.png").convert_alpha()
        else:
            self.image = pygame.image.load("img/enemyPink.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.enemySpeed = value

    def update(self):
        self.rect.x += self.enemySpeed
        if self.rect.x > 475:
            self.rect.x = -25
            self.rect.y += 80

class Shoot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([6, 18])
        self.image.fill(red)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 5

class Special_Shoot(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface([6, 18])
        self.image.fill(blue)

        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y -= 5
