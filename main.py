import random
import sys
import pygame
from pygame.math import Vector2


class Snake:
    def __init__(self):
        self.head = None
        self.middle = None
        self.tail = None
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(0, 0)
        self.new_block = False

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()
        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')

    def draw_snake(self):
        self.update_head()
        self.update_tail()
        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                prev_block = self.body[index - 1] - block
                next_block = self.body[index + 1] - block
                self.update_middle(prev_block, next_block)
                screen.blit(self.middle, block_rect)

    def update_head(self):
        if self.direction == (1, 0):
            self.head = self.head_right
        elif self.direction == (-1, 0):
            self.head = self.head_left
        elif self.direction == (0, -1):
            self.head = self.head_up
        elif self.direction == (0, 1):
            self.head = self.head_down
        elif self.direction == (0, 0):
            self.head = self.head_right

    def update_tail(self):
        direction = self.body[-1] - self.body[-2]
        if direction == (1, 0):
            self.tail = self.tail_right
        elif direction == (-1, 0):
            self.tail = self.tail_left
        elif direction == (0, -1):
            self.tail = self.tail_up
        elif direction == (0, 1):
            self.tail = self.tail_down
        elif direction == (0, 0):
            self.tail = self.tail_right

    def update_middle(self, prev_block, next_block):
        if next_block.y == prev_block.y:
            self.middle = self.body_horizontal
        elif next_block.x == prev_block.x:
            self.middle = self.body_vertical
        elif (prev_block.x == -1 and next_block.y == -1) or (prev_block.y == -1 and next_block.x == -1):
            self.middle = self.body_tl
        elif (prev_block.x == -1 and next_block.y == 1) or (prev_block.y == 1 and next_block.x == -1):
            self.middle = self.body_bl
        elif (prev_block.x == 1 and next_block.y == -1) or (prev_block.y == -1 and next_block.x == 1):
            self.middle = self.body_tr
        elif (prev_block.x == 1 and next_block.y == 1) or (prev_block.y == 1 and next_block.x == 1):
            self.middle = self.body_br

    def move_snake(self):
        if self.direction == (0, 0):
            pass
        elif self.new_block:
            self.body.insert(0, self.body[0] + self.direction)
            self.new_block = False
        else:
            self.body.pop(-1)
            self.body.insert(0, self.body[0] + self.direction)

    def add_block(self):
        self.play_crunch_sound()
        self.new_block = True

    def play_crunch_sound(self):
        self.crunch_sound.play()

    def reset(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(0, 0)


class Fruit:
    def __init__(self):
        self.x = random.randint(0, cell_number-1)
        self.y = random.randint(0, cell_number-1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)


class MAIN:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.game_over_sound = pygame.mixer.Sound('Sound/GameOver.wav')

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        self.check_success()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    @staticmethod
    def draw_grass():
        grass_color = (167, 209, 61)
        for col in range(0, cell_number):
            for row in range(0, cell_number):
                x_pos = int(col * cell_size)
                y_pos = int(row * cell_size)
                grass_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
                if (col + row) % 2 == 0:
                    pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (56, 74, 12))

        # top-left position
        score_rect = score_surface.get_rect(center=(6 + cell_size / 2, 6 + cell_size / 2))

        # bottom right position
        # score_rect = score_surface.get_rect(center=(cell_size*cell_number - 60, cell_size*cell_number - 30))

        apple_rect = apple.get_rect(midleft=(score_rect.right, score_rect.centery))
        bg_rect = pygame.Rect(score_rect.left - 6, score_rect.top - 12,
                              score_rect.width + apple_rect.width + 6, apple_rect.height)

        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 12), bg_rect, 2)

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            # if the fruit is inside the snake, keep randomizing
            invalid_pos = True
            while invalid_pos:
                invalid_pos = False
                self.fruit.randomize()
                for block in self.snake.body[1:]:
                    if block == self.fruit.pos:
                        invalid_pos = True
            self.snake.add_block()

    def check_fail(self):
        if (not 0 <= self.snake.body[0].x < cell_number) or \
           (not 0 <= self.snake.body[0].y < cell_number):
            pass
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                pass
                self.game_over()

    def check_success(self):
        if len(self.snake.body) == cell_number * cell_number:
            print("you won!")
            self.game_over()

    def game_over(self):
        print(len(self.snake.body) - 3)
        self.play_game_over_sound()
        self.fruit = Fruit()
        self.snake.reset()

    def play_game_over_sound(self):
        self.game_over_sound.play()


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

cell_size = 36
cell_number = 20

screen = pygame.display.set_mode((cell_size * cell_number, cell_size * cell_number))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font(None, 25)

main_game = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.body[0].x != main_game.snake.body[1].x:
                main_game.snake.direction = Vector2(0, -1)
            elif event.key == pygame.K_DOWN and main_game.snake.body[0].x != main_game.snake.body[1].x:
                main_game.snake.direction = Vector2(0, 1)
            elif event.key == pygame.K_RIGHT and main_game.snake.body[0].y != main_game.snake.body[1].y:
                main_game.snake.direction = Vector2(1, 0)
            elif event.key == pygame.K_LEFT and main_game.snake.body[0].y != main_game.snake.body[1].y:
                main_game.snake.direction = Vector2(-1, 0)
    screen.fill((175, 215, 70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)
