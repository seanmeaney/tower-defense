#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

from helper_functions import *
import pygame
import random

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
        self.r_locations = []
        row = 0; col = 0
        # for cell_row in csv_loader("data/map.csv", readall=True):
        #     for cell_col in cell_row:
        #         if len(cell_col) > 1:
        #             cell_col = cell_col[-1]
        #         self.map_data[(col, row)] = { "value": cell_col, "sprite": pygame.transform.scale(pygame.image.load(Map.legend_data[cell_col]["sprite"]), settings.tile_size) }
        #         if cell_col == "R":
        #             t_s = settings.tile_size[0] #should probably use the seperate x and y stuff
        #             self.r_locations.append((40 + col*t_s - (t_s/2) , 40 + row*t_s - t_s/2))
        #         col += 1
        #     row += 1; col = 0
        if random_bool:
            start = (1,0)
            end = (16,19)
            self.map_data = {(col,row): self.temp("B", settings) for col in range(20) for row in range(20)}
            self.map_data[start] = {"value": "S", "sprite": pygame.transform.scale(pygame.image.load(Map.legend_data["S"]["sprite"]), settings.tile_size)}
            self.map_data[end] = {"value": "E", "sprite": pygame.transform.scale(pygame.image.load(Map.legend_data["E"]["sprite"]), settings.tile_size)}
            cur = list(start)
            r = random
            while (((end[0]-cur[0])!= 0 and (end[1]-cur[1]))!= 0): 
                d = r.randint(0,4)
                if d == 0 and cur[0] < 18: #down
                    cur[0] += 1
                    if not self.map_data[tuple(cur)]["value"] == "B":
                        cur[0] -= 1
                elif d == 0 and cur[0] > 1: #up
                    cur[0] -= 1
                    if not self.map_data[tuple(cur)]["value"] == "B":
                        cur[0] += 1
                elif d == 1 and cur[1] < 18: #right
                    cur[1] += 1
                    if not self.map_data[tuple(cur)]["value"] == "B":
                        cur[1] -= 1
                elif d == 1 and cur[1] > 1: #left
                    cur[1] -= 1
                    if not self.map_data[tuple(cur)]["value"] == "B":
                        cur[1] += 1
                # if self.map_data[tuple(cur)]["value"] == "B":
                self.map_data[tuple(cur)] = self.temp("R",settings)
        else:
            row = 0; col = 0
            for cell_row in csv_loader("data/map.csv", readall=True):
                for cell_col in cell_row:
                    if len(cell_col) > 1:
                        cell_col = cell_col[-1]
                    self.map_data[(col, row)] = { "value": cell_col, "sprite": pygame.transform.scale(pygame.image.load(Map.legend_data[cell_col]["sprite"]), settings.tile_size) }
                    col += 1
                row += 1; col = 0
            

    def temp(self, value,settings):
        return {"value": value, "sprite": pygame.transform.scale(pygame.image.load(Map.legend_data[value]["sprite"]), settings.tile_size)}
#### ====================================================================================================================== ####
#############                                        MAP_FUNCTIONS                                                 #############
#### ====================================================================================================================== ####



def render_map(map, screen, settings):
    ''' Helper function that renders the Map.
    Input: Map Object, screen (pygame display), Settings Object
    Output: None
    '''
    for cell in map.map_data:
        screen.blit(map.map_data[cell]["sprite"], [cell[0] * settings.tile_size[0], cell[1] * settings.tile_size[1]])

def check_location(map, settings, location):
    if location[0] > 0 and location[0] < settings.window_size[1] and location[1] > 0 and location[1] < settings.window_size[0]-200:
        test = (int(round(location[0]/20) * 20), int(round(location[1]/20) * 20))
        if test in map.r_locations:
            return False
        else: 
            return True
    else:
        return False
