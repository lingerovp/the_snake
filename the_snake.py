from random import randrange

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки.
BORDER_COLOR = (93, 216, 228)

# Цвет яблока.
APPLE_COLOR = (255, 0, 0)

# Цвет змейки.
SNAKE_COLOR = (0, 255, 0)

# Цвет камня.
STONE_COLOR = (128, 128, 128)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Классы и функции игры.
class GameObject:
    """Класс, который описывает базовые атрибуты и функции."""

    def __init__(self) -> None:
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Абстрактный метод орисовки объкта,
        для переопределения в дочерних классах
        """
        pass


class Apple(GameObject):
    """Класс, который описывает яблоко"""

    def __init__(self) -> None:
        super().__init__()
        self.position = self.randomize_position
        self.body_color = APPLE_COLOR

    # Отрисовка яблока.
    def draw(self) -> None:
        """Переопределение метода отрисовки для змеи"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    @property
    def randomize_position(self) -> tuple[int, int]:
        """Метод проверяет не занята ли позиция,
        и возвращает рандомную позицию яблока
        """
        return randrange(0, 621, 20), randrange(0, 461, 20)


class Snake(GameObject):
    """Класс, который описывает змейку"""

    def __init__(self) -> None:
        super().__init__()
        self.positions = [self.position]
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = self.positions[-1]

    def update_direction(self) -> None:
        """Метод обновления направления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, который описывает логику движения змейки"""
        head_position = self.get_head_position
        if head_position[1] == 0 and self.direction == UP:
            self.last = self.positions[-1]
            self.positions.insert(0, (head_position[0], 460))
            self.positions.pop()
        elif head_position[1] == 460 and self.direction == DOWN:
            self.last = self.positions[-1]
            self.positions.insert(0, (head_position[0], 0))
            self.positions.pop()
        elif head_position[0] == 620 and self.direction == RIGHT:
            self.last = self.positions[-1]
            self.positions.insert(0, (0, head_position[1]))
            self.positions.pop()
        elif head_position[0] == 0 and self.direction == LEFT:
            self.last = self.positions[-1]
            self.positions.insert(0, (620, head_position[1]))
            self.positions.pop()
        else:
            self.last = self.positions[-1]
            self.positions.insert(
                0,
                (head_position[0] + 20 * self.direction[0],
                 head_position[1] + 20 * self.direction[1]
                 )
            )
            self.positions.pop()

    def draw(self):
        """Переопределенный метод отрисовки змейки"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки.
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента.
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    @property
    def get_head_position(self) -> tuple[int, int]:
        """Метод, который возвращает координаты головы змейки"""
        return self.positions[0]

    def reset(self) -> None:
        """Метод, который сбрасывает змейку в начальное состояние"""
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT


def handle_keys(game_object):
    """Метод, который обрабатывает нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основной цикл игры"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        global SPEED
        clock.tick(SPEED)
        handle_keys(snake)
        snake.draw()
        apple.draw()
        snake.update_direction()
        if snake.positions[0] == apple.position:
            snake.length += 1
            snake.positions.insert(-1, snake.last)
            while apple.position in snake.positions:
                apple.position = apple.randomize_position
            SPEED += 0.03
        if (snake.get_head_position in snake.positions[3:]
                and snake.length > 4):
            snake.reset()
            apple.position = apple.randomize_position
            screen.fill(BOARD_BACKGROUND_COLOR)
        snake.move()
        pygame.display.update()


if __name__ == '__main__':
    main()
