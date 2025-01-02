import pygame
import random
from custom_objects.ball import Ball
from custom_objects.circle_boundary import Circle_Boundary

substeps = 15

def draw_balls(balls_list):
    for ball in balls_list:
        ball.draw()

def draw_velocity_vectors(balls_list):
    for ball in balls_list:
        ball.draw_velocity()

def collide_balls_point(balls_list, point):
    for ball in balls_list:
        ball.check_collision_point(point)

def collide_balls_line(balls_list, line_y):
    for ball in balls_list:
        ball.check_collision_point((ball.get_x(), line_y))


def check_ball_collisions(balls_list: list[Ball], boundary: Circle_Boundary):
    for ball in balls_list:
        # If ball of screen, get rid of it from the ball list
        if not ball.onscreen(screen):
            balls_list.remove(ball)
            continue
        
        ball.apply_acceleration(ball.ax, ball.ay)
        path = ball.find_path(substeps)
        collide_index = boundary.will_collide(path, ball.radius)
        # If ball collides with the boundary:
        if collide_index != -1:
            ball.collide_circle_boundary(boundary, path, collide_index)
        else:
            ball.update()


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


middle_pos = (screen.get_width() / 2, screen.get_height() / 2)

balls_list = []

boundary = Circle_Boundary(middle_pos, 250, "white", 1)


#ball1 = Ball(middle_pos, 5, "red", balls_list, pygame, screen, 0, 0.01, elasticity_coefficient=0.9)

#ball2 = Ball((middle_pos[0] + 20, middle_pos[1]), 10, "orange", balls_list, pygame, screen, 0, 0.1)

#print(screen.get_height() * 2 / 3)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            ball = Ball(pos, random.randrange(5, 10), (random.randrange(255),random.randrange(255),random.randrange(255)), balls_list, pygame, screen, acceleration_y=0.25, elasticity_coefficient=0.9)

    # RENDER GAME HERE
    # Clear screen
    screen.fill("black")

    boundary.draw(screen, pygame)

    check_ball_collisions(balls_list, boundary)
    draw_balls(balls_list)
    #draw_velocity_vectors(balls_list)

    # flip() the dipslay to put your work on screen
    pygame.display.flip()

    clock.tick(60) # limits FPS

pygame.quit()

