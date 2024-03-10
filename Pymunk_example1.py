
import random
import sys
import pygame
import pymunk
import pymunk.pygame_util

random.seed(1)
def add_ball(space):
    mass = 1
    radius = 10
    inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
    body = pymunk.Body(mass, inertia)
    body.color = pygame.Color("blue")
    x = random.randint(120, 420)
    body.position = x, 50
    shape = pymunk.Circle(body, radius, (0, 0))
    shape.friction = 1
    space.add(body, shape)
    return shape


def add_L(space):

    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (300, 300)

    rotation_limit_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_limit_body.position = (200, 300)

    body = pymunk.Body(10, 10000)
    body.position = (300, 300)
    l1 = pymunk.Segment(body, (-145, 0), (255.0, 0), 1)
    l2 = pymunk.Segment(body, (-145, 0), (-145.0, -20), 1)
    l3 = pymunk.Segment(body, (255, 0), (255, -20), 1)
    l1.friction = 0.5
    l2.friction = 0.5
    l3.friction = 0.5
    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))
    joint_limit = 20
    rotation_limit_joint = pymunk.SlideJoint(
        body, rotation_limit_body, (-100, 0), (0, 0), 0, joint_limit
    )

    space.add(l1, l2,l3, body, rotation_center_joint, rotation_limit_joint)
    return l1, l2, l3


def main():
    pygame.init()
    screen = pygame.display.set_mode((600, 600))
    pygame.display.set_caption("Basic Physics  ")
    clock = pygame.time.Clock()

    space = pymunk.Space()
    space.gravity = (0.0, 900.0)

    lines = add_L(space)
    balls = []
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    ticks_to_next_ball = 10
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                sys.exit(0)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(screen, "slide_and_pinjoint.png")

        ticks_to_next_ball -= 1
        if ticks_to_next_ball <= 0:
            ticks_to_next_ball = 25
            ball_shape = add_ball(space)
            balls.append(ball_shape)

        balls_to_remove = []
        for ball in balls:
            if ball.body.position.y > 450:
                balls_to_remove.append(ball)

        for ball in balls_to_remove:
            space.remove(ball, ball.body)
            balls.remove(ball)

        space.step(1 / 50.0)

        screen.fill((255, 255, 255))
        space.debug_draw(draw_options)

        pygame.display.flip()
        clock.tick(50)


if __name__ == "__main__":
    main()