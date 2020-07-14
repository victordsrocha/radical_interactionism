import sys

import pygame

import pygame_simulation.constants as constants
from src.agent import Agent


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


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def draw_agent(surface_, action):
    global agentImg
    global inside_t
    label, a_x, a_y, a_o = action
    a_x = a_x * 50 + 5
    a_y = a_y * 50 + 5
    global r_x, r_y
    rot = None
    if label == 'vt':
        if a_o == 0:
            rot = 0+90
        if a_o == 1:
            rot = -90+90
        if a_o == 2:
            rot = -180+90
        if a_o == 3:
            rot = -270+90
        rot += -18 * (inside_t + 1)
        # surface_.blit(rot_center(agentImg, -rot), (a_x, a_y))
    elif label == '^t':
        if a_o == 0:
            rot = 0-90
        if a_o == 1:
            rot = -90-90
        if a_o == 2:
            rot = -180-90
        if a_o == 3:
            rot = -270-90
        rot += 18 * (inside_t + 1)
        # surface_.blit(rot_center(agentImg, rot), (a_x, a_y))
    else:
        if a_o == 0:
            rot = 0
        if a_o == 1:
            rot = -90
        if a_o == 2:
            rot = -180
        if a_o == 3:
            rot = -270
    # if label == '>f' or label == '>t':
    # surface_.blit(agentImg, (a_x, a_y))

    if a_o == 0:
        if label == '>t':
            r_y -= 10
        elif label == '>f':
            if inside_t == 0 or inside_t == 1:
                r_y -= 10
            elif inside_t == 2:
                r_y -= 5
            elif inside_t == 3 or inside_t == 4:
                r_y += 12.5
            surface_.blit(bump_img, (a_x, a_y - 50))
        elif label == '-t':
            surface_.blit(touch_true_img, (a_x, a_y - 50))
        elif label == '-f':
            surface_.blit(touch_false_img, (a_x, a_y - 50))
        elif label == '\\t':
            surface_.blit(touch_true_img, (a_x + 50, a_y))
        elif label == '\\f':
            surface_.blit(touch_false_img, (a_x + 50, a_y))
        elif label == '\t':
            surface_.blit(touch_true_img, (a_x - 50, a_y))
        elif label == '\f':
            surface_.blit(touch_false_img, (a_x - 50, a_y))
    elif a_o == 1:
        if label == '>t':
            r_x += 10
        elif label == '>f':
            if inside_t == 0 or inside_t == 1:
                r_x += 10
            elif inside_t == 2:
                r_x += 5
            elif inside_t == 3 or inside_t == 4:
                r_x -= 12.5
            surface_.blit(bump_img, (a_x + 50, a_y))
        elif label == '-t':
            surface_.blit(touch_true_img, (a_x + 50, a_y))
        elif label == '-f':
            surface_.blit(touch_false_img, (a_x + 50, a_y))
        elif label == '\\t':
            surface_.blit(touch_true_img, (a_x, a_y + 50))
        elif label == '\\f':
            surface_.blit(touch_false_img, (a_x, a_y + 50))
        elif label == '\t':
            surface_.blit(touch_true_img, (a_x, a_y - 50))
        elif label == '\f':
            surface_.blit(touch_false_img, (a_x, a_y - 50))
    if a_o == 2:
        if label == '>t':
            r_y += 10
        elif label == '>f':
            if inside_t == 0 or inside_t == 1:
                r_y += 10
            elif inside_t == 2:
                r_y += 5
            elif inside_t == 3 or inside_t == 4:
                r_y -= 12.5
            surface_.blit(bump_img, (a_x, a_y + 50))
        elif label == '-t':
            surface_.blit(touch_true_img, (a_x, a_y + 50))
        elif label == '-f':
            surface_.blit(touch_false_img, (a_x, a_y + 50))
        elif label == '\\t':
            surface_.blit(touch_true_img, (a_x - 50, a_y))
        elif label == '\\f':
            surface_.blit(touch_false_img, (a_x - 50, a_y))
        elif label == '\t':
            surface_.blit(touch_true_img, (a_x + 50, a_y))
        elif label == '\f':
            surface_.blit(touch_false_img, (a_x + 50, a_y))
    elif a_o == 3:
        if label == '>t':
            r_x -= 10
        elif label == '>f':
            if inside_t == 0 or inside_t == 1:
                r_x -= 10
            elif inside_t == 2:
                r_x -= 5
            elif inside_t == 3 or inside_t == 4:
                r_x += 12.5
            surface_.blit(bump_img, (a_x - 50, a_y))
        elif label == '-t':
            surface_.blit(touch_true_img, (a_x - 50, a_y))
        elif label == '-f':
            surface_.blit(touch_false_img, (a_x - 50, a_y))
        elif label == '\\t':
            surface_.blit(touch_true_img, (a_x, a_y - 50))
        elif label == '\\f':
            surface_.blit(touch_false_img, (a_x, a_y - 50))
        elif label == '\t':
            surface_.blit(touch_true_img, (a_x, a_y + 50))
        elif label == '\f':
            surface_.blit(touch_false_img, (a_x, a_y + 50))

    inside_t += 1
    surface_.blit(rot_center(agentImg, rot), (r_x, r_y))


clock = pygame.time.Clock()


def game_loop(surface_, world_map_, agent):
    current = 0
    t = 0
    a = None
    global inside_t

    while True:

        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if t == 0:
            try:
                a = agent.step_actions_list[current]
            except IndexError:
                current = 0
                agent.step()
                a = agent.step_actions_list[current]
            current += 1

        draw_map(surface_, world_map_)
        draw_grid(surface_)
        draw_agent(surface_, a)
        # pygame.time.wait(100)  # wait 100ms

        t = t + 1

        if t == 5:
            t = 0
            inside_t = 0

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
    surface = initialize_game()

    # Agent
    agentInst = Agent()
    agentImg = pygame.image.load('agent_icon.png').convert_alpha()
    agentImg = pygame.transform.scale(agentImg, (int(0.8 * constants.BLOCK_WIDTH), int(0.8 * constants.BLOCK_HEIGHT)))
    agentX = 120
    agentY = 120
    r_x = 1 * 50 + 5
    r_y = 4 * 50 + 5
    r_o = 0
    inside_t = 0

    # touch True
    touch_true_img = pygame.image.load('blue.png').convert_alpha()
    # touch False
    touch_false_img = pygame.image.load('yellow.png').convert_alpha()
    # bump
    bump_img = pygame.image.load('bump.png').convert_alpha()

    world_map = read_map(constants.MAPFILE)

    game_loop(surface, world_map, agentInst)
