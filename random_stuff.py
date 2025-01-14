import math
import pygame
from pygame import Color
import random
from custom_objects.ball import Ball
from custom_objects.circle_boundary import Circle_Boundary

substeps = 5
gravity = 0.02

def draw_balls(balls_list):
    for ball in balls_list:
        ball.draw()

def draw_velocity_vectors(balls_list):
    for ball in balls_list:
        ball.draw_velocity()


def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

        
def check_ball_collisions(balls_list: list[Ball], boundary: Circle_Boundary):
    for ball in balls_list:
        # If ball off screen, get rid of it from the ball list
        if not ball.onscreen(screen):
            balls_list.remove(ball)
            continue

    for substep in range(substeps):
        for ball in balls_list:
            # Apply acceleration from gravity
            ball.apply_acceleration(ball.ax, ball.ay)

            for other_ball in [x for x in balls_list if x != ball]:
                if distance(ball.position, other_ball.position) < (ball.radius + other_ball.radius):
                    # Collision
                    # Calculate new resultant velocity
                    new_velocities = ball.ball_collision_velocity(ball.position, other_ball.position, other_ball)
                    ball.set_velocity(new_velocities[0])
                    other_ball.set_velocity(new_velocities[1])

            if boundary.collides(ball.position, ball.radius):
                # Update the ball velocity and position if it collides with the boundary
                ball.collide_circle_boundary(boundary, ball.position)


        for ball in balls_list:
            ball.move(ball.vx, ball.vy)

    
        

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1920, 1080))
clock = pygame.time.Clock()
running = True


middle_pos = (screen.get_width() / 2, screen.get_height() / 2)

balls_list = []

ball_paths = {}

boundary = Circle_Boundary(middle_pos, 500, "white", 1)


#ball1 = Ball(middle_pos, 5, "red", balls_list, pygame, screen, 0, 0.01, elasticity_coefficient=0.9)

#ball2 = Ball((middle_pos[0] + 20, middle_pos[1]), 10, "orange", balls_list, pygame, screen, 0, 0.1)

#print(screen.get_height() * 2 / 3)

dragging = False
hue = 0
hue_increasing = True


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left mouse button
                pos = pygame.mouse.get_pos()
                if boundary.in_bounds(pos):
                    if hue == 360:
                        hue_increasing = False
                    elif hue == 0:
                        hue_increasing = True

                    if hue_increasing:
                        hue += 1
                    else:
                        hue -= 1
                    
                    color = Color(0, 0, 0, 0)
                    color.hsla = (hue, 100, 50, 100)
                    # random.randrange(1, 10)
                    ball = Ball(pos, 10, color, balls_list, pygame, screen, acceleration_y=gravity, elasticity_coefficient=0.9)
                

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                dragging = False

    if dragging:
        pos = pygame.mouse.get_pos()
        if boundary.in_bounds(pos):
            if hue == 360:
                hue_increasing = False
            elif hue == 0:
                hue_increasing = True

            if hue_increasing:
                hue += 1
            else:
                hue -= 1
            
            color = Color(0, 0, 0, 0)
            color.hsla = (hue, 100, 50, 100)
            # random.randrange(1, 10)
            ball = Ball(pos, 10, color, balls_list, pygame, screen, acceleration_y=gravity, elasticity_coefficient=0.9)

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

