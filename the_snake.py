"""Классическая игра «Змейка» с переходом через границы поля."""

from random import randint

import pygame

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_COLOR = (255, 0, 0)
SNAKE_COLOR = (0, 255, 0)
SPEED = 20

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


class GameObject:
    """Базовый объект с позицией и цветом на игровом поле."""

    def __init__(self):
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Определить отрисовку объекта в дочернем классе."""
        pass


class Apple(GameObject):
    """Яблоко, которое увеличивает длину змейки."""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Выбрать случайную клетку внутри игрового поля."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )

    def draw(self):
        """Нарисовать яблоко и границу его клетки."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Змейка с управлением направлением и списком сегментов."""

    def __init__(self):
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()

    def update_direction(self):
        """Применить выбранное игроком направление движения."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Передвинуть змейку на клетку с переходом через край поля."""
        x, y = self.get_head_position()
        dx, dy = self.direction
        head = (
            (x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, head)
        self.last = None
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        self.position = head

    def draw(self):
        """Стереть ушедший хвост и нарисовать все сегменты змейки."""
        if self.last and self.last not in self.positions:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def get_head_position(self):
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Вернуть змейку в центр поля с исходной длиной и направлением."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обработать закрытие окна и повороты без разворота назад."""
    directions = {
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT,
    }
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type == pygame.KEYDOWN and event.key in directions:
            direction = directions[event.key]
            opposite = tuple(-value for value in game_object.direction)
            if direction != opposite:
                game_object.next_direction = direction


def main():
    """Запустить игру с ростом змейки и сбросом при самостолкновении."""
    pygame.init()
    snake = Snake()
    apple = Apple()
    screen.fill(BOARD_BACKGROUND_COLOR)
    while apple.position in snake.positions:
        apple.randomize_position()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()

        # Узнаём, будет ли съедено яблоко, до удаления хвоста.
        x, y = snake.get_head_position()
        dx, dy = snake.direction
        next_head = (
            (x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )
        if next_head == apple.position:
            snake.length += 1
        snake.move()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        # Полное заполнение поля начинает новую игру.
        if snake.length == GRID_WIDTH * GRID_HEIGHT:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        while apple.position in snake.positions:
            apple.randomize_position()

        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
