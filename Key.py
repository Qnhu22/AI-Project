import pygame
import random
from Config import maze_size, cell_width, cell_height, key_image

class Key:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.image = pygame.transform.scale(key_image, (cell_width, cell_height))
        self.collected = False

    def draw(self, surface):
        if not self.collected:
            x = self.col * cell_width
            y = self.row * cell_height
            surface.blit(self.image, (x, y))

def generate_keys(maze_matrix, num_keys):
    keys = []
    rows = len(maze_matrix)
    cols = len(maze_matrix[0])

    while len(keys) < num_keys:
        row = random.randint(0, rows - 1)
        col = random.randint(0, cols - 1)
        
        # Đặt key ở ô trống, không phải start (0,0) và goal
        if maze_matrix[row][col] == 0 and (row, col) != (0, 0) and (row, col) != (maze_size - 1, maze_size - 1):
            keys.append(Key(row, col))
    
    return keys

def check_collect(player_row, player_col, keys):
    for key in keys:
        if not key.collected and key.row == player_row and key.col == player_col:
            key.collected = True
            return True  # Có key được nhặt
    return False  # Không có key nào nhặt
