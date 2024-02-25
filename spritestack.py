import sys
import os
import math
import json
import pygame
pygame.init()

__name__ = "SpriteStack Viewer"
__version__ = "v0.1.1a"

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
dir1 = None
coords_1 = None
display_size = None
screen_size = None
fps = None
color = None
multiple_sprites = None
dir2 = None
coords_2 = None

# i know that the amount of the sprites can be abstracted, but that can just be implemented in the base game for now

try:
    with open("sprite_stack_tool.json","r") as settings_json:
        json_settings = json.load(settings_json)
        sprite_sheet: bool = json_settings["sprite_sheet"]
        stile_size: tuple = json_settings["sprite_sheet_tile_size"]
        dir1 = json_settings["directory"] 
        coords_1 = tuple(json_settings["coordinates_1"])
        display_size = tuple(json_settings["display_size"])
        screen_size = tuple(json_settings["screen_size"])
        fps = json_settings["fps"]
        color = json_settings["bg_color"]
        stack_space = json_settings["stacking_space"]
        multiple_sprites = json_settings["multiple_sprites"]
        dir2 = json_settings["directory2"]
        coords_2 = json_settings["coordinates_2"]

except:
    with open("sprite_stack_tool.json","w",encoding='utf-8') as settings_json:
        default_data = {
            "sprite_sheet" : False,
            "sprite_sheet_tile_size" : [32,32],
            "directory" : "assets/formula2/",
            "coordinates_1" : [-1,-1],
            "display_size" : [50,50],
            "screen_size" : [500,500],
            "fps" : 60,
            "bg_color" : [0,0,0],
            "stacking_space" : 1,
            "multiple_sprites" : False,
            "directory2" : "assets/formula/",
            "coordinates_2" : [20,20]
        }
        json.dump(default_data,settings_json,ensure_ascii=False, indent=4)
        sprite_sheet: bool = default_data["sprite_sheet"]
        stile_size: tuple = default_data["sprite_sheet_tile_size"]
        dir1 = default_data["directory"] 
        coords_1 = tuple(default_data["coordinates_1"])
        display_size = tuple(default_data["display_size"])
        screen_size = tuple(default_data["screen_size"])
        fps = default_data["fps"]
        color = default_data["bg_color"]
        stack_space = default_data["stacking_space"]
        multiple_sprites = default_data["multiple_sprites"]
        dir2 = default_data["directory2"]
        coords_2 = tuple(default_data["coordinates_2"])
         


screen = pygame.display.set_mode(screen_size, 0, 32)

display = pygame.Surface(display_size)

# sprite_sheet = pygame.image.load('assets/tets_7.png')
if dir1 == "n":
    dir1 = 'assets/tile_car/'




# loading stuff
def loading_sprite_stack(dir):
    images = []
    rectangles = []
    if sprite_sheet:
        sheet = pygame.image.load(dir).convert_alpha()
        column_sprites = sheet.get_width() // stile_size[0]
        row_sprites = sheet.get_height() // stile_size[1]

        for y in range(0,row_sprites):
            rectangles += [pygame.FRect(x, y, stile_size[0], stile_size[1]) for x in range(0,sheet.get_width(),stile_size[0])]

        # images = [sheet, rectangles]
        for rect in rectangles:
            temp_image = pygame.Surface(stile_size)
            # using the specific (1,0,0) color as a color key
            # if you want to use a black color just use (0,0,0)
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
    
    return images

images1 = []
images2 = []
if multiple_sprites:
    images2 = loading_sprite_stack(dir2)

images1 = loading_sprite_stack(dir2)


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

print(coords_1)   
if coords_1 == (-1,-1):
    coords_1 = (display_size[0]/2,display_size[1]/2)
    print(coords_1)     
frame = 0
space_pressed = False
while True:
    display.fill(color)
    

    if multiple_sprites:
        #display.blit(pygame.transform.rotate(images[0], 30), (display_size[0]/2,display_size[1]/2),)
        render_stack(display, images2, coords_2, frame, stack_space)

    render_stack(display, images1, coords_1, frame, stack_space)
    


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
    if debug:
        pygame.display.set_caption(f"{clock.get_fps():.2f} : FPS")
    else:
        pygame.display.set_caption(f"{__name__}")
    
