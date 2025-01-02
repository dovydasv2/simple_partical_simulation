import math

class Circle_Boundary:
    def __init__(self, pos=(0,0), radius=100, color="white", line_width=1):
        self.pos = pos
        self.radius = radius
        self.color = color
        self.line_width = line_width

    # Returns true if ball collides with boundary
    def collides(self, point, ball_radius):
        return (distance(self.pos, point) + ball_radius) >= self.radius
    
    # Return -1 if ball will not collide for any point in the list, else index it collides
    def will_collide(self, point_list, ball_radius):
        for i in range(len(point_list)):
            if self.collides(point_list[i], ball_radius):
                return i
        return -1
    
    def draw(self, screen, pygame):
        pygame.draw.circle(screen, self.color, self.pos, self.radius, width=self.line_width)


def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)