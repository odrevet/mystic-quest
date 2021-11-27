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

map_index_x = 0
map_index_y = 0

def main():
    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    done = True

        tile_layer = tm.get_layer_by_name("Tile Layer 1")
        for (
            x,
            y,
            gid,
        ) in tile_layer:
            if x < MAP_WIDTH and y < MAP_HEIGHT:
                tile = tm.get_tile_image_by_gid(gid)
                screen.blit(tile, (x * tm.tilewidth, y * tm.tileheight))

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
    pygame.quit()
