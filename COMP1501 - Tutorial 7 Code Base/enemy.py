#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

from helper_functions import *
from map import *
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
        enemy_data[enemy[0]] = { "sprite": enemy[1], "health": float(enemy[2]), "speed": float(enemy[3])}
    def __init__(self, enemy_type, location):
        ''' Initialization for Enemy.
        Input: enemy type (string), location (tuple of ints)
        Output: An Enemy Object
        '''
        self.name = enemy_type
        self.sprite = []
        self.pnglist = os.listdir(Enemy.enemy_data[enemy_type]["sprite"])
        for frame in self.pnglist:
            self.sprite.append(pygame.transform.scale(pygame.image.load(Enemy.enemy_data[enemy_type]["sprite"]+"/"+frame).convert_alpha(), (40, 40)))
        self.sprite_frames = len(self.sprite)
        self.sprite_counter = 0
        self.health = Enemy.enemy_data[enemy_type]["health"]
        self.speed = Enemy.enemy_data[enemy_type]["speed"]
        self.location = list(unfix_location(location))
        self.direction = None
        self.effects = []
        self.alive = True
        self.direction = (0, 1)
        self.rotation = 180
        self.wait = 0

    def takeHit(self, damage, effect=None):
        self.health -= damage
        if effect not in self.effects and effect is not None:
            self.effects.append(effect)

    def move(self, map):
        self.location[0] += self.direction[0]*self.speed
        self.location[1] += self.direction[1]*self.speed        

    def turn(self, direction):
        if direction == "down":
            self.direction = (0,1)
        elif direction == "up": 
            self.direction = (0,-1)
        elif direction == "right":
            self.direction = (1, 0)
        elif direction == "left":
            self.direction = (-1, 0)
    
    def turn_cw(self):
        if self.direction == (0,1):
            self.direction = (-1,0)
        elif self.direction == (-1,0):
            self.direction = (0,-1)
        elif self.direction == (0,-1):
            self.direction = (1,0)
        elif self.direction == (1,0):
            self.direction = (0,1)
        self.rotation -= 90
    
    def turn_cc(self):
        self.wait = 5
        if self.direction == (0,1):
            self.direction = (1,0)
        elif self.direction == (1,0):
            self.direction = (0,-1)
        elif self.direction == (0,-1):
            self.direction = (-1,0)
        elif self.direction == (-1,0):
            self.direction = (0,1)
        if self.rotation + 90 < 360:
            self.rotation += 90
        else:
            self.rotation = 0
        
    
    def navigate(self, world_map):
        print("inside the enemy navigate for some reason")

class Basic_Bot(Enemy):
    def __init__(self, enemy_type, location):
        super().__init__(enemy_type, location)
        self.traversed_tiles = {}
        self.last_tile = None
        self.looking_at = None
        self.passable = 0

    
    def navigate(self, world_map):
        fixed_location = (world_map.fix_location(self.location)[0], world_map.fix_location(self.location)[1])
        looking_at = (self.location[0]+max(self.direction[0]*40, self.direction[0]*2), self.location[1]+self.direction[1]*20)
        self.looking_at = looking_at
        facing_wall = world_map.check_location(looking_at)
        if  fixed_location != self.last_tile and self.last_tile is not None:
            if self.last_tile in self.traversed_tiles:
                self.traversed_tiles[self.last_tile] += 1
            else:
                self.traversed_tiles[self.last_tile] = 0
                

        blocked = facing_wall or (world_map.fix_location(looking_at) in self.traversed_tiles and self.traversed_tiles[world_map.fix_location(looking_at)] < int(self.passable))
        while blocked:
            self.turn_cc()
            looking_at = (self.location[0]+max(self.direction[0]*40, self.direction[0]*2), self.location[1]+self.direction[1]*20)
            self.looking_at = looking_at
            facing_wall = world_map.check_location(looking_at)
            blocked = facing_wall or (world_map.fix_location(looking_at) in self.traversed_tiles and self.traversed_tiles[world_map.fix_location(looking_at)] < int(self.passable))
            self.passable += 0.25


        self.last_tile = world_map.fix_location(self.location)

    def update(self, game_data):
        if self.wait > 0:
            self.wait -= 1
            return
        self.move(game_data["map"])
        if self.health <= 0:
            self.alive = False
        if int(self.sprite_counter) < self.sprite_frames - 1:
            self.sprite_counter += 0.1
        else:
            self.sprite_counter = 0
        self.navigate(game_data["map"])
    
    def render(self, screen, settings):
        if self.alive:
            screen.blit(pygame.transform.rotate(self.sprite[int(self.sprite_counter)], self.rotation), (self.location[0]-20, self.location[1]-20))
        #for tile in self.traversed_tiles.keys():
        #    pygame.draw.circle(screen, colours.magenta, unfix_location(tile), 15)




class Pathfinder_Bot(Enemy):
    pass
class Alien_Bot(Enemy):
    pass

#### ====================================================================================================================== ####
#############                                       ENEMY_FUNCTIONS                                                #############
#### ====================================================================================================================== ####




