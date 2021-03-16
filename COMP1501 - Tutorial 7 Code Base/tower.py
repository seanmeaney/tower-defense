#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

from helper_functions import *
import pygame

#### ====================================================================================================================== ####
#############                                         TOWER_CLASS                                                  #############
#### ====================================================================================================================== ####

class Tower:
    ''' Tower Class - represents a single Tower Object. '''
    # Represents common data for all towers - only loaded once, not per new Tower (Class Variable)
    tower_data = {}
    for tower in csv_loader("data/towers.csv"):
        tower_data[tower[0]] = { "sprite": tower[1], "damage": int(tower[2]), "rate_of_fire": int(tower[3]), "radius": int(tower[4]) }
    def __init__(self, tower_type, location):
        ''' Initialization for Tower.
        Input: tower_type (string), location (tuple), radius_sprite (pygame.Surface)
        Output: A Tower Object
        '''
        self.name = tower_type
        self.sprite = pygame.transform.scale(pygame.image.load(Tower.tower_data[tower_type]["sprite"]).convert_alpha(), (40,40))
        #self.radius_sprite = radius_sprite
        self.radius = Tower.tower_data[tower_type]["radius"]
        self.damage = Tower.tower_data[tower_type]["damage"]
        self.rate_of_fire = Tower.tower_data[tower_type]["rate_of_fire"]
        self.location = (round((location[0]-30)/40)*40, round((location[1]-30)/40)*40)
        self.isClicked = False
        self.firingAt = None
        self.recharge = self.rate_of_fire
        self.zapping = None

class Basic_Tower(Tower):
    def __init__(self, tower_type, location):
        super().__init__(tower_type, location)

    def handle_firing(self, enemies):
        if self.recharge >= self.rate_of_fire and len(enemies) != 0:
            self.recharge = 0
            closest = (enemies[0], distance_between_points(self.location, enemies[0].location)) 
            for enemy in enemies:
                if distance_between_points(self.location, enemy.location) < closest[1]:
                    closest = (enemy, distance_between_points(self.location, enemy.location))
            if closest[1] <= self.radius: 
                self.firingAt = closest[0]
                self.zapping = closest[0]
        elif self.recharge < self.rate_of_fire:
            self.recharge += 1
            self.firingAt = None
        else:
            self.firingAt = None
        if self.recharge > 10:
            self.zapping = None
        



#### ====================================================================================================================== ####
#############                                       TOWER_FUNCTIONS                                                #############
#### ====================================================================================================================== ####

def update_tower(tower, game_data):
    tower.handle_firing(game_data["enemies"])
    if tower.firingAt is not None:
        tower.firingAt.takeHit(tower.damage)


def render_tower(tower, screen, settings):
    ''' Helper function that renders a single provided Tower.
    Input: Tower Object, screen (pygame display), Settings Object
    Output: None
    '''
    screen.blit(tower.sprite, tower.location)
    if tower.name == "Basic Tower Lv.1":
        if tower.zapping is not None:
            pygame.draw.aaline(screen, colours.magenta, (tower.location[0]+20, tower.location[1]+20), (tower.zapping.location[0]+20, tower.zapping.location[1]+20))
