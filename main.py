import pygame
import pytmx

pygame.init()

display_width = 160
display_height = 144
screen = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption("Mystic Quest")
clock = pygame.time.Clock()

tm = pytmx.load_pygame("en/mapas/mapa_00_00.tmx")

MAP_WIDTH = 10
MAP_HEIGHT = 8


def main():
    map_screen_index_x = 0
    map_screen_index_y = 0
    
    tile_layer = tm.get_layer_by_name("Tile Layer 1")
    
    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    done = True
                elif event.key == pygame.K_x:
                    map_screen_index_x += MAP_WIDTH
                elif event.key == pygame.K_y:
                    map_screen_index_y += MAP_HEIGHT

        
        for (
            x,
            y,
            gid,
        ) in tile_layer:
            if (
                x > map_screen_index_x
                and x <= map_screen_index_x + MAP_WIDTH
                and y > map_screen_index_y
                and y <= map_screen_index_y + MAP_HEIGHT
            ):
                tile = tm.get_tile_image_by_gid(gid)
                screen.blit(
                    tile,
                    (
                        (x - map_screen_index_x - 1) * tm.tilewidth,
                        (y - map_screen_index_y - 1) * tm.tileheight,
                    ),
                )
        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
    pygame.quit()
