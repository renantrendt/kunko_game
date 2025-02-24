import sys
import pygame
import time

def handle_events(duck, lumberjack, all_sprites, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Atirar quando clicar com o mouse
            if event.button == 1:  # Botão esquerdo do mouse
                mouse_x, mouse_y = pygame.mouse.get_pos()
                bullet = lumberjack.shotgun.shoot(mouse_x, mouse_y)
                bullets.add(bullet)
                all_sprites.add(bullet)
        
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

# Variável para rastrear o tempo do último dano causado
last_damage_time = 0
# Tempo entre os danos em segundos (60 segundos e 14 segundos)
damage_interval = 2

def check_collisions(duck, eagles, bullets, spikes, clouds, game_state):
    global last_damage_time
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
        current_time = time.time()
        # Verifica se o intervalo de dano foi atingido
        if current_time - last_damage_time >= damage_interval:
            last_damage_time = current_time
            # Aqui você deve adicionar a lógica para causar dano ao jogador
            # Exemplo: player.health -= damage_amount
            game_state.lives -= 1
            print('Dano causado!')

    # Colisão com nuvens usando máscaras para colisão precisa
    for cloud in clouds:
        if pygame.sprite.collide_mask(duck, cloud):
            # Impede o pato de atravessar a nuvem
            if duck.rect.bottom > cloud.rect.top and duck.rect.top < cloud.rect.top:
                duck.rect.bottom = cloud.rect.top
                duck.velocity_y = 0
            elif duck.rect.top < cloud.rect.bottom and duck.rect.bottom > cloud.rect.bottom:
                duck.rect.top = cloud.rect.bottom
                duck.velocity_y = 0

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
