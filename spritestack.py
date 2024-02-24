import sys
import os
import math
import json
import pygame
pygame.init()

debug = False
def debug_print(*values: object, sep: str | None = " ", end: str | None = "\n", file: None = None, flush = False, tags:list = [])->None:
    """
    Print statement that gets called only when the debug of the application is equal to `True`.
    Basically the Print function, but only print when `debug == True`
    """
    if debug:
        print(*values, sep=sep, end=end, file=file, flush=flush)


json_settings = None
sprite_sheet = None
stile_size = None
dir = None
display_size = None
screen_size = None
fps = None
color = None

try:
    with open("sprite_stack_tool.json","r") as settings_json:
        json_settings = json.load(settings_json)
        sprite_sheet: bool = json_settings["sprite_sheet"]
        stile_size: tuple = json_settings["sprite_sheet_tile_size"]
        dir = json_settings["directory"] 
        display_size = tuple(json_settings["display_size"])
        screen_size = tuple(json_settings["screen_size"])
        fps = json_settings["fps"]
        color = json_settings["bg_color"]
        stack_space = json_settings["stacking_space"]
except:
    with open("sprite_stack_tool.json","w") as settings_json:
        default_data = {
            "sprite_sheet" : False,
            "sprite_sheet_tile_size" : [32,32],
            "directory" : "assets/formula/",
            "display_size" : [50,50],
            "screen_size" : [500,500],
            "fps" : 60,
            "bg_color" : [0,0,0],
            "stacking_space" : 1
        }
        json.dump(default_data,settings_json)
        sprite_sheet: bool = default_data["sprite_sheet"]
        stile_size: tuple = default_data["sprite_sheet_tile_size"]
        dir = default_data["directory"] 
        display_size = tuple(default_data["display_size"])
        screen_size = tuple(default_data["screen_size"])
        fps = default_data["fps"]
        color = default_data["bg_color"]
        stack_space = default_data["stacking_space"]



screen = pygame.display.set_mode(screen_size, 0, 32)

display = pygame.Surface(display_size)

# sprite_sheet = pygame.image.load('assets/tets_7.png')
if dir == "n":
    dir = 'assets/tile_car/'


images = []
rectangles = []

# loading stuff
if sprite_sheet:
    sheet = pygame.image.load(dir).convert_alpha()
    column_sprites = sheet.get_width() // stile_size[0]
    row_sprites = sheet.get_height() // stile_size[1]

    for y in range(0,row_sprites):
        rectangles += [pygame.FRect(x, y, stile_size[0], stile_size[1]) for x in range(0,sheet.get_width(),stile_size[0])]

    # images = [sheet, rectangles]
    for rect in rectangles:
        temp_image = pygame.Surface(stile_size)
        temp_image.fill((1,0,0))
        temp_image.blit(sheet,(0,0),rect)
        temp_image.set_colorkey((1,0,0))
        images += [temp_image]

else:
    list_dir = os.listdir(dir)
    list_dir.sort()
    images = [pygame.image.load(dir + img) for img in list_dir]
    debug_print(images, os.listdir(dir), list_dir)
    temp_images = []
    for i in images:
        temp_images += [i.convert_alpha()]
    
    images = temp_images

clock = pygame.time.Clock()

# cache:
# caching the whole stack

def render_stack(surf, images, pos, rotation, spread=10):
    
    rotated_img = pygame.transform.rotate(images[0], rotation)
    if debug:
        pygame.draw.rect(surf,(180,180,255), rotated_img.get_rect())
        pygame.draw.rect(surf,(255,0,0), images[0].get_rect(),1)

    for i, img in enumerate(images):
        rotated_img = pygame.transform.rotate(img, rotation)

        surf.blit(rotated_img, (pos[0] - rotated_img.get_width() // 2, pos[1] - rotated_img.get_height() // 2 - i * spread))

        debug_print(rotated_img.get_bounding_rect().centerx, rotated_img.get_bounding_rect().centery - i * spread)

        
frame = 0
space_pressed = False
while True:
    display.fill(color)
    
    #display.blit(pygame.transform.rotate(images[0], 30), (display_size[0]/2,display_size[1]/2),)
    render_stack(display, images, (display_size[0]/2,display_size[1]/2), frame, stack_space)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_SPACE:
                space_pressed = True
                debug_print(space_pressed)
            if event.key == pygame.K_d:
                debug = False if debug else True
                print("Debug mode is:", "on" if debug else "off")

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                space_pressed = False

    debug_print(space_pressed)
    if space_pressed != True:
        frame += 1
        if frame == 360:
            frame = 0

    screen.blit(pygame.transform.scale(display, screen.get_size()), (0, 0))
    pygame.display.update()
    clock.tick(fps)
    pygame.display.set_caption(f"{clock.get_fps():.2f} : FPS")
    
