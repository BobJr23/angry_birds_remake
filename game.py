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

def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)


def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def draw(
        space,
        window,
        draw_options,
        line,
        material,
        orient,
        player_turn,
        building,
        ball,
        player1,
        player2,
):
    window.fill(blue)
    space.debug_draw(draw_options)
    if player_turn == player1 and building:
        pygame.draw.rect(window, grey, (400, 0, width - 400, height))
    elif player_turn == player2 and building:
        pygame.draw.rect(window, grey, (0, 0, width - 400, height))
    if line:
        pygame.draw.line(window, "black", line[0], line[1], 3)

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

def create_ball(space, radius, mass, pos):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    # SHAPE STATS
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (*red, 100)
    shape.elasticity = 0.9
    shape.friction = 0.4
    # ADD TO SIMULATION
    space.add(body, shape)
    return shape

def play():
    player1, player2 = player("p1", 500, []), player("p1", 500, [])
    player_turn = player1
    orient = (16, 80)
    wood = mats(120, 30, brown, "Wood")
    ice = mats(80, 15, blue, "Ice")
    brick = mats(150, 50, black, "Brick")
    material = wood
    run = True
    space = pymunk.Space()
    space.gravity = (0, 980)
    create_boundaries(space, width, height)
    clock = pygame.time.Clock()
    structs = []
    pressed_pos = None
    ball = None
    building = True
    draw_options = pymunk.pygame_util.DrawOptions(window)
    while run:
        line = None
        if ball and pressed_pos:
            line = [
                (100 if player_turn == player1 else 1800, 700),
                pygame.mouse.get_pos(),
            ]
        keys = pygame.key.get_pressed()
        if building:
            if keys[pygame.K_1]:
                material = wood  # wood
            if keys[pygame.K_2]:
                material = ice  # ice
            if keys[pygame.K_3]:
                material = brick  # brick

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if building:  # BUILDING ONLY
                    if event.key == pygame.K_f:
                        if orient == (80, 16):
                            orient = (16, 80)
                        else:
                            orient = (80, 16)
                    elif event.key == pygame.K_RETURN:
                        if player_turn == player1:
                            player_turn = player2
                        else:
                            player_turn = player1
                            building = False
                elif event.key == pygame.K_RETURN:
                    if player_turn == player2:
                        building = True
                    else:
                        player_turn = player2

            if event.type == pygame.MOUSEBUTTONDOWN:
                if building:
                    create_structure(
                        space,
                        (pygame.mouse.get_pos()),
                        orient,
                        (*material.color, 100),
                        material.mass,
                    )
                else:
                    if not ball:
                        ball = create_ball(
                            space,
                            20,
                            50,
                            (100 if player_turn == player1 else 1800, 700),
                        )
                        pressed_pos = pygame.mouse.get_pos()
                        print("waho")
                    elif pressed_pos:
                        ball.body.body_type = pymunk.Body.DYNAMIC
                        angle = calculate_angle(*line)
                        force = calculate_distance(*line) * 50
                        fx = math.cos(angle) * force
                        fy = math.sin(angle) * force
                        ball.body.apply_impulse_at_local_point((fx, fy), (0, 0))
                        pressed_pos = None
                    else:
                        space.remove(ball, ball.body)
                        ball = create_ball(
                            space,
                            20,
                            50,
                            (100 if player_turn == player1 else 1800, 700),
                        )
                        print("yesri")
                        pressed_pos = pygame.mouse.get_pos()

        draw(
            space,
            window,
            draw_options,
            line,
            material,
            orient,
            player_turn,
            building,
            ball,
            player1,
            player2,
        )
        space.step(dt)
        clock.tick(FPS)
    pygame.quit()


if __name__ == "__main__":
    play()
