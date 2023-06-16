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
def draw_game_screen(snake_segments, food_position, score, snake_color):
    screen.fill(BLACK)

    for segment in snake_segments:
        pygame.draw.rect(screen, snake_color, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

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
    speed_increase = False  # Indica se a velocidade está aumentada
    auto_guide = False  # Indica se a cobra está sendo guiada automaticamente

    color_change_interval = 1  # Intervalo de mudança de cor em segundos
    color_change_timer = 0  # Contador de tempo para a mudança de cor
    snake_color = GREEN  # Cor inicial da cobra

    # Loop principal do jogo
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    auto_guide = not auto_guide
                elif event.key == pygame.K_1:
                    speed_increase = True
                elif event.key == pygame.K_2:
                    speed_increase = False

        if not game_over:
            # Lógica do jogo
            if not auto_guide:
                # Captura de eventos de teclado
                keys = pygame.key.get_pressed()

                if keys[pygame.K_UP] and direction != DOWN:
                    direction = UP
                elif keys[pygame.K_DOWN] and direction != UP:
                    direction = DOWN
                elif keys[pygame.K_LEFT] and direction != RIGHT:
                    direction = LEFT
                elif keys[pygame.K_RIGHT] and direction != LEFT:
                    direction = RIGHT

            if auto_guide:
                # Lógica para jogar automaticamente (tecla F pressionada)
                head = snake_segments[0]
                food_x, food_y = food_position

                if head[0] < food_x and direction != LEFT:
                    direction = RIGHT
                elif head[0] > food_x and direction != RIGHT:
                    direction = LEFT
                elif head[1] < food_y and direction != UP:
                    direction = DOWN
                elif head[1] > food_y and direction != DOWN:
                    direction = UP

            # Movimento da cobra
            head = snake_segments[0]
            if direction == UP:
                new_head = (head[0], head[1] - 1)
            elif direction == DOWN:
                new_head = (head[0], head[1] + 1)
            elif direction == LEFT:
                new_head = (head[0] - 1, head[1])
            elif direction == RIGHT:
                new_head = (head[0] + 1, head[1])

            # Verificação de colisões com a parede
            if new_head[0] < 0:
                new_head = (CELLS_X - 1, new_head[1])
            elif new_head[0] >= CELLS_X:
                new_head = (0, new_head[1])
            elif new_head[1] < 0:
                new_head = (new_head[0], CELLS_Y - 1)
            elif new_head[1] >= CELLS_Y:
                new_head = (new_head[0], 0)

            # Movimento da cobra
            snake_segments.insert(0, new_head)

            # Verificação de colisões com a comida
            if new_head == food_position:
                score += 1
                food_position = generate_food_position(snake_segments)
            else:
                snake_segments.pop()

            if not speed_increase:
                snake_speed = 10
            else:
                snake_speed = 200000

            # Verificação de mudança de cor
            if speed_increase and color_change_timer >= color_change_interval:
                snake_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                color_change_timer = 0  # Reinicia o contador de mudança de cor

            # Atualização do contador de mudança de cor
            color_change_timer += clock.get_time() / 1000  # Converte o tempo em milissegundos para segundos

        screen.fill(BLACK)
        draw_game_screen(snake_segments, food_position, score, snake_color)

        if game_over:
            draw_game_over()

        pygame.display.flip()
        clock.tick(snake_speed)

    pygame.quit()

if __name__ == '__main__':
    game()
