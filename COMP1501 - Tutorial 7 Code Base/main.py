#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

from pygame.constants import USEREVENT
from helper_functions import *
from settings import *
from shop import *
from tower import *
from enemy import *
from map import *
import pygame
import sys

NEXTLEVEL = USEREVENT + 20

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
                  "selected_item": None,
                  "clicked": False,
                  "settings": settings,
                  "towers": [],
                  "enemies": spawn_enemies(1),
                  "shop": Shop("Space", settings),
                  "map": Map(settings, False),
                  "font_queue" : [],
                  "event_inc" : 0,
                  "state" : "normal"}

    return game_data

#### ====================================================================================================================== ####
#############                                           PROCESS                                                    #############
#### ====================================================================================================================== ####

def spawn_enemies(wave_number):
    if wave_number == 1:            #temporary just for first wave
        return [Basic_Bot("Lesser Alien", (1,0))]
    elif wave_number < 4:
        #just to test the waves, real implementation needs to spawn different types and the current numbers are probalbly not balanced
        return [Basic_Bot("Lesser Alien", (1,-1*x)) for x in range(4*wave_number)] 
    elif wave_number >= 4:
        bots = [Basic_Bot("Lesser Alien", (1, -1*x)) for x in range(3*wave_number)]
        for y in range(int(2*wave_number/4)):
            bots.append(Basic_Bot("Heavy", (1, -1*y)))
        return bots
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

        if event.type == NEXTLEVEL:
            game_data["state"] = "normal"
            game_data["enemies"] = spawn_enemies(game_data["current_wave"])

        for f in game_data["font_queue"]:
            if f[3] == event.type:
                game_data["font_queue"].remove(f)
                if game_data["font_queue"] == []:
                    game_data["event_inc"] = 0

        # Handle Mouse Button Down
        if event.type == pygame.MOUSEBUTTONDOWN:
            game_data["clicked"] = True
            game_data["selected_item"] = False
            if (t:=game_data["shop"].selected_item):
                game_data["shop"].clicked_item = t
                game_data["shop"].selected_item = None
                game_data["selected_item"] = True

        # Handle Mouse Button Up
        if event.type == pygame.MOUSEBUTTONUP:
            game_data["clicked"] = False
            if game_data["selected_item"]: 
                if check_location(game_data["map"],game_data["settings"],pos):
                    if game_data["shop"].clicked_item.available:
                        game_data["current_currency"] -= game_data["shop"].clicked_item.cost
                        if game_data["shop"].clicked_item.type == "tower":
                            game_data["towers"].append(game_data["shop"].clicked_item.construct_item((game_data["shop"].clicked_item.name, pos)))
                    else:
                        add_to_font_queue(game_data,("Insufficent Funds!", True, (0,0,0)),(game_data["settings"].window_size[0]//2,0), 3000)
                if game_data["shop"].clicked_item.type == "wall" and game_data["shop"].clicked_item.available:
                    game_data["map"].build_wall(pos)
                if game_data["shop"].clicked_item.type == "path" and game_data["shop"].clicked_item.available:
                    game_data["map"].build_path(pos)
            game_data["selected_item"] = False
            game_data["shop"].clicked_item = None


#### ====================================================================================================================== ####
#############                                            UPDATE                                                    #############
#### ====================================================================================================================== ####

def add_to_font_queue(game_data, what, where,time):
    game_data["event_inc"]+=1
    game_data["font_queue"].append((what,where,time,USEREVENT+game_data["event_inc"]))
    pygame.time.set_timer(USEREVENT+game_data["event_inc"], time)

def update(game_data):
    ''' Updating function - handles all the modifications to the game_data objects (other than boolean flags).
    Input: game_data
    Output: None
    '''
    update_shop(game_data["shop"], game_data["current_currency"], game_data["settings"])
    if game_data["state"] == "normal":
        update_all_enemies(game_data)
        update_all_towers(game_data)
    
    
def update_all_enemies(game_data):
    enemies = game_data["enemies"]
    game_data["enemies"] = [i for i in game_data["enemies"] if i.alive == True]
    if game_data["enemies"]:
        for enemy in game_data["enemies"]:
            enemy.update(game_data)
            if check_location(game_data["map"], game_data["settings"], enemy.location) == "l's":
                game_data["stay_open"] = False
    else:
        game_data["current_wave"] +=1
        game_data["state"] = "temp"
        pygame.time.set_timer(NEXTLEVEL, 3000, True)

def update_all_towers(game_data):
    for tower in game_data["towers"]:
        update_tower(tower, game_data)

#### ====================================================================================================================== ####
#############                                            RENDER                                                    #############
#### ====================================================================================================================== ####

def render_font_queue(game_data):
    for f in game_data["font_queue"]: 
        game_data["screen"].blit(game_data["settings"].font.render(*f[0]),f[1])

def render(game_data):
    ''' Rendering function - displays all objects to screen.
    Input: game_data
    Output: None
    '''
    render_map(game_data["map"], game_data["screen"], game_data["settings"])
    render_shop(game_data["shop"], game_data["screen"], game_data["settings"], game_data["current_currency"])
    for enemy in game_data["enemies"]:
        enemy.render(game_data["screen"], game_data["settings"])
    for tower in game_data["towers"]:
        render_tower(tower, game_data["screen"], game_data["settings"])
    render_font_queue(game_data)
    if game_data["state"] == "temp":
        cur = str(game_data["current_wave"])
        game_data["screen"].blit(game_data["settings"].title_font.render("Stage" + cur, True, (255,255,255)), (375,0))
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