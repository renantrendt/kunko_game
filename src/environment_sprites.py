import pygame
import random

from .config import SCREEN_WIDTH, SCREEN_HEIGHT

class Cloud(pygame.sprite.Sprite):
    def __init__(self, speed_multiplier=1):
        super().__init__()
        self.image = pygame.Surface((70, 28))  # Reduzido de 100x40
        self.image.fill((255, 255, 255))  # Branco
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(100, SCREEN_HEIGHT - 140)  # Ajustado para tela menor
        self.speed = random.randint(2, 4) * speed_multiplier

    def update(self):
        # Mover nuvem para a esquerda
        self.rect.x -= self.speed
        
        # Reposicionar nuvem quando sair da tela
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randint(100, SCREEN_HEIGHT - 140)  # Ajustado para tela menor

class Eagle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((42, 28))  # Reduzido de 60x40
        self.image.fill((139, 69, 19))  # Marrom
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(50, SCREEN_HEIGHT - 140)  # Ajustado para tela menor
        self.speed = random.randint(3, 6)

    def update(self):
        # Mover águia para a esquerda
        self.rect.x -= self.speed
        
        # Reposicionar águia quando sair da tela
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randint(50, SCREEN_HEIGHT - 140)  # Ajustado para tela menor

class Spikes(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        spike_width = 60
        spike_height = 60  # Aumentado para 50 pixels
        num_spikes = SCREEN_WIDTH // spike_width + 1
        
        self.image = pygame.Surface((SCREEN_WIDTH, spike_height), pygame.SRCALPHA)
        
        # Desenha vários spikes ao longo da largura da tela
        for i in range(num_spikes):
            x = i * spike_width
            # Desenha cada spike como um triângulo maior
            pygame.draw.polygon(self.image, (255, 0, 0), [
                (x, spike_height),  # Base esquerda
                (x + spike_width//2, 0),  # Topo
                (x + spike_width, spike_height)  # Base direita
            ])
        
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = 0
        self.rect.y = SCREEN_HEIGHT - spike_height  # Ajusta a posição vertical
