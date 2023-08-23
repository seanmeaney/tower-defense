#### ====================================================================================================================== ####
#############                                           IMPORTS                                                    #############
#### ====================================================================================================================== ####

from helper_functions import *
import pygame
import tower

#### ====================================================================================================================== ####
#############                                          SHOP_CLASS                                                  #############
#### ====================================================================================================================== ####

class Shop:
    ''' Settings Class - represents a single Setting Object. '''
    def __init__(self, theme, settings):
        self.location = [800, 0]
        self.size = [200, settings.window_size[1]]
        self.items = []
        self.ui_data = ui_data()
        for item_data in csv_loader("data/shop.csv"):
            self.items.append(shop_item(item_data))
        self.clicked_item = None
        item_location = [self.location[0] + (self.size[0] - 2 * self.ui_data.item_size) / 3, self.location[1] + (self.size[0] - 2 * self.ui_data.item_size) / 3 + 150]
        for item in self.items:
            item.location = item_location
            if item_location[0] + self.ui_data.item_size * 2 > settings.window_size[0]:
                item_location = [self.location[0] + (self.size[0] - 2 * self.ui_data.item_size) / 3, item_location[1] + (self.size[0] - 2 * self.ui_data.item_size) / 3 + self.ui_data.item_size + 25]
            else:
                item_location = [item_location[0] + (self.size[0] - 2 * self.ui_data.item_size) / 3 + self.ui_data.item_size, item_location[1]]

#### ====================================================================================================================== ####
#############                                         SHOP_FUNCTIONS                                               #############
#### ====================================================================================================================== ####

def update_shop(shop, current_currency, settings):
    ''' Helper function that updates the Shop.
    Input: Shop Object, current currency (int), Settings Object
    Output: None
    '''
    # Handle Mouse-Over tower in shop, sets it as 'selected_item' for rendering purposes
    # Also handles unaffordable towers in shop (switched to available to False)
    shop.selected_item = None
    (mX, mY) = pygame.mouse.get_pos()
    for item in shop.items:
        if current_currency < item.cost:
            item.available = False
        else:
            item.available = True
        if (mX > item.location[0] and mX < item.location[0] + shop.ui_data.item_size) and (mY > item.location[1] and mY < item.location[1] + shop.ui_data.item_size):
                shop.selected_item = item

def render_shop(shop, screen, settings, current_currency):
    ''' Helper function that renders the Shop.
    Input: Shop Object, screen (pygame display), Settings Object, current currency (int)
    Output: None
    '''
    # Rendering Shop Background
    for row in range(settings.window_size[1] // settings.tile_size[1]):
        for col in range(settings.window_size[0] // settings.tile_size[0]):
            screen.blit(shop.ui_data.background, (shop.location[0] + col * settings.tile_size[0], shop.location[1] + row * settings.tile_size[1]))

    # Rendering Top Section
    shop_text = settings.title_font.render("Shop", True, (254, 207, 0))
    screen.blit(shop_text, (shop.location[0] + shop_text.get_width() // 3, 15))

    # Rendering Towers
    for item in shop.items:
        # -- Optional Split for Unavailable Icons --
        if item.available:
            screen.blit(shop.ui_data.item_background, item.location)
            screen.blit(item.sprite, (item.location[0]+10, item.location[1]+10))
        else:
            screen.blit(shop.ui_data.item_background, item.location)
            screen.blit(item.sprite, (item.location[0]+10, item.location[1]+10))
            
        # Rendering Item Information (Text)
        item_cost_text = settings.font.render("{}".format(item.cost), True, (254, 207, 0))
        screen.blit(item_cost_text, (item.location[0] + 30, item.location[1] + shop.ui_data.item_size - 2))
        screen.blit(shop.ui_data.currency, (item.location[0], item.location[1] + shop.ui_data.item_size + 3))
    
    # Handle Player Currency
    current_currency_text = settings.font.render("{}".format(current_currency), True, (254, 207, 0))
    screen.blit(current_currency_text, (shop.location[0] + current_currency_text.get_width() // 3 + 30, 645))
    screen.blit(shop.ui_data.currency, (shop.location[0] + 5, 650))

    # Handle Mouse Over Tower
    if shop.selected_item is not None:
        selected_tower_text = settings.font.render(shop.selected_item.name, True, (254, 207, 0))
        screen.blit(selected_tower_text, (shop.location[0] + selected_tower_text.get_width() // 8, 100))

    # Handle Selected Tower
    if shop.clicked_item is not None:
        screen.blit(pygame.transform.scale(shop.ui_data.radius_sprite, (shop.clicked_item.radius * 2, shop.clicked_item.radius * 2)), (pygame.mouse.get_pos()[0] - shop.clicked_item.radius, pygame.mouse.get_pos()[1] - shop.clicked_item.radius))
        screen.blit(shop.clicked_item.sprite, (pygame.mouse.get_pos()[0] - shop.ui_data.item_size // 2, pygame.mouse.get_pos()[1] - shop.ui_data.item_size // 2))



class shop_item():
    def __init__(self, csv_data):
        self.name = csv_data[0]
        self.type = csv_data[1]
        self.sprite = pygame.transform.scale(pygame.image.load(csv_data[2]).convert_alpha(), (60,60))
        self.available = csv_data[3]
        self.cost = int(csv_data[4])
        self.radius = int(csv_data[5])
        self.location = None
        self.class_name = csv_data[6]
    def construct_item(self, args):
        if args[0] == "Basic Tower Lv.1":
            return tower.Basic_Tower(args[0], args[1])
        elif args[0] == "Basic Tower Lv.2":
            return tower.Medium_Tower(args[0], args[1])

class ui_data():
    def __init__(self):
        for ui in csv_loader("data/ui.csv"):
            self.background = pygame.image.load(ui[3]).convert_alpha()
            self.currency = pygame.transform.scale(pygame.image.load(ui[4]).convert_alpha(), (24, 24))
            self.item_size = int(ui[5])
            self.item_background = pygame.transform.scale(pygame.image.load(ui[1]).convert_alpha(), (self.item_size, self.item_size))
            self.item_background_disabled = pygame.transform.scale(pygame.image.load(ui[2]).convert_alpha(), (self.item_size, self.item_size))
            self.radius_sprite = pygame.image.load(ui[6]).convert_alpha()
