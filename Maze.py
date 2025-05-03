import pygame
from Config import cell_width, cell_height, path_image, maze_matrix
from Colors import Colors

class Maze:
    def __init__(self, matrix):
        self.matrix = matrix
        self.rows = len(matrix)
        self.cols = len(matrix[0])

    def draw(self, surface):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.matrix[row][col] == 1:
                    x, y = col * cell_width, row * cell_height
                    surface.blit(path_image, (x, y))
                    self.draw_border(surface, row, col)

        self.draw_outer_border(surface)

    def draw_border(self, surface, row, col):
        x, y = col * cell_width, row * cell_height
        outer = Colors.PURPLE_2
        inner = Colors.LIGHT_YELLOW

        directions = [
            ((x, y), (x + cell_width, y), row > 0 and self.matrix[row - 1][col] == 0),              # top
            ((x, y + cell_height), (x + cell_width, y + cell_height), row < self.rows - 1 and self.matrix[row + 1][col] == 0),  # bottom
            ((x, y), (x, y + cell_height), col > 0 and self.matrix[row][col - 1] == 0),             # left
            ((x + cell_width, y), (x + cell_width, y + cell_height), col < self.cols - 1 and self.matrix[row][col + 1] == 0)   # right
        ]

        for start, end, show in directions:
            if show:
                pygame.draw.line(surface, outer, (start[0] - 1, start[1] - 1), (end[0] - 1, end[1] - 1), 3)
                pygame.draw.line(surface, inner, start, end, 2)

    def draw_outer_border(self, surface):
        maze_width = self.cols * cell_width
        maze_height = self.rows * cell_height
        radius = 10
        layers = [(Colors.PURPLE_2, 6), (Colors.LIGHT_YELLOW, 3)]

        for i, (color, thickness) in enumerate(layers):
            offset = i
            rect = pygame.Rect(offset, offset, maze_width - offset * 2, maze_height - offset * 2)
            pygame.draw.rect(surface, color, rect, thickness, border_radius=radius)