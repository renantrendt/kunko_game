import sys
import pygame

def handle_events(duck, clouds=None):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            # Pulo
            if event.key == pygame.K_SPACE:
                duck.jump(jump_type='space')  # Pulo forte limitado
            elif event.key == pygame.K_w:
                duck.jump(jump_type='w')  # Pulo fraco com limite próprio
            
            # Pum
            if event.key in [pygame.K_f, pygame.K_q]:
                duck.fart()
    
    # Movimento horizontal
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        duck.rect.x -= 5  # Mover para esquerda
    if keys[pygame.K_d]:
        duck.rect.x += 5  # Mover para direita

def check_collisions(duck, eagles, bullets, spikes, game_state):
    # Colisão da bala com o Quack
    bullet_hits = pygame.sprite.spritecollide(duck, bullets, True)
    if bullet_hits:
        game_state.lives -= 1

    # Colisão com águias
    eagle_hits = pygame.sprite.spritecollide(duck, eagles, False)
    if eagle_hits:
        game_state.lives -= 1

    # Colisão com espinhos
    spike_hits = pygame.sprite.spritecollide(duck, spikes, False)
    if spike_hits:
        game_state.lives -= 1

    return game_state.lives <= 0

def show_game_over_popup(screen):
    popup = pygame.Surface((400, 200))
    popup.fill((255, 200, 200))  # Fundo rosa claro
    
    # Configurar fonte
    font_title = pygame.font.Font(None, 50)
    font_subtitle = pygame.font.Font(None, 36)
    
    # Renderizar texto
    title = font_title.render("Ohh so sad :(", True, (0, 0, 0))
    subtitle = font_subtitle.render("Try again!", True, (0, 0, 0))
    
    # Posicionar texto
    title_rect = title.get_rect(center=(200, 80))
    subtitle_rect = subtitle.get_rect(center=(200, 130))
    
    # Desenhar na popup
    popup.blit(title, title_rect)
    popup.blit(subtitle, subtitle_rect)
    
    # Posicionar popup no centro da tela
    popup_rect = popup.get_rect(center=(screen.get_width()//2, screen.get_height()//2))
    
    # Desenhar popup
    screen.blit(popup, popup_rect)
    pygame.display.flip()
    
    # Esperar por input
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
