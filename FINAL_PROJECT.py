import pygame, sys, random
from pygame.math import Vector2

pygame.init()
cell_size = 30
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

def scale_image(image_path):
    image = pygame.image.load(image_path).convert_alpha()
    return pygame.transform.scale(image, (cell_size, cell_size))

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5,10), Vector2(4,10), Vector2(3,10)]
        self.direction = Vector2(1,0)
        self.new_block = False

        # Load gambar kepala sesuai arah
        self.head_up = scale_image(r"C:\Users\ASUS\Music\FINAL\Graphics\head_up.png")
        self.head_down = scale_image(r"C:\Users\ASUS\Music\FINAL\Graphics\head_down.png")
        self.head_right = scale_image(r"C:\Users\ASUS\Music\FINAL\Graphics\head_right.png")
        self.head_left = scale_image(r"C:\Users\ASUS\Music\FINAL\Graphics\head_left.png")

        # Load gambar ekor sesuai arah
        self.tail_up = scale_image(r"C:\Users\ASUS\Music\FINAL\Graphics\tail_up.png")
        self.tail_down = scale_image(r"C:\Users\ASUS\Music\FINAL\Graphics\tail_down.png")
        self.tail_right = scale_image(r"C:\Users\ASUS\Music\FINAL\Graphics\tail_right.png")
        self.tail_left = scale_image(r"C:\Users\ASUS\Music\FINAL\Graphics\tail_left.png")

        # Load gambar badan
        self.body_vertical = scale_image(r"C:\Users\ASUS\Music\FINAL\Graphics\body_vertical.png")
        self.body_horizontal = scale_image(r"C:\Users\ASUS\Music\FINAL\Graphics\body_horizontal.png")
        self.body_tr = scale_image(r"C:\Users\ASUS\Music\FINAL\Graphics\body_tr.png")
        self.body_tl = scale_image(r"C:\Users\ASUS\Music\FINAL\Graphics\body_tl.png")
        self.body_br = scale_image(r"C:\Users\ASUS\Music\FINAL\Graphics\body_br.png")
        self.body_bl = scale_image(r"C:\Users\ASUS\Music\FINAL\Graphics\body_bl.png")

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:  # Kepala ular
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:  # Ekor ular
                screen.blit(self.tail, block_rect)
            else:  # Tubuh ular
                previous_block = self.body[index - 1] - block
                next_block = self.body[index + 1] - block

                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if (previous_block.x == -1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == -1):
                        screen.blit(self.body_tl, block_rect)
                    elif (previous_block.x == -1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == -1):
                        screen.blit(self.body_bl, block_rect)
                    elif (previous_block.x == 1 and next_block.y == -1) or (previous_block.y == -1 and next_block.x == 1):
                        screen.blit(self.body_tr, block_rect)
                    elif (previous_block.x == 1 and next_block.y == 1) or (previous_block.y == 1 and next_block.x == 1):
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1,0):
            self.head = self.head_left
        elif head_relation == Vector2(-1,0):
            self.head = self.head_right
        elif head_relation == Vector2(0,1):
            self.head = self.head_up
        elif head_relation == Vector2(0,-1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1,0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1,0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0,1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0,-1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block:
            self.body.insert(0, self.body[0] + self.direction)
            self.new_block = False
        else:
            self.body.pop()
            self.body.insert(0, self.body[0] + self.direction)

    def add_block(self):
        self.new_block = True

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.pos = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.score = 0

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def draw_grass(self):
        grass_color1 = (167, 209, 61)
        grass_color2 = (157, 198, 52)

        for row in range(cell_number):
            for col in range(cell_number):
                if (row + col) % 2 == 0:
                    pygame.draw.rect(screen, grass_color1, (col * cell_size, row * cell_size, cell_size, cell_size))
                else:
                    pygame.draw.rect(screen, grass_color2, (col * cell_size, row * cell_size, cell_size, cell_size))

    def draw_score(self):
        score_surface = font.render(f"Score: {self.score}", True, (56, 74, 12))
        screen.blit(score_surface, (10, 10))

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
            self.score += 1

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()

    def game_over(self):
        pygame.quit()
        sys.exit()

apple = scale_image(r'C:\Users\ASUS\Music\FINAL\Graphics\mouse.png')

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_game = MAIN()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and main_game.snake.direction.y != 1:
                main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_RIGHT and main_game.snake.direction.x != -1:
                main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_DOWN and main_game.snake.direction.y != -1:
                main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_LEFT and main_game.snake.direction.x != 1:
                main_game.snake.direction = Vector2(-1, 0)

    screen.fill((175,215,70))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)