import pygame
import random

pygame.font.init()

# GLOBALS VARS
# Leikglugginn
s_width = 1000
s_height = 800


# tetris window 2x

play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 30 height per block

block_size = 30

top_left_x_p1 = 30
top_left_x_p2 = 350


top_left_x = (s_width - play_width) // 2
# top_left_x = 150
top_left_y = s_height - play_height


# SHAPE FORMATS

S = [['.....',
      '.....',
      '..00.',
      '.00..',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]
# index 0 - 6 represent shape


class Piece(object):  # *
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_pos={}):  # *
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_pos:
                c = locked_pos[(j,i)]
                grid[i][j] = c
    return grid


def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)

    return positions


def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]

    formatted = convert_shape_format(shape)

    for pos in formatted:
        if pos not in accepted_pos:
            if pos[1] > -1:
                return False
    return True


def check_lost(positions1, positions2):
    flag1 = 10
    flag2 = 20
    neutral = 0
    for pos1 in positions1:
        x, y = pos1
        if y < 1:
            return True, flag1
    for pos2 in positions2:
        x, y = pos2
        if y < 1:
            return True, flag2

    return False, neutral


def get_shape():
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)

    surface.blit(label, (top_left_x + play_width /2 - (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))


def draw_grid(surface, grid1, grid2):
    # sx = 150
    sx1 = top_left_x_p1
    sx2 = top_left_x_p2
    sy = top_left_y

    for i in range(len(grid1)):
        pygame.draw.line(surface, (128,128,128), (sx1, sy + i*block_size), (sx1+play_width, sy+ i*block_size))
        for j in range(len(grid1[i])):
            pygame.draw.line(surface, (128, 128, 128), (sx1 + j*block_size, sy),(sx1 + j*block_size, sy + play_height))
    
    for k in range(len(grid2)):
        pygame.draw.line(surface, (128,128,128), (sx2, sy + k*block_size), (sx2+play_width, sy+ k*block_size))
        for m in range(len(grid2[k])):
            pygame.draw.line(surface, (128, 128, 128), (sx2 + m*block_size, sy),(sx2 + m*block_size, sy + play_height))


def clear_rows(grid, locked):

    inc = 0
    for i in range(len(grid)-1, -1, -1):
        row = grid[i]
        if (0,0,0) not in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[(j,i)]
                except:
                    continue

    if inc > 0:
        for key in sorted(list(locked), key=lambda x: x[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + inc)
                locked[newKey] = locked.pop(key)

    return inc


def draw_next_shape(next_shape1, next_shape2, surface):
    font = pygame.font.SysFont('comicsans', 30)
    label1 = font.render('Next Shape P1', 1, (255,255,255))
    label2 = font.render('Next Shape P2', 1, (255,255,255))
    format1 = next_shape1.shape[next_shape1.rotation % len(next_shape1.shape)]
    format2 = next_shape2.shape[next_shape2.rotation % len(next_shape2.shape)]

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 280
    sx2 = top_left_x + play_width + 50
    sy2 = top_left_y + play_height/2 - 100

    for i, line in enumerate(format1):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, next_shape1.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)
    
    
    for k, line in enumerate(format2):
        row = list(line)
        for m, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, next_shape2.color, (sx2 + m*block_size, sy2 + k*block_size, block_size, block_size), 0)

    surface.blit(label1, (sx + 10, sy - 30))
    surface.blit(label2, (sx2 + 10, sy2 - 30))


def update_score(nscore1, nscore2):
    score = max_score()

    with open('scores.txt', 'a') as f:
        if nscore1 > int(score):
            f.write("P1 " + str(nscore1) + "\n")
        if nscore2 > int(score):
            f.write("P2 " + str(nscore2)+ "\n")


def max_score():
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[-1].split()[-1]

    return score


