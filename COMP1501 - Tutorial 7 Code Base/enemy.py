#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

from helper_functions import *
import pygame
import random
import os

#### ====================================================================================================================== ####
#############                                         ENEMY_CLASS                                                  #############
#### ====================================================================================================================== ####

class Enemy:
    ''' Enemy Class - represents a single Enemy Object. '''
    # Represents common data for all enemies - only loaded once, not per new Enemy (Class Variable)
    enemy_data = {}
    for enemy in csv_loader("data/enemies.csv"):
        enemy_data[enemy[0]] = { "sprite": enemy[1], "health": int(enemy[2]), "speed": int(enemy[3]) }
    def __init__(self, enemy_type, location):
        ''' Initialization for Enemy.
        Input: enemy type (string), location (tuple of ints)
        Output: An Enemy Object
        '''
        self.name = enemy_type
        self.sprite = []
        self.pnglist = os.listdir(Enemy.enemy_data[enemy_type]["sprite"])
        for frame in self.pnglist:
            self.sprite.append(pygame.transform.flip(pygame.transform.scale(pygame.image.load(Enemy.enemy_data[enemy_type]["sprite"]+"/"+frame).convert_alpha(), (40, 40)), False, True))
        self.sprite_frames = len(self.sprite)
        self.sprite_counter = 0
        self.health = Enemy.enemy_data[enemy_type]["health"]
        self.speed = Enemy.enemy_data[enemy_type]["speed"]
        self.location = ((location[0]*20)+20, (location[1]*20)+20)
        self.direction = None
        self.effects = []
        self.alive = True
        self.spriteNum = 0

    def takeHit(self, damage, effect=None):
        self.health -= damage
        if effect not in self.effects and effect is not None:
            self.effects.append(effect)

    def move(self, map):
        self.location = (self.location[0], self.location[1] + self.speed/10)


class Basic_Bot(Enemy):
    pass
    # def __init__(self, enemy_type, location):
    #     super().__init__(enemy_type, location)

    # def move(self, map):
    #     rand = random.randint(4)
class Lefty_Bot(Enemy):
    pass
class Pathfinder_Bot(Enemy):
    pass
class Alien_Bot(Enemy):
    pass

#### ====================================================================================================================== ####
#############                                       ENEMY_FUNCTIONS                                                #############
#### ====================================================================================================================== ####

def update_enemy(enemy, game_data):
    enemy.move(game_data["map"])
    if enemy.health <= 0:
        enemy.alive = False
    if int(enemy.sprite_counter) < enemy.sprite_frames - 1:
        enemy.sprite_counter += 0.1
    else:
        enemy.sprite_counter = 0

def render_enemy(enemy, screen, settings):
    ''' Helper function that renders a single provided Enemy.
    Input: Enemy Object, screen (pygame display), Settings Object
    Output: None
    '''
    if enemy.alive:
        screen.blit(enemy.sprite[int(enemy.sprite_counter)], enemy.location)
