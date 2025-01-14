import math

class Ball:
    def __init__(self, position, radius, color, balls_list, pygame, screen, acceleration_x=0, acceleration_y=0, elasticity_coefficient=1):
        self.prev_pos = position
        self.position = position # Current position
        self.next_pos = position
        self.radius = radius
        self.mass = radius**2
        self.color = color
        self.pygame = pygame
        self.screen = screen
        self.vx = 0
        self.vy = 0
        self.ax = acceleration_x
        self.ay = acceleration_y
        self.queued_move = False
        self.elasticity_coefficient = elasticity_coefficient
        balls_list.append(self)

    def draw(self):
        self.pygame.draw.circle(self.screen, self.color, self.position, self.radius)

    def draw_velocity(self):
        self.pygame.draw.line(self.screen, self.color, self.position, (self.position[0] + self.vx, self.position[1] + self.vy), 1)

    def move(self, delta_x, delta_y):
        self.position = (self.get_x() + delta_x, self.get_y() + delta_y)

    def move_to(self, x, y):
        self.position = (x, y)

    def set_acceleration(self, accel_x, accel_y):
        self.ax = accel_x
        self.ay = accel_y

    def apply_acceleration(self, accel_x, accel_y):
        self.vx += accel_x
        self.vy += accel_y

    def find_path(self, substeps):
        path = []
        og_pos = self.position
        vx = self.vx
        vy = self.vy

        for i in range(1, substeps + 1):
            path.append((og_pos[0] + (vx * (i / substeps)), og_pos[1] + (vy * (i / substeps))))

        return path
    
    # Assume new velocity is already set for the ball. Returns remaining substeps after a collision
    def find_new_substeps(self, substep, substep_index, total_substeps):
        remaining_substeps = total_substeps - substep_index
        path = []

        if remaining_substeps == 0:
            return path
        
        scaled_down_velocity = scalar_mult(remaining_substeps / total_substeps, self.velocity())
        for i in range(1, remaining_substeps + 1):
            path.append(add_vectors(substep, (scaled_down_velocity[0] * (i / remaining_substeps), scaled_down_velocity[1] * (i / remaining_substeps))))

        return path
        

    def collide_circle_boundary(self, boundary, position):
        # Find normalized normal vector of collision
        point_of_collision = position
        normal_vector = invert_vector(get_unit_vector((self.position[0] - boundary.pos[0], self.position[1] - boundary.pos[1])))
        overlap = distance(boundary.pos, self.position) + self.radius - boundary.radius

        if overlap > 0:
            ball_pos = add_vectors(self.position, scalar_mult(overlap, normal_vector))
            self.move_to(ball_pos[0], ball_pos[1])

        normal_vector = invert_vector(get_unit_vector((self.position[0] - boundary.pos[0], self.position[1] - boundary.pos[1])))
        new_velocity = scalar_mult(self.elasticity_coefficient, reflect_vector_about(normal_vector, (self.vx, self.vy)))

        self.vx = new_velocity[0]
        self.vy = new_velocity[1] 

    def collides_point(self, point):
        return self.distance_from_center(point) <= self.radius
    
    def collides_ball(self, ball):
        return distance(self.position, ball.position) < self.radius + ball.radius
    
    def velocity(self):
        return (self.vx, self.vy)
    
    def set_velocity(self, velocity):
        self.vx = velocity[0]
        self.vy = velocity[1]

    # Returns a list of tuples [v1, v2] (One v for each ball)
    def ball_collision_velocity(self, pos1, pos2, other):
        overlap = (self.radius + other.radius) - distance(pos1, pos2)
        normal = (pos2[0] - pos1[0], pos2[1] - pos1[1])
        ball_pos = pos1
        other_pos = pos2
        if overlap > 0:
            dist = vector_magnitude(normal)
            if dist != 0:
                hat_n = get_unit_vector(normal)
                total_inv_mass = (1 / self.mass) + (1 / other.mass)

                ball_pos = subtract_vectors(pos1, scalar_mult(overlap * (1 / self.mass) / total_inv_mass, hat_n))
                self.move_to(ball_pos[0], ball_pos[1])

                other_pos = add_vectors(pos2, scalar_mult(overlap * (1 / other.mass) / total_inv_mass, hat_n))
                other.move_to(other_pos[0], other_pos[1])
        
        unit_normal = get_unit_vector((other_pos[0] - ball_pos[0], other_pos[1] - ball_pos[1]))
        inv_mass_ball = 1 / self.mass
        inv_mass_other = 1 / other.mass
        delta_v = scalar_mult((-(1 + self.elasticity_coefficient)) * (dot_product(subtract_vectors(self.velocity(), other.velocity()), unit_normal)) / (inv_mass_ball + inv_mass_other), unit_normal)
        new_v1 = add_vectors(self.velocity(), scalar_mult(inv_mass_ball, delta_v))
        new_v2 = subtract_vectors(other.velocity(), scalar_mult(inv_mass_other, delta_v))

        return [new_v1, new_v2]


    def resolve_ball_to_ball(self, ball):
        collision_vector = get_unit_vector((self.position[0] - ball.position[0], self.position[1] - ball.position[1]))
        inverse_mass = 1 / self.mass

        scaled_collision = scalar_mult(inverse_mass * ball.mass * self.elasticity_coefficient * (abs(vector_magnitude((self.vx, self.vy)) - vector_magnitude((ball.vx, ball.vy)))), collision_vector)

        new_velocity_x = self.vx + scaled_collision[0]
        new_velocity_y = self.vy + scaled_collision[1]

        self.vx = new_velocity_x
        self.vy = new_velocity_y
        
        self.queued_move = True

    def move_queued(self):
        if self.queued_move:
            self.move(self.vx, self.vy)
            self.queued_move = False
        


    
    """def resolve_collision_point(self, point):
        # Find unit vector from center of ball to the point
        unit_vector = get_unit_vector((self.x_dist_from_center(point), self.y_dist_from_center(point)))

        self.collision_temp_x = self.position[0] - (int(unit_vector[0] * self.x_dist_from_center(point)))
        self.collision_temp_y = self.position[1] - (int(unit_vector[1] * self.y_dist_from_center(point)))
        #self.position = ((self.position[0] + (unit_vector[0] * self.radius)), (self.position[1] + (unit_vector[1] * self.radius)))

        self.vx = self.vx * (unit_vector[0]) * self.elasticity_coefficient
        self.vy = self.vy * (unit_vector[1]) * self.elasticity_coefficient

    def check_collision_point(self, point):
        if self.collides_point(point):
            self.resolve_collision_point(point)
            self.collision = True"""

    def update(self):
        self.move(self.vx, self.vy)

    def get_x(self):
        return self.position[0]
    
    def get_y(self):
        return self.position[1]
    
    def distance_from_center(self, position):
        return math.sqrt((self.get_x() - position[0])**2 + (self.get_y() - position[1])**2)
    
    # Directional
    def x_dist_from_center(self, position):
        return self.get_x() - position[0]
    
    # Directional
    def y_dist_from_center(self, position):
        return self.get_y() - position[1]
    
    def onscreen(self, screen):
        return (self.position[0] > 0 and self.position[0] < screen.get_width()) and (self.position[1] > 0 and self.position[1] < screen.get_height())










def vector_magnitude(vector):
    return math.sqrt((vector[0]**2) + (vector[1]**2))

def get_unit_vector(vector):
    magnitude = vector_magnitude(vector)
    if magnitude != 0:
        return ((vector[0] / magnitude), (vector[1] / magnitude))
    return (vector[0], vector[1])

def invert_vector(vector):
    return (-vector[0], -vector[1])

def dot_product(v1, v2):
    return (v1[0]*v2[0]) + (v1[1]*v2[1])

def add_vectors(v1, v2):
    return (v1[0] + v2[0], v1[1] + v2[1])

def subtract_vectors(v1, v2):
    return (v1[0] - v2[0], v1[1] - v2[1])

def scalar_mult(scalar, vector):
    return (scalar*vector[0], scalar*vector[1])

def reflect_vector_about(normal, vector):
    # normal pointing in direction of reflection
    right = scalar_mult(2*(dot_product(normal, vector)), normal)
    return (vector[0]-right[0], vector[1]-right[1])

def distance(p1, p2):
    return math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)

