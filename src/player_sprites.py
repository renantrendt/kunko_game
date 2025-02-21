import pygame
import math
import random

from .config import SCREEN_WIDTH, SCREEN_HEIGHT

class Duck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((35, 35))  # Reduzido de 50x50
        self.image.fill((255, 255, 0))  # Amarelo
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        
        # Física do pulo
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.jumping = False
        self.jumps_remaining = 2
        
        # Pulos separados para Space e W
        self.space_jumps_remaining = 2
        self.w_jumps_remaining = 2
        
        # Cooldowns separados para Space e W
        self.space_cooldown_timer = 0
        self.w_cooldown_timer = 0
        self.space_cooldown_duration = 2000  # 2 segundos
        self.w_cooldown_duration = 50  # 50 milissegundos
        
        # Contadores de pulos consecutivos
        self.space_consecutive_jumps = 0
        self.w_consecutive_jumps = 0
        
        # Sistema de pum
        self.farts_remaining = 2
        self.cooldown_timer = 0
        self.cooldown_duration = 1500  # 1.5 segundos
        
        # Novo atributo de arranhões
        self.scratch_count = 0
        
        # Contador de colisões com Eagles
        self.eagle_collision_count = 0
        
        # Último update para cooldown
        self._last_update = pygame.time.get_ticks()

    def draw_scars(self):
        # Criar imagem com arranhões
        scar_image = self.image.copy()
        
        # Adicionar arranhões baseado no número de colisões
        for _ in range(self.scratch_count):
            # Posições aleatórias para os arranhões
            start_x = random.randint(0, self.rect.width)
            start_y = random.randint(0, self.rect.height)
            end_x = random.randint(0, self.rect.width)
            end_y = random.randint(0, self.rect.height)
            
            # Desenhar o arranhão
            pygame.draw.line(scar_image, (255, 0, 0), (start_x, start_y), (end_x, end_y), 2)
        
        # Atualizar a imagem do Quack
        self.image = scar_image

    def update(self, clouds=None):
        # Atualiza cooldowns de pulo
        self.update_cooldowns()
        
        # Atualiza cooldown de pum
        if self.cooldown_timer > 0:
            self.cooldown_timer -= pygame.time.get_ticks() - self._last_update
            if self.cooldown_timer <= 0:
                self.cooldown_timer = 0
        
        # Gravidade
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
        
        # Verificar colisão com nuvens
        if clouds:
            for cloud in clouds:
                if pygame.sprite.collide_mask(self, cloud):
                    # Lógica de colisão com nuvem
                    self.velocity_y = 0
                    self.rect.bottom = cloud.rect.top
                    self.jumping = False
        
        # Limites verticais
        if self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.velocity_y = 0
            self.jumping = False
        
        # Resetar pulos SEMPRE
        self.space_jumps_remaining = 2
        self.w_jumps_remaining = 2
        
        # Limites horizontais
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        
        # Limitar velocidade vertical
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity_y = 0
            
        # Último update
        self._last_update = pygame.time.get_ticks()

        # Desenhar arranhões
        self.draw_scars()

    def jump(self, jump_force=-12, jump_type='space'):
        # Lógica de pulo com tratamento separado para Space e W
        if jump_type == 'space':
            if self.space_jumps_remaining > 0 and (self.space_consecutive_jumps < 2 or self.space_cooldown_timer <= 0):
                self.velocity_y = -20  # Pulo forte
                self.jumping = True
                self.space_jumps_remaining -= 1
                self.space_consecutive_jumps += 1
                
                # Iniciar cooldown após 2 pulos consecutivos
                if self.space_consecutive_jumps >= 2:
                    self.space_cooldown_timer = self.space_cooldown_duration
        
        elif jump_type == 'w':
            if self.w_jumps_remaining > 0 and (self.w_consecutive_jumps < 2 or self.w_cooldown_timer <= 0):
                self.velocity_y = -10  # Pulo fraco
                self.jumping = True
                self.w_jumps_remaining -= 1
                self.w_consecutive_jumps += 1
                
                # Iniciar cooldown após 2 pulos consecutivos
                if self.w_consecutive_jumps >= 2:
                    self.w_cooldown_timer = self.w_cooldown_duration
        
        # Resetar gravidade para dar mais impulso
        self.gravity = 0.5

    def can_fart(self):
        return self.farts_remaining > 0

    def fart(self):
        if self.can_fart():
            self.farts_remaining -= 1
            self.cooldown_timer = self.cooldown_duration

    def update_cooldowns(self):
        if self.space_cooldown_timer > 0:
            self.space_cooldown_timer -= pygame.time.get_ticks() - self._last_update
            if self.space_cooldown_timer <= 0:
                self.space_cooldown_timer = 0
                self.space_consecutive_jumps = 0
        if self.w_cooldown_timer > 0:
            self.w_cooldown_timer -= pygame.time.get_ticks() - self._last_update
            if self.w_cooldown_timer <= 0:
                self.w_cooldown_timer = 0
                self.w_consecutive_jumps = 0
        self._last_update = pygame.time.get_ticks()


