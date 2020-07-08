import pygame
import sys
import pygame_simulation.constants as constants


def get_tile_color(tile_contents):
    tile_color = (0, 0, 0)
    if tile_contents == 'w':
        tile_color = constants.GREEN
    elif tile_contents == '-':
        tile_color = constants.GREY
    return tile_color


def draw_grid(surface_):
    for i in range(constants.NUMBER_OF_BLOCKS_WIDE):
        new_height = round(i * constants.BLOCK_HEIGHT)
        new_width = round(i * constants.BLOCK_WIDTH)
        pygame.draw.line(surface_, constants.BLACK, (0, new_height), (constants.SCREEN_WIDTH, new_height), 2)
        pygame.draw.line(surface_, constants.BLACK, (new_width, 0), (new_width, constants.SCREEN_HEIGHT), 2)


def draw_map(surface_, map_tiles):
    for j, tile in enumerate(map_tiles):
        for i, tile_contents in enumerate(tile):
            # print(f'{i},{j}: {tile_contents}')
            myrect = pygame.Rect(i * constants.BLOCK_WIDTH, j * constants.BLOCK_HEIGHT, constants.BLOCK_WIDTH,
                                 constants.BLOCK_HEIGHT)
            pygame.draw.rect(surface_, get_tile_color(tile_contents), myrect)


def draw_agent(surface_, map_tiles, x, y):
    surface_.blit(agentImg, (x, y))


def game_loop(surface_, world_map_):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        draw_map(surface_, world_map_)
        draw_grid(surface_)
        draw_agent(surface_, world_map_, 55, 205)
        pygame.display.update()


def initialize_game():
    pygame.init()
    surface_ = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))
    pygame.display.set_caption(constants.TITLE)
    surface_.fill(constants.GREY)
    return surface_


def read_map(mapfile):
    with open(mapfile, 'r') as f:
        world_map_ = f.readlines()
    world_map_ = [line.strip() for line in world_map_]
    return world_map_


if __name__ == '__main__':
    # Agent
    agentImg = pygame.image.load('agent_icon.png')
    agentImg = pygame.transform.scale(agentImg, (int(0.8 * constants.BLOCK_WIDTH), int(0.8 * constants.BLOCK_HEIGHT)))
    agentX = 120
    agentY = 120

    world_map = read_map(constants.MAPFILE)
    surface = initialize_game()
    game_loop(surface, world_map)
