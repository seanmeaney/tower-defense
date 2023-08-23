#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

from helper_functions import *
import pygame

#### ====================================================================================================================== ####
#############                                          TILE CLASSES                                                   #############
#### ====================================================================================================================== ####

class Tile:
    def __init__(self, xpos, ypos):
        self.xpos = xpos
        self.ypos = ypos
        self.sprite = pygame.transform.scale(pygame.image.load("assets/map/unspecified_tile.png").convert_alpha(), (40, 40))
        self.tower = None

    def type(self):
        return "generic"

    def check_collision(self, coords: tuple):
        if self.xpos < coords[0] < self.xpos+40 and self.ypos < coords[1] < self.ypos+40:
            return True



class pathTile(Tile):
    def __init__(self, xpos, ypos):
        super().__init__(xpos, ypos)
        self.sprite = pygame.transform.scale(pygame.image.load("assets/map/path_tile.png").convert_alpha(), (40, 40))

    def type(self):
        return "path"

        
class wallTile(Tile):
    def __init__(self, xpos, ypos):
        super().__init__(xpos, ypos)
        self.sprite = pygame.transform.scale(pygame.image.load("assets/map/wall_tile.png").convert_alpha(), (40, 40))


    def type(self):
        return "wall"
    
    def placeTower(self, tower):
        self.tower = tower
        tower.location = (self.xpos, self.ypos)

class startTile(Tile):
    def __init__(self, xpos, ypos):
        super().__init__(xpos, ypos)
        self.sprite = pygame.transform.scale(pygame.image.load("assets/map/start_tile.png").convert_alpha(), (40, 40))


class finishTile(Tile):
    def __init__(self, xpos, ypos):
        super().__init__(xpos, ypos)
        self.sprite = pygame.transform.scale(pygame.image.load("assets/map/finish_tile.png").convert_alpha(), (40, 40))

    def type(self):
        return "end"


