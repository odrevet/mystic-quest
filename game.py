import readline
import pygame
import pytmx

from interpreter import *
from hero import *


# Block size in tiles
BLOCK_WIDTH = 10
BLOCK_HEIGHT = 8


class Game:
    def __init__(self):
        self.hero = Hero(72, 42)
        self.font = None
        self.tm = None
        self.clock = pygame.time.Clock()

        self.block_number = 0
        self.load_map("00")

        self.map_screen_index_x = 5 * BLOCK_WIDTH
        self.map_screen_index_y = 6 * BLOCK_HEIGHT

        # script
        self.lexer = lex.lex()
        self.parser = yacc.yacc()
        self.parser.parse(variable_declarations)

    def load_map(self, map_number_hex):
        map_number_dec = "{:02d}".format(int(map_number_hex, 16))
        self.tm = pytmx.load_pygame(
            f"en/mapas/mapa_{map_number_dec}_{map_number_hex}.tmx"
        )
        self.event_layer = self.tm.get_layer_by_name("Object Layer eventos")
        self.tile_layer = self.tm.get_layer_by_name("Tile Layer 1")

    def display(self, surface_screen, surface_window):
        surface_screen.fill(((255, 255, 255)))

        # map
        for (
            x,
            y,
            gid,
        ) in self.tile_layer:
            if (
                x > self.map_screen_index_x - 1
                and x <= self.map_screen_index_x + BLOCK_WIDTH - 1
                and y > self.map_screen_index_y - 1
                and y <= self.map_screen_index_y + BLOCK_HEIGHT - 1
            ):
                tile = self.tm.get_tile_image_by_gid(gid)
                surface_screen.blit(
                    tile,
                    (
                        (x - self.map_screen_index_x) * self.tm.tilewidth,
                        (y - self.map_screen_index_y) * self.tm.tileheight,
                    ),
                )

        # hero
        self.hero.draw(surface_screen)

        # HUD
        text_surface = self.font.render(
            f" HP    {self.hero.hp} MP    {self.hero.mp} G    {self.hero.gold}",
            False,
            (0, 0, 0),
        )
        surface_screen.blit(text_surface, (0, 130))

        # update display
        scaled_win = pygame.transform.scale(surface_screen, surface_window.get_size())
        surface_window.blit(scaled_win, (0, 0))
        pygame.display.update()

        self.clock.tick(30)

    def update(self):
        # update hero location
        if self.hero.is_moving:
            if self.hero.direction == Direction.UP:
                self.hero.y -= 1
            if self.hero.direction == Direction.RIGHT:
                self.hero.x += 1
            if self.hero.direction == Direction.DOWN:
                self.hero.y += 1
            if self.hero.direction == Direction.LEFT:
                self.hero.x -= 1

        ## Logic
        # check boundaries
        if self.hero.x + self.hero.SIZE > self.tm.tilewidth * BLOCK_WIDTH:
            self.hero.x = 0
            self.map_screen_index_x += BLOCK_WIDTH
        elif self.hero.x < 0:
            self.hero.x = 144
            self.map_screen_index_x -= BLOCK_WIDTH
        elif self.hero.y + self.hero.SIZE > BLOCK_HEIGHT * self.tm.tileheight:
            self.hero.y = 0
            self.map_screen_index_y += BLOCK_HEIGHT
        elif self.hero.y < 0:
            self.hero.y = 112
            self.map_screen_index_y -= BLOCK_HEIGHT

        self.hero.update()

        # check tile events
        hero_bounding_box_map = self.hero.bounding_box.copy()
        hero_bounding_box_map.x += self.map_screen_index_x * self.tm.tilewidth
        hero_bounding_box_map.y += self.map_screen_index_y * self.tm.tileheight
        for game_event in self.event_layer:
            if hero_bounding_box_map.colliderect(
                (
                    game_event.x,
                    game_event.y,
                    self.tm.tilewidth,
                    self.tm.tileheight,
                )
            ):
                nro_script = game_event.properties["nroScript"]
                print(nro_script)
                self.parser.parse(f"CALL ${nro_script}")

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                instructions = input("> ")
                if debug_tokens:
                    self.lexer.input(instructions)
                    print_tokens(self.lexer)
                self.parser.parse(instructions)

            if event.key == pygame.K_LEFT:
                self.hero.is_moving = True
                self.hero.direction = Direction.LEFT
                self.hero.frame_index = 5
                self.hero.flip = False
            if event.key == pygame.K_RIGHT:
                self.hero.is_moving = True
                self.hero.direction = Direction.RIGHT
                self.hero.frame_index = 5
                self.hero.flip = True
            if event.key == pygame.K_UP:
                self.hero.is_moving = True
                self.hero.direction = Direction.UP
                self.hero.frame_index = 3
                self.hero.flip = False
            if event.key == pygame.K_DOWN:
                self.hero.is_moving = True
                self.hero.direction = Direction.DOWN
                self.hero.frame_index = 1
                self.hero.flip = False

            if event.mod & pygame.KMOD_LSHIFT:
                if event.key == pygame.K_UP:
                    if self.map_screen_index_y > 0:
                        self.map_screen_index_y -= BLOCK_HEIGHT
                elif event.key == pygame.K_DOWN:
                    self.map_screen_index_y += BLOCK_HEIGHT
                elif event.key == pygame.K_LEFT:
                    if self.map_screen_index_x > 0:
                        self.map_screen_index_x -= BLOCK_WIDTH
                elif event.key == pygame.K_RIGHT:
                    self.map_screen_index_x += BLOCK_WIDTH
                    if (
                        self.map_screen_index_x
                        >= int(self.tm.properties["sizeX"], 16) * BLOCK_WIDTH
                    ):
                        self.map_screen_index_x = 0
        elif event.type == pygame.KEYUP:
            if event.key in [
                pygame.K_LEFT,
                pygame.K_RIGHT,
                pygame.K_UP,
                pygame.K_DOWN,
            ]:
                self.hero.is_moving = False

    ## CALLBACKS ##
    def MUSIC(self, id):
        print(f"Play music {id}")

    def TELEPORT(self, MM, BB, XX, YY):
        print(f"Teleport to {MM} {BB} {XX} {YY}")
        self.hero.x = int(XX, 16) * 8
        self.hero.y = int(YY, 16) * 8
        self.block_number = int(BB, 16)
        self.load_map(MM)

        size = int(self.tm.properties["sizeX"], 16)
        self.map_screen_index_y = (self.block_number % size) * BLOCK_HEIGHT
        self.map_screen_index_x = (self.block_number // size) * BLOCK_WIDTH

    def SCRIPT_ENTRAR_BLOQUE(self):
        bn_half = self.block_number // 2
        index = bn_half  # TODO index row ordered

        print(self.block_number, bn_half, index)

        if (self.block_number // 2) % 2 == 0:
            print("A")
            layer = self.tm.get_layer_by_name('Object Layer bloquesA') 
        else:
            print("B")
            layer = self.tm.get_layer_by_name('Object Layer bloquesB')

        print(layer[index].properties)