def draw_window(surface, grid1, grid2, score1=0, score2=0, last_score = 0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    label = font.render('Tetris 2 Player', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    
    # Player 1
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Player 1 ', 1, (255,255,255))

    sx = top_left_x_p1 +20
    sy = 150
    # sx = top_left_x_p1 + play_width 
    # sy = top_left_y + play_height

    surface.blit(label, (sx, sy))
    # Player 2
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Player 2 ', 1, (255,255,255))

    sx = top_left_x_p2 +20
    sy = 150
    # sx = top_left_x_p1 + play_width 
    # sy = top_left_y + play_height

    surface.blit(label, (sx, sy))

    # current score Player 1
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score P1: ' + str(score1), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 20, sy + 200))
    # current score Player 2
    font = pygame.font.SysFont('comicsans', 30)
    label = font.render('Score P2: ' + str(score2), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 20, sy + 240))
    # last score
    label = font.render('High Score: ' + last_score, 1, (255,255,255))

    sx = top_left_x + play_width
    sy = top_left_y + play_height/2 -100

    surface.blit(label, (sx + 70, sy + 320))

    # moving the block 
    # player 1
    for i in range(len(grid1)):
        for j in range(len(grid1[i])):
            pygame.draw.rect(surface, grid1[i][j], (top_left_x_p1 + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)
    # player 2
    for k in range(len(grid2)):
        for m in range(len(grid2[k])):
            pygame.draw.rect(surface, grid2[k][m], (top_left_x_p2 + m*block_size, top_left_y + k*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x_p1, top_left_y, play_width, play_height), 5)
    pygame.draw.rect(surface, (255, 0, 0), (top_left_x_p2, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid1, grid2)


def main(win):
    last_score = max_score()
    locked_positions1 = {}
    locked_positions2 = {}
    grid1 = create_grid(locked_positions1)
    grid2 = create_grid(locked_positions2)

    change_piece1 = False
    change_piece2 = False
    run = True
    current_piece1 = get_shape()
    current_piece2 = get_shape()
    next_piece1 = get_shape()
    next_piece2 = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.27
    level_time = 0
    score1 = 0
    score2 = 0

    while run:
        grid1 = create_grid(locked_positions1)
        grid2 = create_grid(locked_positions2)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()

        if level_time/1000 > 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005

        # PLAYER 1
        if fall_time/1000 > fall_speed:
            fall_time = 0
            current_piece1.y += 1
            current_piece2.y += 1
            if not(valid_space(current_piece1, grid1)) and current_piece1.y > 0:
                current_piece1.y -= 1
                change_piece1 = True
            if not(valid_space(current_piece2, grid2)) and current_piece2.y > 0:
                current_piece2.y -= 1
                change_piece2 = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()

            if event.type == pygame.KEYDOWN:
                # PLAYER 1
                if event.key == pygame.K_LEFT:
                    current_piece1.x -= 1
                    if not(valid_space(current_piece1, grid1)):
                        current_piece1.x += 1
                if event.key == pygame.K_RIGHT:
                    current_piece1.x += 1
                    if not(valid_space(current_piece1, grid1)):
                        current_piece1.x -= 1
                if event.key == pygame.K_DOWN:
                    current_piece1.y += 1
                    if not(valid_space(current_piece1, grid1)):
                        current_piece1.y -= 1
                if event.key == pygame.K_UP:
                    current_piece1.rotation += 1
                    if not(valid_space(current_piece1, grid1)):
                        current_piece1.rotation -= 1
                
                # PLAYER 2
                if event.key == pygame.K_a:
                    current_piece2.x -= 1
                    if not(valid_space(current_piece2, grid2)):
                        current_piece2.x += 1
                if event.key == pygame.K_d:
                    current_piece2.x += 1
                    if not(valid_space(current_piece2, grid2)):
                        current_piece2.x -= 1
                if event.key == pygame.K_s:
                    current_piece2.y += 1
                    if not(valid_space(current_piece2, grid2)):
                        current_piece2.y -= 1
                if event.key == pygame.K_w:
                    current_piece2.rotation += 1
                    if not(valid_space(current_piece2, grid2)):
                        current_piece2.rotation -= 1

        shape_pos1 = convert_shape_format(current_piece1)
        shape_pos2 = convert_shape_format(current_piece2)

        for i in range(len(shape_pos1)):
            x, y = shape_pos1[i]
            if y > -1:
                grid1[y][x] = current_piece1.color

        for j in range(len(shape_pos2)):
            x2, y2 = shape_pos2[j]
            if y2 > -1:
                grid2[y2][x2] = current_piece2.color

        if change_piece1:
            for pos1 in shape_pos1:
                p = (pos1[0], pos1[1])
                locked_positions1[p] = current_piece1.color
            current_piece1 = next_piece1
            next_piece1 = get_shape()
            change_piece1 = False
            score1 += clear_rows(grid1, locked_positions1) * 10
        # Player 2
        if change_piece2:
            for pos2 in shape_pos2:
                p = (pos2[0], pos2[1])
                locked_positions2[p] = current_piece2.color
            current_piece2 = next_piece2
            next_piece2 = get_shape()
            change_piece2 = False
            score2 += clear_rows(grid2, locked_positions2) * 10

        draw_window(win, grid1, grid2, score1, score2, last_score)
        draw_next_shape(next_piece1, next_piece2, win)
        pygame.display.update()

        lost, flag = check_lost(locked_positions1, locked_positions2)

        if lost:#if returns true
            if flag == 10:
                draw_text_middle(win, "PLAYER 1 LOST!", 80, (255,255,255))
            if flag == 20:
                draw_text_middle(win, "PLAYER 2 LOST!", 80, (255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score1, score2)


def main_menu(win):  # *
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win, 'Press Any Key To Play', 60, (255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                main(win)

    pygame.display.quit()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('TETRIS 2 PLAYER')
main_menu(win)