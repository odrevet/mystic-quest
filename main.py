import pygame
import pytmx

pygame.init()


display_width = 160
display_height = 144

screen = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption("Mystic Quest")
clock = pygame.time.Clock()

# load map data
tm = pytmx.load_pygame("en/mapas/mapa_00_00.tmx")


def main():

    if __debug__:
        for visible_layer in tm.visible_layers:
            print(visible_layer)

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        tile_layer = tm.get_layer_by_name("Tile Layer 1")
        for (
            x,
            y,
            gid,
        ) in tile_layer:
            tile = tm.get_tile_image_by_gid(gid)
            screen.blit(tile, (x * tm.tilewidth, y * tm.tileheight))

        pygame.display.update()
        clock.tick(30)


if __name__ == "__main__":
    main()
    pygame.quit()
