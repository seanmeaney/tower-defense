#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

from helper_functions import *
import pygame
import random
import tile

#### ====================================================================================================================== ####
#############                                          MAP_CLASS                                                   #############
#### ====================================================================================================================== ####

class Map:
    ''' Map Class - represents a single Map Object. '''
    # Represents common data for all Maps - only loaded once, not per new Map (Class Variable)
    legend_data = {}
    for legend in csv_loader("data/legend.csv"):
        legend_data[legend[0]] = { "type": legend[1], "sprite": legend[2] }
    def __init__(self, settings, random_bool):
        ''' Initialization for Map.
        Input: Settings Oject
        Output: A Map Object
        '''
        self.map_data = {}

        row = 0; col = 0
        for cell_row in csv_loader("data/map.csv", readall=True):
            for cell_col in cell_row:
                if len(cell_col) > 1:
                    cell_col = cell_col[-1]

                if cell_col == "W":
                    self.map_data[(col, row)] = tile.wallTile(col, row)

                elif cell_col == "P":
                    self.map_data[(col, row)] = tile.pathTile(col, row)
                
                elif cell_col == "S":
                    self.map_data[(col, row)] = tile.startTile(col, row)

                elif cell_col == "F":
                    self.map_data[(col, row)] = tile.finishTile(col, row)
                
                col += 1
            row += 1; col = 0
        # if random_bool:
        #     start = (1,0)
        #     end = (16,19)
        #     self.map_data = {(col,row): self.temp("B", settings) for col in range(20) for row in range(20)}
        #     self.map_data[start] = {"value": "S", "sprite": pygame.transform.scale(pygame.image.load(Map.legend_data["S"]["sprite"]), settings.tile_size)}
        #     self.map_data[end] = {"value": "E", "sprite": pygame.transform.scale(pygame.image.load(Map.legend_data["E"]["sprite"]), settings.tile_size)}
        #     cur = list(start)
        #     r = random
        #     while ((end[0]-cur[0]) + (end[1]-cur[1]))> 1:
        #         d = r.randint(0,4)
        #         if d == 0 and cur[0] < 18: #down
        #             cur[0] += 1
        #         elif d == 1 and cur[0] > 1: #up
        #             cur[0] -= 1
        #         elif d == 2 and cur[1] < 18: #right
        #             cur[1] += 1
        #         elif d == 2 and cur[1] > 1: #left
        #             cur[1] -= 1
        #         self.map_data[tuple(cur)] = self.temp("R",settings)
        # else:
        #     row = 0; col = 0
        #     for cell_row in csv_loader("data/map.csv", readall=True):
        #         for cell_col in cell_row:
        #             if len(cell_col) > 1:
        #                 cell_col = cell_col[-1]
        #             self.map_data[(col, row)] = { "value": cell_col, "sprite": pygame.transform.scale(pygame.image.load(Map.legend_data[cell_col]["sprite"]), settings.tile_size) }
        #             col += 1
        #         row += 1; col = 0
            

    def temp(self, value,settings):
        return {"value": value, "sprite": pygame.transform.scale(pygame.image.load(Map.legend_data[value]["sprite"]), settings.tile_size)}
    
    def build_wall(self, pos):
        fixed_pos = (int((round(pos[0]-20)/40)), int(round((pos[1]-20)/40)))
        if self.map_data[fixed_pos].type() == "path":
            self.map_data[fixed_pos] = tile.wallTile(fixed_pos[0], fixed_pos[1])

    def build_path(self, pos):
        print("Inside Build_Path")
        fixed_pos = (int((round(pos[0]-20)/40)), int(round((pos[1]-20)/40)))
        if self.map_data[fixed_pos].type() == "wall":
            self.map_data[fixed_pos] = tile.pathTile(fixed_pos[0], fixed_pos[1])

    def check_location(self, location):
        if location[0] > 0 and location[1] > 0:
            fixed_location = (int((round(location[0]-20)/40)), int(round((location[1]-20)/40)))
            if self.map_data[fixed_location].type() == "wall":
                return True
        return False
    def fix_location(self, location):
        fixed = (int((round(location[0]-20)/40)), int(round((location[1]-20)/40)))
        return fixed
#### ====================================================================================================================== ####
#############                                        MAP_FUNCTIONS                                                 #############
#### ====================================================================================================================== ####



def render_map(map, screen, settings):
    ''' Helper function that renders the Map.
    Input: Map Object, screen (pygame display), Settings Object
    Output: None
    '''
    for cell in map.map_data:
        screen.blit(map.map_data[cell].sprite, [cell[0] * settings.tile_size[0], cell[1] * settings.tile_size[1]])

def check_location(map, settings, location, other_towers = None):
    if location[0] > 0 and location[0] < settings.window_size[1] and location[1] > 0 and location[1] < settings.window_size[0]-200:
        fixed_location = fix_location(location)
        if map.map_data[fixed_location].type() == "wall":
            other = fixed_location[0] * 40,fixed_location[1]*40
            for tower in other_towers:
                if other == tower.location:
                    return False
            return True
        if map.map_data[fixed_location].type() == "end":
            return "l's"
    return False

def fix_location(location):
    fixed = (int((round(location[0]-20)/40)), int(round((location[1]-20)/40)))
    return fixed

def unfix_location(location):
    unfixed = ((location[0]*40)+20, (location[1]*40)+20)
    return unfixed