class Lumberjack(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Criar uma superfície mais detalhada para o lenhador, agora menor
        self.image = pygame.Surface((56, 84), pygame.SRCALPHA)  # Reduzido de 80x120
        
        # Base do corpo
        pygame.draw.rect(self.image, (100, 50, 20), (14, 28, 28, 42))  # Marrom escuro
        
        # Camisa xadrez com mais detalhes
        for x in range(14, 42, 7):
            pygame.draw.line(self.image, (200, 0, 0), (x, 28), (x, 70), 1)  # Linhas verticais vermelhas
            pygame.draw.line(self.image, (0, 0, 200), (14, x), (42, x), 1)  # Linhas horizontais azuis
        
        # Cabeça com mais detalhes
        pygame.draw.circle(self.image, (255, 218, 185), (28, 17), 13)  # Tom de pele
        
        # Olhos
        pygame.draw.circle(self.image, (0, 0, 0), (25, 15), 2)  # Olho esquerdo
        pygame.draw.circle(self.image, (0, 0, 0), (31, 15), 2)  # Olho direito
        
        # Barba mais elaborada
        pygame.draw.polygon(self.image, (180, 180, 180), [
            (21, 21), (35, 21), (28, 28)])
        
        self.rect = self.image.get_rect()

        # Posicionar no canto inferior direito
        self.rect.bottomright = (SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Shotgun
        self.shotgun = Shotgun(self)

class Shotgun(pygame.sprite.Sprite):
    def __init__(self, lumberjack):
        super().__init__()
        self.image = pygame.Surface((84, 28), pygame.SRCALPHA)  # Reduzido de 120x40
        
        # Cano mais realista (agora apontando para a esquerda)
        pygame.draw.line(self.image, (100, 100, 100), (84, 14), (14, 14), 8)  # Cano principal
        
        # Detalhes metálicos
        for x in range(21, 77, 14):
            pygame.draw.line(self.image, (50, 50, 50), (x, 10), (x, 18), 2)
        
        # Coronha de madeira com textura (invertida)
        pygame.draw.polygon(self.image, (139, 69, 19), [(14, 7), (0, 14), (14, 21)])
        
        # Gatilho com sombra
        pygame.draw.circle(self.image, (0, 0, 0), (49, 14), 3)
        pygame.draw.circle(self.image, (150, 150, 150), (49, 14), 2)
        
        self.rect = self.image.get_rect()
        self.lumberjack = lumberjack
        self.update()

    def update(self):
        # Posicionar a shotgun junto ao braço do lenhador
        self.rect.left = self.lumberjack.rect.left - 9  # Mais para trás
        self.rect.centery = self.lumberjack.rect.centery + 22  # Mais para baixo

    def get_bullet_start_pos(self):
        return self.rect.left, self.rect.centery

class Bullet(pygame.sprite.Sprite):
    def __init__(self, start_x, start_y, target_x, target_y):
        super().__init__()
        self.image = pygame.Surface((14, 3), pygame.SRCALPHA)  # Reduzido de 20x5
        pygame.draw.line(self.image, (255, 0, 0), (0, 1), (14, 1), 2)  # Bala vermelha
        
        self.rect = self.image.get_rect()
        self.rect.midright = (start_x, start_y)
        
        # Calcular direção
        dx = target_x - start_x
        dy = target_y - start_y
        
        # Normalizar e ajustar velocidade
        magnitude = math.sqrt(dx**2 + dy**2)
        self.velocity_x = (dx / magnitude) * 10
        self.velocity_y = (dy / magnitude) * 10

    def update(self):
        # Mover bala na direção calculada
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y
        
        # Remover bala se sair da tela
        if (self.rect.right < 0 or 
            self.rect.left > SCREEN_WIDTH or 
            self.rect.bottom < 0 or 
            self.rect.top > SCREEN_HEIGHT):
            self.kill()
