#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

from helper_functions import *
from settings import *
from shop import *
from tower import *
from enemy import *
from map import *
import pygame
import sys

#### ====================================================================================================================== ####
#############                                         INITIALIZE                                                   #############
#### ====================================================================================================================== ####

def initialize():
    ''' Initialization function - initializes various aspects of the game including settings, shop, and more.
    Input: None
    Output: game_data dictionary
    '''
    # Initialize Pygame
    pygame.init()
    pygame.display.set_caption("COMP 1501 - Tutorial 7: Tower Defense (TD) Base Code")

    # Initialize the Settings Object
    settings = Settings()

    # Initialize game_data and return it
    game_data = { "screen": pygame.display.set_mode(settings.window_size),
                  "current_currency": settings.starting_currency,
                  "current_wave": 1,
                  "stay_open": True,
                  "selected_tower": None,
                  "clicked": False,
                  "settings": settings,
                  "towers": [Basic_Tower("Basic Tower Lv.1", (3,3))],
                  "enemies": spawn_enemies(1),
                  "shop": Shop("Space", settings),
                  "map": Map(settings, True) }

    return game_data

#### ====================================================================================================================== ####
#############                                           PROCESS                                                    #############
#### ====================================================================================================================== ####

def spawn_enemies(wave_number):
    if wave_number == 1:            #temporary just for first wave
        return [Enemy("Lesser Alien", (1,-1)), Enemy("Lesser Alien", (1,-2)), Enemy("Lesser Alien", (1,-3)), Enemy("Lesser Alien", (1,-4))]
    else:
        #just to test the waves, real implementation needs to spawn different types and the current numbers are probalbly not balanced
        return [Enemy("Lesser Alien", (1,-x)) for x in range(4*wave_number)] 



def process(game_data):
    ''' Processing function - handles all form of user input. Raises flags to trigger certain actions in Update().
    Input: game_data dictionary
    Output: None
    '''
    pos = pygame.mouse.get_pos()
    for event in pygame.event.get():

        # Handle [X] press
        if event.type == pygame.QUIT:
            game_data["stay_open"] = False

        # Handle Mouse Button Down
        if event.type == pygame.MOUSEBUTTONDOWN:
            game_data["clicked"] = True
            game_data["selected_tower"] = False
            if (t:=game_data["shop"].selected_item):
                game_data["shop"].clicked_item = t
                game_data["shop"].selected_item = None
                game_data["selected_tower"] = True

        # Handle Mouse Button Up
        if event.type == pygame.MOUSEBUTTONUP:
            game_data["clicked"] = False
            if game_data["selected_tower"] : 
                if check_location(game_data["map"],game_data["settings"],pos): #temporary, also needs a check for money
                    game_data["selected_tower"] = False
                    game_data["towers"].append(Basic_Tower(game_data["shop"].clicked_item,tuple(map(lambda x: round((x-20)/20) , pos))))
                    game_data["shop"].clicked_item = None
                else:
                    game_data["selected_tower"] = False
                    game_data["shop"].clicked_item = None


#### ====================================================================================================================== ####
#############                                            UPDATE                                                    #############
#### ====================================================================================================================== ####

def update(game_data):
    ''' Updating function - handles all the modifications to the game_data objects (other than boolean flags).
    Input: game_data
    Output: None
    '''
    update_shop(game_data["shop"], game_data["current_currency"], game_data["settings"])
    update_all_enemies(game_data)
    update_all_towers(game_data)
    
def update_all_enemies(game_data):
    game_data["enemies"] = [i for i in game_data["enemies"] if i.alive == True]
    if game_data["enemies"]:
        for enemy in game_data["enemies"]:
            update_enemy(enemy, game_data)
    else:
        game_data["current_wave"] +=1
        game_data["enemies"] = spawn_enemies(game_data["current_wave"])


def update_all_towers(game_data):
    for tower in game_data["towers"]:
        update_tower(tower, game_data)

#### ====================================================================================================================== ####
#############                                            RENDER                                                    #############
#### ====================================================================================================================== ####

def render(game_data):
    ''' Rendering function - displays all objects to screen.
    Input: game_data
    Output: None
    '''
    render_map(game_data["map"], game_data["screen"], game_data["settings"])
    render_shop(game_data["shop"], game_data["screen"], game_data["settings"], game_data["current_currency"])
    for enemy in game_data["enemies"]:
        render_enemy(enemy, game_data["screen"], game_data["settings"])
    for tower in game_data["towers"]:
        render_tower(tower, game_data["screen"], game_data["settings"])
    pygame.display.update()

#### ====================================================================================================================== ####
#############                                             MAIN                                                     #############
#### ====================================================================================================================== ####

def main():
    ''' Main function - initializes everything and then enters the primary game loop.
    Input: None
    Output: None
    '''
    # Initialize all required variables and objects
    game_data = initialize()

    # Begin Central Game Loop
    while game_data["stay_open"]:
        process(game_data)
        update(game_data)
        render(game_data)

    # Exit pygame and Python
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()