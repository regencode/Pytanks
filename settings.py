import pygame

class Settings():
    def __init__(self):
        
        # Game appearance settings

        self.display_size = (1200, 800)
        self.background_color = "#c9c9c9"
        self.framerate = 60

        # Player settings
        self.player_speed = 4
        self.player_boostSpeed = self.player_speed*1.5
        self.player_posDelayMin = 200 #ms
        self.player_posDelayMax = 500 #ms
        self.player_maxHealth = 80
        self.player_invulnerableTime = 800 #ms
        self.player_boostCooldown = 5000 #ms
        self.player_boostTime = 300 #ms

        # Enemy settings
        self.enemy_maxSpeed = 2
        self.enemy_accelThreshold = 0.2
        self.enemy_spawnRateMin = 300 #ms
        self.enemy_spawnRateMax = 500 #ms
        self.enemy_maxNum = 4
        self.enemy_maxHealth = 500
        self.enemy_expOnKill = 10
        self.enemy_damage = 20

        self.rectangle_maxHealth = self.enemy_maxHealth * 3

        # Bullet settings
        self.pBullet_speed = 8
        self.pBullet_rawDamage = 150
        self.pBullet_damage = self.pBullet_rawDamage + (self.pBullet_speed*15)
        self.pBullet_cooldown = 500 #ms
        self.pBullet_size = 0.7
        self.pBullet_lifetime = 2500 #ms

        # Enemy Bullet settings
        self.eBullet_speed = 8
        self.eBullet_damage = 20
        self.eBullet_cooldown = 2500 #ms
        self.eBullet_size = 0.6
        self.eBullet_lifetime = 2000 #ms

        # Enemy Drops settings
        self.drops_lifetime = 10000 #ms
    

        #Game progression settings
        self.expThresholds = []
        for i in range(10, 500, 10):
            self.expThresholds.append(i)

        # Other settings
        self.wall_damage = 30
    
    def update_difficulty(self):
        # Increase difficulty every time this method is called (from main)

        self.enemy_maxNum *= 2

        if self.player_speed <= 17:
            self.enemy_maxSpeed += 1

        self.enemy_maxHealth *= 1.15
        self.enemy_spawnRateMin /= 1.75
        self.enemy_spawnRateMax /= 1.75
        self.enemy_accelThreshold += 0.07
        self.enemy_expOnKill *= 1.1
        self.eBullet_speed += 2
        self.eBullet_cooldown /= 1.2

    def update_levelUp(self):
        # Increase player stats every level up
        if self.player_speed <= 15:
            self.player_speed += 0.4

        self.pBullet_speed += 2.2
        self.pBullet_size += 0.2
        self.pBullet_damage += 125
        self.pBullet_cooldown /= 1.3