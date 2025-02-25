class Duck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 60), pygame.SRCALPHA)  # Superfície com transparência
        self.draw_duck()  # Chama o método para desenhar o pato
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100
        
        # Física do pulo
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_strength = -10
        self.space_jump_strength = -70  # Ajuste esse valor para a força do pulo do Space
        self.jumping = False
        self.jumps_remaining = 2
        
        # Pulos separados para Space e W
        self.space_jumps_remaining = 1
        self.w_jumps_remaining = 2
        
        # Cooldowns separados para Space e W
        self.space_cooldown_timer = 0
        self.w_cooldown_timer = 0
        self.space_cooldown_duration = 1000  # 1000 milissegundos
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

    def draw_duck(self):
        # Limpar a superfície antes de desenhar
        self.image.fill((0, 0, 0, 0))  # Transparente
        
        # Corpo principal (branco)
        pygame.draw.ellipse(self.image, (255, 255, 255), (10, 15, 45, 40))  # Corpo oval
        
        # Cabeça (branca)
        pygame.draw.ellipse(self.image, (255, 255, 255), (35, 5, 30, 30))  # Cabeça redonda
        
        # Bico (amarelo)
        pygame.draw.polygon(self.image, (255, 200, 0), [(60, 15), (70, 15), (65, 20)])  # Bico
        
        # Boné
        pygame.draw.rect(self.image, (255, 0, 0), (40, 0, 20, 8))  # Parte vermelha
        pygame.draw.rect(self.image, (0, 255, 255), (40, 0, 10, 8))  # Parte azul
        pygame.draw.ellipse(self.image, (255, 0, 0), (35, 0, 10, 8))  # Aba
        
        # Pernas (amarelas)
        pygame.draw.rect(self.image, (255, 200, 0), (20, 50, 3, 10))  # Perna esquerda
        pygame.draw.rect(self.image, (255, 200, 0), (35, 50, 3, 10))  # Perna direita

    def draw(self, screen):
        self.draw_duck()  # Chama o método para desenhar o pato
        screen.blit(self.image, self.rect)

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
        
        # Flag para verificar se está em uma nuvem
        on_cloud = False
        
        # Verificar colisão com nuvens
        if clouds:
            for cloud in clouds:
                # Verificar sobreposição horizontal
                horizontal_overlap = (
                    self.rect.left < cloud.rect.right and 
                    self.rect.right > cloud.rect.left
                )
                
                # Verificar colisão vertical
                vertical_overlap = (
                    self.rect.bottom >= cloud.rect.top and 
                    self.rect.top < cloud.rect.bottom
                )
                
                # Colisão precisa
                if horizontal_overlap and vertical_overlap:
                    # Se estiver no chão e pulando, teletransportar para cima da nuvem
                    if self.rect.bottom >= SCREEN_HEIGHT - 50:
                        self.rect.bottom = cloud.rect.top
                        self.velocity_y = 0
                        self.jumping = False
                        on_cloud = True
                    # Se estiver caindo, pousar na nuvem
                    elif self.velocity_y > 0:
                        self.velocity_y = 0
                        self.rect.bottom = cloud.rect.top
                        self.jumping = False
                        on_cloud = True
                    break
        
        # Limites verticais
        if not on_cloud and self.rect.bottom >= SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.velocity_y = 0
            self.jumping = False
        
        # Resetar pulos em qualquer situação
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

    def jump(self, jump_force=-12, jump_type='space'):
        # Lógica de pulo com tratamento separado para Space e W
        if jump_type == 'space':
            if self.space_jumps_remaining > 0 and (self.space_consecutive_jumps < 2 or self.space_cooldown_timer <= 0):
                self.velocity_y = self.space_jump_strength  # Pulo forte
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