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


class pathTile(tile):
    def __init__(self):
        super().__init__()

        
class wallTile(tile):
    def __init__(self):
        super().__init__()
    
    def placeTower(self, tower):

