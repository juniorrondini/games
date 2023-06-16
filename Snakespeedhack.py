import pygame
import random

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Tamanho da célula e número de células
CELL_SIZE = 20
CELLS_X = SCREEN_WIDTH // CELL_SIZE
CELLS_Y = SCREEN_HEIGHT // CELL_SIZE

# Direções
UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

# Inicialização do Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")

clock = pygame.time.Clock()

# Função para desenhar a pontuação
def draw_score(score):
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))

# Função para desenhar a mensagem de fim de jogo
def draw_game_over():
    font = pygame.font.Font(None, 72)
    text = font.render("Game Over", True, RED)
    screen.blit(text, (SCREEN_WIDTH/2 - text.get_width()/2, SCREEN_HEIGHT/2 - text.get_height()/2))

# Função para desenhar a tela do jogo
def draw_game_screen(snake_segments, food_position, score):
    screen.fill(BLACK)

    for segment in snake_segments:
        pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(screen, RED, (food_position[0] * CELL_SIZE, food_position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    draw_score(score)

    pygame.display.flip()

# Função para gerar uma posição aleatória para a comida
def generate_food_position(snake_segments):
    while True:
        food_position = (random.randint(0, CELLS_X - 1), random.randint(0, CELLS_Y - 1))
        if food_position not in snake_segments:
            return food_position

# Função principal do jogo
def game():
    snake_segments = [(5, 5), (4, 5), (3, 5)]
    direction = RIGHT
    food_position = generate_food_position(snake_segments)
    score = 0
    game_over = False

    snake_speed = 10  # Velocidade inicial da cobra
    wall_collision = False  # Indica se a cobra pode colidir com as paredes
    auto_guide = False  # Indica se a cobra está sendo guiada automaticamente

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT
                elif event.key == pygame.K_1:
                    # Aumentar velocidade em 1000%
                    snake_speed *= 10
                elif event.key == pygame.K_i:
                    # Ativar imortalidade contra colisão com as paredes
                    wall_collision = not wall_collision
                elif event.key == pygame.K_f:
                    # Ativar/Desativar guiar automaticamente até a comida
                    if auto_guide:
                        auto_guide = False
                    else:
                        auto_guide = True

        if auto_guide:
            head = snake_segments[0]
            food_x, food_y = food_position

            if head[0] < food_x:
                direction = RIGHT
            elif head[0] > food_x:
                direction = LEFT
            elif head[1] < food_y:
                direction = DOWN
            elif head[1] > food_y:
                direction = UP

        head = snake_segments[0]
        if direction == UP:
            new_head = (head[0], head[1] - 1)
        elif direction == DOWN:
            new_head = (head[0], head[1] + 1)
        elif direction == LEFT:
            new_head = (head[0] - 1, head[1])
        elif direction == RIGHT:
            new_head = (head[0] + 1, head[1])

        if not wall_collision:
            # A cobra atravessa as paredes
            new_head = (new_head[0] % CELLS_X, new_head[1] % CELLS_Y)

        snake_segments.insert(0, new_head)

        if new_head == food_position:
            score += 1
            food_position = generate_food_position(snake_segments)
        else:
            snake_segments.pop()

        draw_game_screen(snake_segments, food_position, score)
        clock.tick(snake_speed)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game()

        draw_game_over()
        pygame.display.flip()

game()
