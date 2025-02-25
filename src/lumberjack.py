import pygame

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
        self._last_update = pygame.time.get_ticks()

    def auto_shoot(self, target, all_sprites, bullets):
        current_time = pygame.time.get_ticks()
        if current_time - self._last_update > 1000:  # Cooldown reduzido para 500 ms
            bullet = self.shotgun.shoot(target.rect.centerx, target.rect.centery)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self._last_update = current_time
            return bullet
        return None

    def auto_shoot_at_duck(self, duck, all_sprites, bullets):
        return self.auto_shoot(duck, all_sprites, bullets)
