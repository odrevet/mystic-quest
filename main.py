import pygame
import pytmx
import re
from script import Script
from hero import *


def read_scripts():
    with open("en/scripts/scripts.txt", "r") as file:
        scripts_str = file.read()
        scripts_arr = re.split(
            r"--- script: ([a-f0-9]{4}) addr: ([a-f0-9]{4}) ------------------.*",
            scripts_str,
        )

        variable_declarations = scripts_arr.pop(0)

        scripts = []
        for i in range(0, len(scripts_arr), 3):
            scripts.append(
                Script(scripts_arr[i], scripts_arr[i + 1], scripts_arr[i + 2])
            )

        return variable_declarations, scripts


def main():
    pygame.init()

    resolution_screen = (160, 144)
    resolution_window = (640, 480)
    surface_window = pygame.display.set_mode(resolution_window)
    surface_screen = pygame.Surface(resolution_screen)

    pygame.display.set_caption("Mystic Quest")
    clock = pygame.time.Clock()

    # map
    map_hi = "{:02x}".format(0)
    map_low = "{:02x}".format(0)

    tm = pytmx.load_pygame(f"en/mapas/mapa_{map_hi}_{map_low}.tmx")

    MAP_WIDTH = 10
    MAP_HEIGHT = 8

    map_screen_index_x = 5 * MAP_WIDTH
    map_screen_index_y = 6 * MAP_HEIGHT


    event_layer= tm.get_layer_by_name("Object Layer eventos")
    for event in event_layer:
        print(event.x, event.y, event.properties['nroScript'])

    tile_layer = tm.get_layer_by_name("Tile Layer 1")



    # hero
    hero = Hero()

    done = False

    while not done:
        ## Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    done = True

                if event.key == pygame.K_LEFT:
                    hero.is_moving = True
                    hero.direction = Direction.LEFT
                    hero.frame_index = 5
                    hero.flip = False
                if event.key == pygame.K_RIGHT:
                    hero.is_moving = True
                    hero.direction = Direction.RIGHT
                    hero.frame_index = 5
                    hero.flip = True
                if event.key == pygame.K_UP:
                    hero.is_moving = True
                    hero.direction = Direction.UP
                    hero.frame_index = 3
                    hero.flip = False
                if event.key == pygame.K_DOWN:
                    hero.is_moving = True
                    hero.direction = Direction.DOWN
                    hero.frame_index = 1
                    hero.flip = False

                if event.mod & pygame.KMOD_LSHIFT:
                    if event.key == pygame.K_UP:
                        map_screen_index_y -= MAP_HEIGHT
                    elif event.key == pygame.K_DOWN:
                        map_screen_index_y += MAP_HEIGHT
                    elif event.key == pygame.K_LEFT:
                        map_screen_index_x -= MAP_WIDTH
                    elif event.key == pygame.K_RIGHT:
                        map_screen_index_x += MAP_WIDTH
            elif event.type == pygame.KEYUP:
                if event.key in [
                    pygame.K_LEFT,
                    pygame.K_RIGHT,
                    pygame.K_UP,
                    pygame.K_DOWN,
                ]:
                    hero.is_moving = False

        # update hero location
        if hero.is_moving:
            if hero.direction == Direction.UP:
                hero.y -= 1
            if hero.direction == Direction.RIGHT:
                hero.x += 1
            if hero.direction == Direction.DOWN:
                hero.y += 1
            if hero.direction == Direction.LEFT:
                hero.x -= 1

        # check boundaries
        if(hero.x + hero.SIZE > tm.tilewidth * MAP_WIDTH):
            hero.x = 0
            map_screen_index_x += MAP_WIDTH
        elif(hero.x < 0):
            hero.x = 144
            map_screen_index_x -= MAP_WIDTH
        elif(hero.y + hero.SIZE > 160):
            hero.y = 0
            map_screen_index_y += MAP_HEIGHT
        elif(hero.y < 0):
            hero.y = 120
            map_screen_index_y -= MAP_HEIGHT

        ## Display
        # map
        for (
            x,
            y,
            gid,
        ) in tile_layer:
            if (
                x > map_screen_index_x - 1
                and x <= map_screen_index_x + MAP_WIDTH - 1
                and y > map_screen_index_y - 1
                and y <= map_screen_index_y + MAP_HEIGHT - 1
            ):
                tile = tm.get_tile_image_by_gid(gid)
                surface_screen.blit(
                    tile,
                    (
                        (x - map_screen_index_x) * tm.tilewidth,
                        (y - map_screen_index_y) * tm.tileheight,
                    ),
                )

        # hero
        hero.draw(surface_screen)

        # update display
        scaled_win = pygame.transform.scale(surface_screen, surface_window.get_size())
        surface_window.blit(scaled_win, (0, 0))
        pygame.display.update()

        clock.tick(30)


if __name__ == "__main__":
    main()
    pygame.quit()
