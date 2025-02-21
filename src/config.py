# Configurações do jogo

# Tela
# Configurações da tela
SCREEN_WIDTH = 800  # Reduzido de 1024
SCREEN_HEIGHT = 600  # Reduzido de 768

# Cores
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)
GREEN = (34, 139, 34)

# Dificuldade
DIFFICULTY_STAGES = [
    {
        'time': 30000,  # 30 segundos
        'score_multiplier': 2,
        'clouds_reduction': 0.8,  # 20% menos clouds
        'speed_increase': 1.13  # 13% + speed
    },
    {
        'time': 60000,  # 1 minuto
        'score_multiplier': 3,
        'clouds_reduction': 0.74,  # 26% menos clouds
        'speed_increase': 1.26  # 26% + speed
    },
    {
        'time': 150000,  # 2 minutos e 30 segundos
        'score_multiplier': 4,
        'clouds_reduction': 0.55,  # 45% menos clouds
        'speed_increase': 1.39  # 39% + speed
    }
]

# Pontuação
SCORE_INTERVAL = 2000  # 2 segundos
BASE_SCORE = 10
