#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

from helper_functions import *
import pygame

#### ====================================================================================================================== ####
#############                                          TILE CLASSES                                                   #############
#### ====================================================================================================================== ####

class Tile:
    def __init__(self, location: tuple):
        self.location = location
        self.sprite = pygame.transform.scale(pygame.image.load("assets/map/unspecified_tile.png").convert_alpha(), (40, 40))
        self.tower = None
    def check_collision(self, coords: tuple):
        if self.location[0] < coords[0] < self.location[0]+40 and self.location[1] < coords[1] < self.location[1]+40:
            return True


class pathTile(tile):
    def __init__(self):
        self.sprite = pygame.transform.scale(pygame.image.load("assets/map/path_tile.png").convert_alpha(), (40, 40))
        super().__init__()

        
class wallTile(tile):
    def __init__(self):
        self.sprite = pygame.transform.scale(pygame.image.load("assets/map/wall_tile.png").convert_alpha(), (40, 40))
        super().__init__()
    
    def placeTower(self, tower):
        self.tower = tower



