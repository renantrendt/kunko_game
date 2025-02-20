import pygame
import random
import sys

# Inicialização do Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kunko o Patinho Peidorreiro")

# Cores
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (34, 139, 34)

# Classe do Patinho
class Duck(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((255, 255, 0))  # Temporariamente amarelo
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 100
        self.velocity_y = 0
        self.jumping = False
        self.fart_power = 0

    def update(self):
        # Gravidade
        self.velocity_y += 0.5
        self.rect.y += self.velocity_y

        # Limitar ao chão
        if self.rect.bottom > SCREEN_HEIGHT - 50:
            self.rect.bottom = SCREEN_HEIGHT - 50
            self.velocity_y = 0
            self.jumping = False

        # Limitar ao topo
        if self.rect.top < 0:
            self.rect.top = 0
            self.velocity_y = 0

    def jump(self):
        if not self.jumping:
            self.velocity_y = -12
            self.jumping = True

    def fart(self):
        self.velocity_y = -15
        self.fart_power = 10

# Classe da Nuvem
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((100, 40))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.rect.y = random.randint(100, SCREEN_HEIGHT - 200)
        self.speed = random.randint(2, 4)

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.x = SCREEN_WIDTH
            self.rect.y = random.randint(100, SCREEN_HEIGHT - 200)

# Criação dos sprites
all_sprites = pygame.sprite.Group()
clouds = pygame.sprite.Group()
duck = Duck()
all_sprites.add(duck)

# Criar algumas nuvens iniciais
for i in range(4):
    cloud = Cloud()
    cloud.rect.x = random.randint(0, SCREEN_WIDTH)
    all_sprites.add(cloud)
    clouds.add(cloud)

# Clock para controle de FPS
clock = pygame.time.Clock()

# Loop principal do jogo
running = True
while running:
    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                duck.jump()
            elif event.key == pygame.K_SPACE:
                duck.fart()

    # Input contínuo
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        duck.rect.x -= 5
    if keys[pygame.K_d]:
        duck.rect.x += 5

    # Atualização
    all_sprites.update()

    # Colisões com nuvens
    hits = pygame.sprite.spritecollide(duck, clouds, False)
    if hits:
        duck.velocity_y = 0
        duck.rect.bottom = hits[0].rect.top
        duck.jumping = False

    # Desenho
    screen.fill(BLUE)  # Fundo azul
    pygame.draw.rect(screen, GREEN, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))  # Chão
    all_sprites.draw(screen)
    
    # Atualização da tela
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
