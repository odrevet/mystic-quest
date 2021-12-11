import pygame
from game import Game
import interpreter

def main():
    pygame.init()
    pygame.font.init()
    font = pygame.font.SysFont("", 12)

    resolution_screen = (160, 144)
    resolution_window = (640, 480)
    surface_window = pygame.display.set_mode(resolution_window)
    surface_screen = pygame.Surface(resolution_screen)

    pygame.display.set_caption("Mystic Quest")
    
    game = Game()
    interpreter.game = game
    game.font = font

    done = False
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    done = True

            game.events(event)
        game.update()
        game.display(surface_screen, surface_window)

if __name__ == "__main__":
    main()
    pygame.quit()
