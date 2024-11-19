from random import randrange

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
STONE_COLOR = (128, 128, 128)
SPEED = 10
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption('Змейка')
clock = pygame.time.Clock()


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

    @staticmethod
    def draw_cell(position, color) -> None:
        """Статический метод, который отрисовывает одну клетку."""
        rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, который описывает яблоко"""

    def __init__(self, snake_position=()) -> None:
        super().__init__()
        self.snake_positions = snake_position
        self.position = self.randomize_position
        self.body_color = APPLE_COLOR

    # Отрисовка яблока.
    def draw(self) -> None:
        """Переопределение метода отрисовки для змеи"""
        self.draw_cell(self.position, self.body_color)

    @property
    def randomize_position(self) -> tuple[int, int]:
        """Метод проверяет не занята ли позиция,
        и возвращает рандомную позицию яблока
        """
        while True:
            random_position = randrange(0, 621, 20), randrange(0, 461, 20)
            if random_position not in self.snake_positions:
                return random_position


class Snake(GameObject):
    """Класс, который описывает змейку"""

    def __init__(self) -> None:
        super().__init__()
        self.direction = None
        self.length = None
        self.positions = None
        self.reset()
        self.body_color = SNAKE_COLOR
        self.next_direction = None
        self.last = self.positions[-1]

    def update_direction(self, event_key) -> None:
        """Метод обновления направления движения змейки"""
        self.next_direction = event_key
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, который описывает логику движения змейки"""
        head_position_x, head_position_y = self.get_head_position
        self.last = self.positions[-1]
        if self.length > len(self.positions):
            self.positions.insert(
                0,
                ((head_position_x + 20 * self.direction[0]) % 640,
                 (head_position_y + 20 * self.direction[1]) % 480
                 )
            )
        else:
            self.positions.insert(
                0,
                ((head_position_x + 20 * self.direction[0]) % 640,
                 (head_position_y + 20 * self.direction[1]) % 480
                 )
            )
            self.positions.pop()

    def draw(self):
        """Переопределенный метод отрисовки змейки"""
        self.draw_cell(self.positions[0], self.body_color)
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
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """Метод, который обрабатывает нажатия клавиш"""
    for event in pygame.event.get():
        actions = {
            pygame.K_UP: (UP, DOWN),
            pygame.K_DOWN: (DOWN, UP),
            pygame.K_LEFT: (LEFT, RIGHT),
            pygame.K_RIGHT: (RIGHT, LEFT),
        }

        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if game_object.direction != actions[event.key][1]:
                game_object.update_direction(actions[event.key][0])
            elif event.key == pygame.K_ESCAPE:
                pygame.quit()
                raise SystemExit


def main():
    """Основной цикл игры"""
    pygame.init()
    snake = Snake()
    apple = Apple(snake.positions)

    while True:
        global SPEED
        clock.tick(SPEED)
        apple.draw()
        snake.draw()
        handle_keys(snake)
        if snake.positions[0] == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position
            SPEED += 0.03
        if (snake.length > 4
                and snake.get_head_position in snake.positions[3:]):
            snake.reset()
            apple.position = apple.randomize_position
        snake.move()
        pygame.display.update()


if __name__ == '__main__':
    main()
