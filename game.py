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
FPS = 60
dt = 1 / FPS


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


def draw(space, window, draw_options):
    window.fill(blue)
    space.debug_draw(draw_options)

    pygame.display.update()


def create_boundaries(space, width, height):
    rects = [
        [(width / 2, height - 10), (width, 20)],
        # [(width / 2, 10), (width, 20)],
        # [(10, height / 2), (20, height)],
        # [(width - 10, height / 2), (20, height)],
    ]
    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos

        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)


def create_structure(space, pos, size, color, mass):
    body = pymunk.Body()
    body.position = pos
    shape = pymunk.Poly.create_box(body, size, radius=1)
    shape.color = color
    shape.mass = mass
    shape.elasticity = 0.4
    shape.friction = 0.4
    space.add(body, shape)
    return shape


def play():
    run = True
    space = pymunk.Space()
    space.gravity = (0, 980)
    create_boundaries(space, width, height)
    clock = pygame.time.Clock()
    draw_options = pymunk.pygame_util.DrawOptions(window)
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        draw(space, window, draw_options)
        space.step(dt)
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    play()
