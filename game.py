import pygame
import pymunk
import pymunk.pygame_util
import math, time, sys

pygame.init()
width, height = 1900, 900
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Furious Birds!")
white = (255, 255, 255)
green = (50, 168, 82)
black = (0, 0, 0)
red = (200, 0, 0)
grey = (105, 105, 105)
blue = (66, 185, 189)
brown = (133, 64, 65)

bird_sprite = pygame.transform.scale(
    pygame.image.load(r"angrybird.png"),
    (47, 47),
)
FONT = pygame.font.Font(None, 40)

class player:
    def __init__(self, name, gold=int, birds=list):
        self.name = name
        self.gold = gold
        self.birds = birds


class mats:
    def __init__(self, mass, cost, color, name):
        self.mass = mass
        self.cost = cost
        self.color = color
        self.name = name

def play():
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    pygame.quit()

if __name__ == "__main__":
    play()