def MUSIC(game, id):
    print(f"Play music {id}")

def TELEPORT(game, MM, BB, XX, YY):
    print(f"Teleport to {MM} {BB} {XX} {YY}")
    game.hero.x = int(XX, 16) * 8
    game.hero.y = int(YY, 16) * 8
    block_number = int(YY, BB)
    game.map_screen_index_x = 0 # TODO from BB
    game.map_screen_index_y = 0
    game.load_map(MM)
