import pygame 
from Config import cell_width, cell_height
from AI import solve_maze_bfs, solve_maze_astar, simulated_annealing_path, solve_maze_ucs, stochastic_hill_climbing, beam_search

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
        self.move_delay = 150
        self.step_count = 0
        self.start_position = (x, y)  # Lưu vị trí bắt đầu
        self.end_position = None      # Lưu vị trí cuối cùng

    def update_path(self, maze, target, algorithm):
    # Chỉ in nếu là thuật toán mới hoặc chưa có path
        if self.algorithm_selected != algorithm or not self.path:
            print(f"Running {algorithm} for boat at ({self.row}, {self.col})")

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
        else:
            self.path = []
            print(f"No path found using {algorithm}. Boat remains at {self.end_position}.")

        self.algorithm_selected = algorithm  # ✅ Ghi nhớ thuật toán đã chọn
        self.path_index = 0

        if not self.path:
            print(f"No path found using {algorithm}. Boat remains at ({self.row}, {self.col}).")


    def move(self, maze):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time >= self.move_delay:
            if not self.path:
                print("Boat has no path.")
                return  # Không có đường đi
            if self.path_index < len(self.path):
                direction = self.path[self.path_index]
                next_row = self.row + direction[0]
                next_col = self.col + direction[1]
                if 0 <= next_row < len(maze) and 0 <= next_col < len(maze[0]) and maze[next_row][next_col] == 0:
                    self.row = next_row
                    self.col = next_col
                    self.path_index += 1
                    self.step_count += 1  # Cập nhật số bước
                    print(f"Boat moved to ({self.row}, {self.col}), Step Count: {self.step_count}")
                else:
                    print("Boat cannot move to the next cell.")
            else:
                # Cập nhật vị trí cuối cùng
                self.end_position = (self.row, self.col)
                print(f"Boat reached the end of its path at {self.end_position}.")
            self.last_move_time = current_time

    def draw(self, surface):
        x = self.col * cell_width
        y = self.row * cell_height
        surface.blit(self.image, (x, y))