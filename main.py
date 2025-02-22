import sys
import pygame
import random

from src.config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLUE, GREEN
from src.player_sprites import Duck, Lumberjack, Bullet
from src.environment_sprites import Cloud, Eagle, Spikes
from src.game_logic import GameState
from src.game_events import handle_events, check_collisions, show_game_over_popup

# Inicialização do Pygame
pygame.init()

# Configurações da tela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kunko o Patinho Peidorreiro")

# Fonte para pontuação
font = pygame.font.Font(None, 36)

# Clock para controle de FPS
clock = pygame.time.Clock()

def reset_game():
    # Limpar todos os sprites
    all_sprites.empty()
    clouds.empty()
    eagles.empty()
    bullets.empty()
    spikes.empty()
    
    # Recriar sprites principais
    duck = Duck()
    lumberjack = Lumberjack()
    
    # Adicionar sprites ao grupo
    all_sprites.add(duck)
    all_sprites.add(lumberjack)
    all_sprites.add(lumberjack.shotgun)
    
    # Recriar nuvens com lógica de spawn
    for _ in range(10):  # Criar 10 nuvens iniciais
        cloud = Cloud()
        cloud.rect.x = random.randint(0, SCREEN_WIDTH)
        cloud.rect.y = random.randint(0, SCREEN_HEIGHT // 2)  # Metade superior da tela
        clouds.add(cloud)
        all_sprites.add(cloud)
    
    # Reiniciar estado do jogo
    game_state.reset()
    
    return duck, lumberjack

# Grupos de sprites
all_sprites = pygame.sprite.Group()
clouds = pygame.sprite.Group()
eagles = pygame.sprite.Group()
spikes = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Estado do jogo
game_state = GameState()

# Inicializar jogo
duck, lumberjack = reset_game()

# Loop principal do jogo
running = True
last_time = pygame.time.get_ticks()

while running:
    current_time = pygame.time.get_ticks()
    delta_time = current_time - last_time
    last_time = current_time

    # Eventos
    handle_events(duck, clouds)

    # Atualizar lógica do jogo
    game_state.update_difficulty(delta_time, clouds, all_sprites)
    game_state.spawn_eagle(eagles, all_sprites)
    game_state.spawn_spikes(spikes, all_sprites)
    game_state.shoot_bullet(lumberjack, duck, all_sprites, bullets)

    # Atualizar sprites
    all_sprites.update()

    # Verificar colisões
    if check_collisions(duck, eagles, bullets, spikes, clouds, game_state):
        show_game_over_popup(screen)
        duck, lumberjack = reset_game()

    # Limpar tela
    screen.fill(BLUE)  # Fundo azul
    pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))  # Chão

    # Desenhar sprites
    all_sprites.draw(screen)

    # Renderizar pontuação e vidas
    score_text = font.render(f'Pontuação: {game_state.score}', True, (0, 0, 0))
    lives_text = font.render(f'Vidas: {game_state.lives}', True, (0, 0, 0))
    screen.blit(score_text, (10, 50))
    screen.blit(lives_text, (10, 90))
    
    # Mostrar status dos pums
    pums_text = f'Pums: {duck.farts_remaining}'
    if duck.farts_remaining == 0:
        cooldown = max(0, duck.cooldown_timer / 1000)  # Converter para segundos
        pums_text += f' (Cooldown: {cooldown:.1f}s)'
    text_surface = font.render(pums_text, True, (0, 0, 0))
    screen.blit(text_surface, (10, 10))

    # Atualização da tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
