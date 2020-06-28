import pygame
import math
import sys
import map  # CUSTOM MAP

# COLOUR CONSTS
black = (0, 0, 0)
white = (255, 255, 255)
grey = (40, 40, 40)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
orange = (255, 165, 0)

# GLOBAL VARIABLES
screen_width = 800
screen_height = 800
fps = 60
title = 'GRID'
title_size = 16
cols = screen_width // title_size
rows = screen_height // title_size

# INIT
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('')
clock = pygame.time.Clock()
screen.fill(white)


class Node:
    def __init__(self, i, j):
        self.mode = 'default'
        self.x = j
        self.y = i

        self.g_cost = 0
        self.h_cost = 0
        self.parent = None

        self.strict = False  # START AND END NODES COLOUR DOESN'T CHANGE

    @property
    def f_cost(self):
        return self.h_cost + self.g_cost

    def show(self):
        if self.strict:
            pygame.draw.rect(screen, blue, (self.x * title_size, self.y * title_size, title_size, title_size), 0)
            pygame.draw.rect(screen, grey, (self.x * title_size, self.y * title_size, title_size, title_size), 1)
        elif self.mode == 'default':
            pygame.draw.rect(screen, white, (self.x * title_size, self.y * title_size, title_size, title_size), 0)
            pygame.draw.rect(screen, black, (self.x * title_size, self.y * title_size, title_size, title_size), 1)
        elif self.mode == 'obstacle':
            pygame.draw.rect(screen, grey, (self.x * title_size, self.y * title_size, title_size, title_size), 0)
        elif self.mode == 'open':
            pygame.draw.rect(screen, green, (self.x * title_size, self.y * title_size, title_size, title_size), 0)
            pygame.draw.rect(screen, grey, (self.x * title_size, self.y * title_size, title_size, title_size), 1)

        elif self.mode == 'closed':
            pygame.draw.rect(screen, red, (self.x * title_size, self.y * title_size, title_size, title_size), 0)
            pygame.draw.rect(screen, grey, (self.x * title_size, self.y * title_size, title_size, title_size), 1)
        elif self.mode == 'start' or self.mode == 'end' or self.mode == 'path':
            pygame.draw.rect(screen, blue, (self.x * title_size, self.y * title_size, title_size, title_size), 0)
            pygame.draw.rect(screen, grey, (self.x * title_size, self.y * title_size, title_size, title_size), 1)


# CREATE 2D ARRAY [ROW, COL]
grid = [[0 for i in range(rows)] for j in range(cols)]

# FILL GRID WITH EMPTY TILE
for i in range(rows):
    for j in range(cols):
        grid[i][j] = Node(i, j)

# SET SCREEN BORDERS AS OBSTACLES
