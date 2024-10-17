import pygame
import random

# Inicializa o Pygame
pygame.init()

# Dimensões da janela do jogo
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# Velocidade inicial do jogador e avalanche
PLAYER_SPEED = 5
AVALANCHE_SPEED = 2

# FPS
clock = pygame.time.Clock()

# Carregando o personagem (esquiador)
player_img = pygame.Surface((40, 60))
player_img.fill(RED)
player_rect = player_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))


# Função para desenhar obstáculos (troncos e pedras)
def create_obstacle():
    width = random.randint(40, 70)
    height = random.randint(20, 30)
    x_pos = random.randint(0, SCREEN_WIDTH - width)
    y_pos = random.randint(-100, -40)
    return pygame.Rect(x_pos, y_pos, width, height)


# Lista de obstáculos
obstacles = [create_obstacle() for _ in range(5)]


# Função principal do jogo
def game_loop():
    running = True
    player_x_change = 0
    avalanche_y = -100
    avalanche_speed = AVALANCHE_SPEED
    obstacle_speed = 5
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Movimento do jogador
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -PLAYER_SPEED
                if event.key == pygame.K_RIGHT:
                    player_x_change = PLAYER_SPEED
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0

        # Atualizar a posição do jogador
        player_rect.x += player_x_change
        if player_rect.left < 0:
            player_rect.left = 0
        if player_rect.right > SCREEN_WIDTH:
            player_rect.right = SCREEN_WIDTH

        # Movimento dos obstáculos
        for obstacle in obstacles:
            obstacle.y += obstacle_speed
            if obstacle.y > SCREEN_HEIGHT:
                obstacles.remove(obstacle)
                obstacles.append(create_obstacle())
                score += 1

        # Movimento da avalanche
        avalanche_y += avalanche_speed
        if avalanche_y > SCREEN_HEIGHT:
            avalanche_y = -100

        # Checar colisão com obstáculos
        for obstacle in obstacles:
            if player_rect.colliderect(obstacle):
                running = False  # Finaliza o jogo se o jogador colidir

        # Desenhar tudo
        screen.fill(WHITE)

        # Desenha avalanche
        pygame.draw.rect(screen, GRAY, (0, avalanche_y, SCREEN_WIDTH, 20))

        # Desenha jogador
        screen.blit(player_img, player_rect)

        # Desenha obstáculos
        for obstacle in obstacles:
            pygame.draw.rect(screen, BLACK, obstacle)

        # Mostra pontuação
        font = pygame.font.SysFont(None, 36)
        text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(60)  # 60 FPS

    pygame.quit()


# Inicia o loop do jogo
game_loop()