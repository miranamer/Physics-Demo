#.\physx\Scripts\activate
# IF YOU GET ERROR MODULE NOT FOUND -> INSTALL IN CMD / POWERSHELL AND IT SHOULD WORK
# Why Are You Looking At My Achievements????



from msilib.schema import MsiAssembly
from venv import create
import matplotlib.pyplot as plt
import pymunk
import pygame as pg
import pymunk.pygame_util
import math
import random as rd


pg.init()

WIDTH, HEIGHT = 1000, 800
WIN = pg.display.set_mode((WIDTH, HEIGHT))

def calc_distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def calc_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def draw(space, WIN, draw_options, line):
    WIN.fill((255, 255, 255))
    if line:
        pg.draw.line(WIN, (0, 0, 0), line[0], line[1], 3)

    space.debug_draw(draw_options)

    pg.display.update()

def add_block(space, size): # static block at rand positions
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    pos1 = rd.randint(100, 800)
    pos2 = rd.randint(100, 800)
    body.position = (pos1, pos2)
    shape = pymunk.Poly.create_box(body, size)
    shape.elasticity = 0.4
    shape.friction = 0.35
    space.add(body, shape)

    return shape


def add_structure(space, width, height):
    body = pymunk.Body()
    pos1 = rd.randint(30, 870)
    body.position = (pos1, height - 120)
    size_w = rd.randint(40, 60)
    size_h = rd.randint(150, 200)
    shape = pymunk.Poly.create_box(body, (size_w, size_h))
    shape.mass = size_w * 2.5
    shape.elasticity = 0.4
    shape.friction = 0.4
    space.add(body, shape)

    return shape


def create_boundaries(space, width, height):
    rects = [
        [(width / 2, height - 10), (width, 20)], # Position, Size
        [(width / 2, 10), (width, 20)],
        [(10, height / 2), (20, height)],
        [(width - 10, height / 2), (20, height)]
    ]

    for pos, size in rects:
        body = pymunk.Body(body_type = pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.35
        space.add(body, shape)


def add_object(space, radius, mass, pos):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos # centre of body
    
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.color = (255, 0, 0, 100) # final arg = opacity
    space.add(body, shape) # shape is attached to body
    shape.elasticity = 1
    shape.friction = 0.35
    
    return shape



def run(WIN, width, height):
    run = True
    clock = pg.time.Clock()
    
    space = pymunk.Space()
    space.gravity = ((0, 981))
    
    fps = 60
    dt = 1/fps

    
    create_boundaries(space, width, height)

    draw_options = pymunk.pygame_util.DrawOptions(WIN)

    rand_force = [-10000, 10000]

    ball = None
    block = None
    pressed_pos = None
    structure = None

    while run:
        line = None

        if ball and pressed_pos:
            line = [pressed_pos, pg.mouse.get_pos()]

        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            if event.type == pg.MOUSEBUTTONDOWN:
                if not ball and not block and not structure:
                    rand_val = rd.randint(1, 3)
                    pressed_pos = pg.mouse.get_pos()
                    ball = add_object(space, 30, 10, pressed_pos)
                    structure = add_structure(space, width, height)
                    
                    t = [] # will store the blocks
                    for _ in range(rand_val):
                        block = add_block(space, (100, 100))
                        t.append(block)
                
                elif pressed_pos:
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    angle = calc_angle(*line)
                    force = calc_distance(*line) * 100 # resultant force
                    fx = math.cos(angle) * force # horizontal force
                    fy = math.sin(angle) * force # vertical force
                    ball.body.apply_impulse_at_local_point((fx, fy), (0, 0))
                    pressed_pos = None
                
                else:
                    space.remove(ball, ball.body)
                    
                    for i in range(len(t)):
                        space.remove(t[i])
                    
                    space.remove(structure, structure.body)
                    ball = None
                    block = None
                    structure = None
                    
                    
                    
            

                

        
        draw(space, WIN, draw_options, line)
        space.step(dt)

        
        pg.display.update()

    pg.quit()

#elif event.button == 3: # right click
    #ball.body.apply_impulse_at_local_point((0, 10000), (0, 0))

#if event.type == pg.MOUSEBUTTONDOWN:
                #if event.button == 1: # left click
                    #val = rd.randint(0, 1)
                    #ball.body.apply_impulse_at_local_point((rand_force[val], rand_force[val]), (0, 0))

if __name__ == '__main__':
    run(WIN, WIDTH, HEIGHT)

