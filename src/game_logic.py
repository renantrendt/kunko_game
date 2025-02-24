import pygame
import random

from .config import (
    SCREEN_WIDTH, SCREEN_HEIGHT, 
    DIFFICULTY_STAGES, 
    SCORE_INTERVAL, 
    BASE_SCORE
)
from .player_sprites import Bullet
from .environment_sprites import Cloud, Eagle, Spikes

class GameState:
    def __init__(self):
        self.score = 0
        self.score_timer = 0
        self.difficulty_timer = 0
        self.current_difficulty_stage = 0
        self.eagle_timer = 0
        self.lumberjack_shoot_timer = 0
        self.lives = 3

    def update_difficulty(self, delta_time, clouds, all_sprites):
        self.difficulty_timer += delta_time
        self.score_timer += delta_time
        self.eagle_timer += delta_time

        # Aumentar pontuação
        if self.score_timer >= SCORE_INTERVAL:
            current_stage = None
            for stage in DIFFICULTY_STAGES:
                if self.difficulty_timer >= stage['time']:
                    current_stage = stage
            
            self.score += BASE_SCORE * (current_stage['score_multiplier'] if current_stage else 1)
            self.score_timer = 0

        # Aumentar dificuldade nos estágios definidos
        for i, stage in enumerate(DIFFICULTY_STAGES):
            if (self.difficulty_timer >= stage['time'] and 
                self.current_difficulty_stage < i):
                # Reduzir número de nuvens
                clouds_to_remove = int(len(clouds) * stage['clouds_reduction'])
                for _ in range(clouds_to_remove):
                    cloud = clouds.sprites()[0]
                    all_sprites.remove(cloud)
                    clouds.remove(cloud)
                
                # Aumentar velocidade das nuvens
                for cloud in clouds:
                    cloud.speed *= stage['speed_increase']
                
                self.current_difficulty_stage = i

    def spawn_eagle(self, eagles, all_sprites):
        if self.eagle_timer >= 5000 and len(eagles) < 2:
            eagle = Eagle()
            all_sprites.add(eagle)
            eagles.add(eagle)
            self.eagle_timer = 0

    def spawn_spikes(self, spikes, all_sprites):
        if self.difficulty_timer >= 120000 and len(spikes) == 0:
            spike = Spikes()
            all_sprites.add(spike)
            spikes.add(spike)

    def shoot_bullet(self, lumberjack, duck, all_sprites, bullets):
        if self.lumberjack_shoot_timer >= 3000:
            bullet_start_x, bullet_start_y = lumberjack.shotgun.get_bullet_start_pos()
            bullet = Bullet(
                bullet_start_x,
                bullet_start_y,
                duck.rect.centerx,
                duck.rect.centery
            )
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.lumberjack_shoot_timer = 0

    def update_shoot_timer(self, delta_time):
        self.lumberjack_shoot_timer += delta_time
        self.eagle_timer += delta_time

    def reset(self):
        self.score = 0
        self.difficulty_timer = 0
        self.current_difficulty_stage = 0
        self.eagle_timer = 0
        self.lumberjack_shoot_timer = 0
        self.lives = 20000
