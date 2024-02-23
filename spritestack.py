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
dir = None
display_size = None
screen_size = None
fps = None

with open("sprite_stack_tool.json","r") as settings_json:
    json_settings = json.load(settings_json)
    sprite_sheet = json_settings["sprite_sheet"]
    dir = json_settings["directory"] 
    display_size = tuple(json_settings["display_size"])
    screen_size = tuple(json_settings["screen_size"])
    fps = json_settings["fps"]

screen = pygame.display.set_mode(screen_size, 0, 32)

display = pygame.Surface(display_size)

# sprite_sheet = pygame.image.load('assets/tets_7.png')
if dir == "n":
    dir = 'assets/tile_car/'


images = None

if sprite_sheet == True:
    ...
else:
    images = [pygame.image.load(dir + img) for img in os.listdir(dir)]

clock = pygame.time.Clock()

# cache:
# caching the whole stack

def render_stack(surf, images, pos, rotation, spread=1):
    
    rotated_img = pygame.transform.rotate(images[0], rotation)
    pygame.draw.rect(surf,(180,180,255), rotated_img.get_rect())
    pygame.draw.rect(surf,(255,0,0), images[0].get_rect(),1)

    for i, img in enumerate(images):
        rotated_img = pygame.transform.rotate(img, rotation)
        # pygame.draw.rect(surf,(255,0,0), rotated_img.get_rect())
        surf.blit(rotated_img, (pos[0] - rotated_img.get_width() // 2, pos[1] - rotated_img.get_height() // 2 - i * spread))
        #surf.blit(rotated_img, (0, 0 - i * spread))
        # print((pos[0] - rotated_img.get_width() // 2, pos[1] - rotated_img.get_height() // 2 - i * spread))
        debug_print(rotated_img.get_bounding_rect().centerx, rotated_img.get_bounding_rect().centery - i * spread)

        
frame = 0
space_pressed = False
while True:
    display.fill((0, 0, 0))
    
    #display.blit(pygame.transform.rotate(images[0], 30), (display_size[0]/2,display_size[1]/2),)

    render_stack(display, images, (display_size[0]/2,display_size[1]/2), frame)
    
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
                print(space_pressed)
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
    pygame.display.set_caption(f"{clock.get_fps():.2f}")
    
