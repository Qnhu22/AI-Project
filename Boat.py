import pygame
from Config import cell_width, cell_height
from AI import solve_maze_bfs, solve_maze_astar, simulated_annealing_path, solve_maze_ucs, stochastic_hill_climbing, beam_search, solve_maze_qlearning

def path_to_directions(path):
    """Chuyển đổi đường đi từ tọa độ tuyệt đối sang hướng di chuyển tương đối."""
    directions = []
    for i in range(1, len(path)):
        dx = path[i][0] - path[i - 1][0]
        dy = path[i][1] - path[i - 1][1]
        directions.append((dx, dy))
    return directions

class Boat:
    def __init__(self, x, y):
        self.row = x
        self.col = y
        self.image = pygame.image.load('Image/monster.png')
        self.image = pygame.transform.scale(self.image, (cell_width, cell_height))
        self.path = None
        self.path_index = 0
        self.algorithm_selected = None
        self.last_move_time = 0
        self.move_delay = 300
        self.step_count = 0
        self.start_position = (x, y)
        self.end_position = None
        self.monster_path = [(self.row, self.col)]
        self.last_target = None

    def update_path(self, maze, target, algorithm):
        # Chỉ cập nhật nếu thuật toán thay đổi, không có đường đi, hoặc mục tiêu thay đổi
        if self.algorithm_selected != algorithm or not self.path or target != self.last_target:
            print(f"Running {algorithm} for boat at ({self.row}, {self.col}) to target {target}")

            if algorithm == "BFS":
                self.path = solve_maze_bfs(maze, (self.row, self.col), target) or []
            elif algorithm == "A*":
                self.path = solve_maze_astar(maze, (self.row, self.col), target) or []
            elif algorithm == "Simulated Annealing":
                self.path = simulated_annealing_path(
                    maze, (self.row, self.col), target, max_iterations=1000, initial_temp=100, cooling_rate=0.99
                ) or []
            elif algorithm == "Stochastic Hill Climbing":
                self.path = stochastic_hill_climbing(maze, (self.row, self.col), target) or []
            elif algorithm == "UCS":
                self.path = solve_maze_ucs(maze, (self.row, self.col), target) or []
            elif algorithm == "Beam Search":
                self.path = beam_search(maze, (self.row, self.col), target) or []
            elif algorithm == "Q-Learning":
                self.path = solve_maze_qlearning(
                    maze, (self.row, self.col), target,
                    episodes=200, alpha=0.1, gamma=0.9, epsilon=0.1
                ) or []
            else:
                self.path = []
                print(f"No path found with {algorithm}. Boat stays at {self.end_position}.")

            self.algorithm_selected = algorithm
            self.path_index = 0
            self.last_target = target

            if not self.path:
                print(f"No path found with {algorithm}. Boat stays at ({self.row}, {self.col}).")

    def move(self, maze):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.move_delay:
            if not self.path:
                if not hasattr(self, 'path_warning_printed'):
                    print("Boat has no path.")
                    self.path_warning_printed = True
                return
            self.path_warning_printed = False

            if self.path_index < len(self.path):
                direction = self.path[self.path_index]
                next_row = self.row + direction[0]
                next_col = self.col + direction[1]
                if (0 <= next_row < len(maze) and 0 <= next_col < len(maze[0]) and
                    maze[next_row][next_col] == 0):
                    self.row = next_row
                    self.col = next_col
                    self.path_index += 1
                    self.step_count += 1
                    self.monster_path.append((self.row, self.col))
                    print(f"Boat moves to ({self.row}, {self.col}), Steps: {self.step_count}")
                else:
                    print("Boat cannot move to the next cell.")
            else:
                self.end_position = (self.row, self.col)
                print(f"Boat reached end of path at {self.end_position}.")
            self.last_move_time = current_time

    def draw(self, surface):
        x = self.col * cell_width
        y = self.row * cell_height
        surface.blit(self.image, (x, y))

    def get_monster_path(self):
        return self.monster_path