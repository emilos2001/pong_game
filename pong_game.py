import random
import pygame as pg
import sys

pg.init()
WIDTH, HEIGHT = 1200, 900
BALL_WIDTH, BALL_HEIGHT = 50, 50
BALL_X, BALL_Y = WIDTH // 2, HEIGHT // 2
FIRST_LINE = WIDTH // 3
SECOND_LINE = WIDTH // 2
THIRD_LINE = WIDTH - 400
MARGIN_LINE = HEIGHT // 23
screen = pg.display.set_mode((WIDTH, HEIGHT))
clock = pg.time.Clock()
back_ground = (102, 153, 153)
score_player1 = 0
score_player2 = 0


class Ball(pg.Rect):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.random = random.Random()
        self.ball_color = (204, 122, 0)
        self.speed_ball = 1
        self.radius = 15
        self.x_velocity = 0
        self.y_velocity = 0
        self.movement()

    def movement(self):
        random_x_direction = self.random.randint(0, 1) * 2 - 1
        random_y_direction = self.random.randint(0, 1) * 2 - 1
        self.x_velocity = random_x_direction * self.speed_ball
        self.y_velocity = random_y_direction * self.speed_ball

    def move_ball(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        if self.colliderect(rackets.left_racket):
            self.x_velocity = abs(self.x_velocity) + self.speed_ball + 1.5
        if self.colliderect(rackets.right_racket):
            self.x_velocity = -abs(self.x_velocity) - self.speed_ball - 1.5
        if self.colliderect(rackets.back_right_racket):
            self.x_velocity = abs(self.x_velocity) + self.speed_ball + 1.5
        if self.colliderect(rackets.back_left_racket):
            self.x_velocity = -abs(self.x_velocity) - self.speed_ball - 1.5

    def reset(self, window_width, window_height):
        if self.right >= window_width or self.left <= 0:
            self.x = window_width // 2
            self.y = window_height // 2
            rackets.left_x = 15
            rackets.right_x = window_width - 25
            rackets.left_y = window_height // 2
            rackets.right_y = window_height // 2
            self.movement()

    def score(self, window_width, window):
        global score_player1, score_player2
        font = pg.font.Font(None, 35)
        if self.right >= window_width:
            self.right = window_width
            score_player1 += 1

        if self.left <= 0:
            self.left = 0
            score_player2 += 1

        player1 = (font.render(f"player 1               {score_player1}", True, 'white'))
        player2 = (font.render(f"{score_player2}               player 2", True, 'white'))
        window.blit(player1, (FIRST_LINE - player1.get_width() // 2, HEIGHT // 100))
        window.blit(player2, (THIRD_LINE - player2.get_width() // 2, HEIGHT // 100))
    def stop_ball(self, window_height):
        if self.bottom >= window_height:
            self.bottom = window_height
            self.y_velocity = -self.speed_ball * 1.2
        if self.top <= MARGIN_LINE:
            self.top = MARGIN_LINE
            self.y_velocity = self.speed_ball * 1.2

    def draw_ball(self, window):
        pg.draw.circle(window, self.ball_color, self.center, self.radius)


class Rackets(pg.Rect):
    def __init__(self, width, height):
        super().__init__(0, 0, width, height)
        self.back_right_racket = None
        self.back_left_racket = None
        self.right_racket = None
        self.left_racket = None
        self.left_width = 15
        self.right_width = 15
        self.height = 125
        self.right_x = width - 25
        self.right_y = (height // 2) - 50
        self.left_x = 15
        self.left_y = (height // 2) - 50
        self.left_speedX = 7
        self.left_speedY = 10
        self.right_speedX = 7
        self.right_speedY = 10
        self.w_pressed = False
        self.s_pressed = False
        self.d_pressed = False
        self.a_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.right_pressed = False
        self.left_pressed = False

    def update(self, **kwargs):
        # wasd
        if self.w_pressed:
            self.left_y -= self.left_speedY
        elif self.s_pressed:
            self.left_y += self.left_speedY
        elif self.a_pressed:
            self.left_x -= self.left_speedX
        elif self.d_pressed:
            self.left_x += self.left_speedX
        # wasd stop at margins
        if self.left_y >= HEIGHT - self.height:
            self.left_y = HEIGHT - self.height
        if self.left_y <= MARGIN_LINE:
            self.left_y = MARGIN_LINE
        if self.left_x >= FIRST_LINE - self.left_width:
            self.left_x = FIRST_LINE - self.left_width
        if self.left_x <= 0:
            self.left_x = 0

        # arrow
        if self.up_pressed:
            self.right_y -= self.right_speedY
        elif self.down_pressed:
            self.right_y += self.right_speedY
        elif self.left_pressed:
            self.right_x -= self.right_speedX
        elif self.right_pressed:
            self.right_x += self.right_speedX

        # arrow stop at margin
        if self.right_y >= HEIGHT - self.height:
            self.right_y = HEIGHT - self.height
        if self.right_y <= MARGIN_LINE:
            self.right_y = MARGIN_LINE
        if self.right_x <= THIRD_LINE:
            self.right_x = THIRD_LINE
        if self.right_x >= WIDTH - self.right_width:
            self.right_x = WIDTH - self.right_width

    def draw_rackets(self, window):
        self.left_racket = (self.left_x, self.left_y, self.left_width // 2, self.height)
        self.back_left_racket = (self.left_x - self.left_width // 2, self.left_y, self.left_width // 2, self.height)
        self.right_racket = (self.right_x, self.right_y, self.right_width // 2, self.height)
        self.back_right_racket = (
            self.right_x + self.right_width // 2, self.right_y, self.right_width // 2, self.height)
        pg.draw.rect(window, '#ffbf00', self.left_racket)  # the front side of left racket
        pg.draw.rect(window, '#000000', self.back_left_racket)  # the back side of right racket
        pg.draw.rect(window, '#73E600', self.right_racket)  # the front side of left racket
        pg.draw.rect(window, '#000000', self.back_right_racket)  # the back side of left racket


rackets = Rackets(WIDTH, HEIGHT)
balls = Ball(BALL_X, BALL_Y, BALL_WIDTH, BALL_HEIGHT)
running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            # arrow move
            if event.key == pg.K_UP:
                rackets.up_pressed = True
            elif event.key == pg.K_DOWN:
                rackets.down_pressed = True
            elif event.key == pg.K_LEFT:
                rackets.left_pressed = True
            elif event.key == pg.K_RIGHT:
                rackets.right_pressed = True
            # wasd move
            if event.key == pg.K_w:
                rackets.w_pressed = True
            elif event.key == pg.K_s:
                rackets.s_pressed = True
            elif event.key == pg.K_a:
                rackets.a_pressed = True
            elif event.key == pg.K_d:
                rackets.d_pressed = True
        elif event.type == pg.KEYUP:
            # arrow stop
            if event.key == pg.K_UP:
                rackets.up_pressed = False
            elif event.key == pg.K_DOWN:
                rackets.down_pressed = False
            elif event.key == pg.K_LEFT:
                rackets.left_pressed = False
            elif event.key == pg.K_RIGHT:
                rackets.right_pressed = False
            # wasd stop
            if event.key == pg.K_w:
                rackets.w_pressed = False
            elif event.key == pg.K_s:
                rackets.s_pressed = False
            elif event.key == pg.K_a:
                rackets.a_pressed = False
            elif event.key == pg.K_d:
                rackets.d_pressed = False
    rackets.update()
    screen.fill(back_ground)
    rackets.draw_rackets(screen)
    pg.draw.line(screen, "#b3cccc", (FIRST_LINE, 0), (FIRST_LINE, HEIGHT), 3)
    pg.draw.line(screen, "#ffffff", (SECOND_LINE, 0), (SECOND_LINE, HEIGHT), 5)
    pg.draw.line(screen, "#ffffff", (0, MARGIN_LINE), (WIDTH, MARGIN_LINE), 5)
    pg.draw.line(screen, "#b3cccc", (THIRD_LINE, 0), (THIRD_LINE, HEIGHT), 3)
    balls.score(WIDTH, screen)
    balls.move_ball()
    balls.reset(WIDTH, HEIGHT)
    balls.stop_ball(HEIGHT)
    balls.draw_ball(screen)
    pg.display.flip()
    clock.tick(60)
