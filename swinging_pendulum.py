import pymunk as pm
import pygame as pg
import pymunk.pygame_util
import math
import random as rd

pg.init()

WIDTH, HEIGHT = 1000, 800
WIN = pg.display.set_mode((WIDTH, HEIGHT))

def draw(space, WIN, draw_options):
    WIN.fill((255, 255, 255))

    space.debug_draw(draw_options)

    pg.display.update()


def create_pendulum(space, mouse_pos):
    joint_body = pm.Body(body_type=pm.Body.STATIC)
    joint_body.position = mouse_pos

    body = pm.Body()
    body.position = mouse_pos

    line = pm.Segment(body, (0, 0), (255, 0), 5)
    circle = pm.Circle(body, 40, (255, 0))

    line.friction = 1
    circle.friction = 1
    line.mass = 8
    circle.mass = 30
    circle.elasticity = 0.95

    joint = pm.PinJoint(body, joint_body, (0, 0), (0, 0))

    space.add(circle, line, body, joint)

    





def run(WIN, width, height):
    run = True
    clock = pg.time.Clock()
    space = pymunk.Space()
    space.gravity = ((0, 981))
    
    fps = 60
    dt = 1/fps

    
    

    draw_options = pymunk.pygame_util.DrawOptions(WIN)
    pendulum = None

    

    

    while run:
        

        

        clock.tick(fps)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            elif event.type == pg.MOUSEBUTTONDOWN:
                if pendulum is None:
                    mouse_pos = pg.mouse.get_pos()
                    pendulum = create_pendulum(space, mouse_pos)
                else:
                    #space.remove(pendulum.body, pendulum) # doesnt work
                    pendulum = None
         
        
        draw(space, WIN, draw_options)
        space.step(dt)

        
        pg.display.update()

    pg.quit()


if __name__ == '__main__':
    run(WIN, WIDTH, HEIGHT)