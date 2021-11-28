import pygame
import pytmx

pygame.init()

resolution_screen = (160, 144)
resolution_window = (640, 480)
surface_window = pygame.display.set_mode(resolution_window)
surface_screen = pygame.Surface(resolution_screen)

pygame.display.set_caption("Mystic Quest")
clock = pygame.time.Clock()

map_hi = "{:02x}".format(0)
map_low = "{:02x}".format(0)

tm = pytmx.load_pygame(f"en/mapas/mapa_{map_hi}_{map_low}.tmx")

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
                surface_screen.blit(
                    tile,
                    (
                        (x - map_screen_index_x - 1) * tm.tilewidth,
                        (y - map_screen_index_y - 1) * tm.tileheight,
                    ),
                )

        scaled_win = pygame.transform.scale(surface_screen, surface_window.get_size())
        surface_window.blit(scaled_win, (0, 0))
        pygame.display.update()

        clock.tick(30)


if __name__ == "__main__":
    main()
    pygame.quit()
