import pygame
from collections import deque
import heapq
import random
import time
import math
import numpy as np

directions = [
    (-1, 0),  # lên
    (1, 0),   # xuống
    (0, -1),  # trái
    (0, 1),   # phải

 ]
# Hàm thuật toán bfs
def solve_maze_bfs(maze, start, goal):

    rows = len(maze)      #xác định số hàng
    cols = len(maze[0])   #xác định cột
    
    queue = deque([(start)]) #tạo chỗ xếp hàng
    visited = {start} #đánh dấu ô 
    
    # Dictionary lưu đường đi
    came_from = {} 
    
    while queue: #
        current = queue.popleft() #lấy phần tử đầu tiên
        
        if current == goal:
            # Tái tạo đường đi
            path = []
            while current in came_from:
                prev = came_from[current]
                path.append((current[0] - prev[0], current[1] - prev[1]))
                current = prev
            path.reverse()
            return path
            
        # Kiểm tra tất cả các hướng có thể đi
        for dx, dy in directions:
            next_row = current[0] + dx
            next_col = current[1] + dy
            neighbor = (next_row, next_col) 
            
            # Kiểm tra điều kiện hợp lệ
            if (0 <= next_row < rows and 
                0 <= next_col < cols and 
                maze[next_row][next_col] == 0 and  # 0 là đường đi
                neighbor not in visited):
                
                queue.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current
    
    return None  # Không tìm thấy đường đi

# Hàm thuật toán A*
def heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])    #f(n)=g(n)+h(n)
def solve_maze_astar(maze, start, goal):

    rows = len(maze)
    cols = len(maze[0])
    
    # Tập đóng (closed_set): Lưu các điểm đã xử lý.
    closed_set = set()

    # Tập mở (open_set): Hàng đợi ưu tiên, lưu các điểm cần xử lý tiếp theo.
    # Sử dụng heapq để đảm bảo các phần tử có giá trị f nhỏ nhất được xử lý trước.
    open_set = []
    heapq.heappush(open_set, (0, start))  # Thêm điểm bắt đầu với giá trị f = 0.
    
    # Dictionary lưu "cha" của mỗi điểm, phục vụ cho việc tái tạo đường đi.
    came_from = {}
    
    # g_score lưu chi phí từ điểm bắt đầu đến mỗi điểm.
    g_score = {start: 0}

    # Lặp cho đến khi không còn điểm nào trong tập mở
    while open_set:
        # Lấy điểm có giá trị f nhỏ nhất từ open_set
        current = heapq.heappop(open_set)[1]
        
        # Nếu đã đến đích, tái tạo và trả về đường đi
        if current == goal:
            path = []  # Danh sách lưu các bước di chuyển
            while current in came_from:
                prev = came_from[current]  # Lấy điểm cha của current
                path.append((current[0] - prev[0], current[1] - prev[1]))  # Lưu hướng di chuyển
                current = prev  # Quay về điểm cha
            path.reverse()  # Đảo ngược danh sách để có đường đi từ start đến goal
            return path  # Trả về danh sách các bước di chuyển
        
        # Thêm điểm hiện tại vào tập đóng
        closed_set.add(current)
        
        # Kiểm tra các điểm lân cận
        for dx, dy in directions:  # directions chứa các vector di chuyển hợp lệ (vd: [(0,1), (1,0), (0,-1), (-1,0)])
            neighbor = (current[0] + dx, current[1] + dy)  # Tính tọa độ của điểm lân cận
            
            # Kiểm tra điều kiện hợp lệ của điểm lân cận
            if (neighbor[0] < 0 or neighbor[0] >= rows or  # Nằm ngoài lưới (hàng)
                neighbor[1] < 0 or neighbor[1] >= cols or  # Nằm ngoài lưới (cột)
                maze[neighbor[0]][neighbor[1]] == 1 or     # Là tường (giá trị 1 trong maze)
                neighbor in closed_set):                  # Đã được xử lý trước đó
                continue
            
            # Tính toán chi phí tạm thời từ start đến neighbor qua current
            tentative_g_score = g_score[current] + 1
            
            # Nếu neighbor chưa được thăm hoặc tìm thấy đường đi tốt hơn
            if (neighbor not in g_score or tentative_g_score < g_score[neighbor]):
                came_from[neighbor] = current  # Cập nhật cha của neighbor
                g_score[neighbor] = tentative_g_score  # Cập nhật g_score của neighbor
                
                # Tính giá trị f = g + h (h là giá trị heuristic từ neighbor đến goal)
                f_score = tentative_g_score + heuristic(neighbor, goal)
                
                # Thêm neighbor vào tập mở
                heapq.heappush(open_set, (f_score, neighbor))
    
    # Nếu không tìm thấy đường đi
    return None



def heuristic(a, b):
    """
    Tính toán khoảng cách Manhattan giữa hai ô.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def calculate_max_depth(maze, complexity='medium'):
    """
    Tính toán độ sâu tối đa dựa trên kích thước mê cung và độ phức tạp.
    """
    size = len(maze) * len(maze[0])
    wall_density = sum(row.count(1) for row in maze) / size

    # Hệ số điều chỉnh dựa trên độ phức tạp
    factor = {
        'simple': 0.3,
        'medium': 0.5,
        'complex': 0.7
    }.get(complexity, 0.5)

    if wall_density > 0.5:  # Điều chỉnh nếu mật độ tường cao
        factor += 0.1

    return int(factor * size)



# SIMULATED ANNEALING
def schedule(t, k=20, lam=0.005, limit=1000):
    """Cooling schedule function."""
    return (k * np.exp(-lam * t) if t < limit else 0)

def simulated_annealing_path(maze, start, goal, max_iterations=1000, initial_temp=100, cooling_rate=0.99):
    """
    Simulated Annealing for the maze game. The boat tries to minimize the distance to the player.
    """
    current = start
    current_cost = heuristic(current, goal)
    temperature = initial_temp
    path = []  # Store the path the boat takes

    for t in range(max_iterations):
        if current == goal:
            print(f"Boat reached the player after {t} iterations.")
            return path

        # Get all valid neighbors
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_row, next_col = current[0] + dx, current[1] + dy
            if 0 <= next_row < len(maze) and 0 <= next_col < len(maze[0]) and maze[next_row][next_col] == 0:
                neighbors.append((next_row, next_col))

        if not neighbors:  # No valid moves
            print("Boat is stuck.")
            break

        # Choose a random neighbor
        next_position = random.choice(neighbors)
        next_cost = heuristic(next_position, goal)

        # Calculate the change in cost
        delta_cost = next_cost - current_cost

        # Determine whether to accept the move
        if delta_cost < 0 or random.uniform(0, 1) < math.exp(-delta_cost / temperature):
            current = next_position
            current_cost = next_cost
            path.append((next_position[0] - start[0], next_position[1] - start[1]))

        # Cool down the temperature
        temperature *= cooling_rate
        if temperature < 1e-3:  # If the temperature is too low, stop
            print("Temperature is too low, stopping.")
            break

    return path if current == goal else None

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])



def solve_maze_ucs(maze, start, goal):
    rows = len(maze)
    cols = len(maze[0])

    # Tập mở (open_set) sử dụng heapq để lưu các điểm với chi phí thấp nhất
    open_set = []
    heapq.heappush(open_set, (0, start))  # (chi phí, điểm)
    
    # Tập đã thăm
    visited = set()
    
    # Tạo dictionary lưu lại đường đi (came_from) để tái tạo đường đi
    came_from = {}
    
    # Lưu chi phí từ điểm start đến các điểm
    g_score = {start: 0}

    while open_set:
        # Lấy điểm có chi phí nhỏ nhất từ open_set
        current_cost, current = heapq.heappop(open_set)

        # Nếu đến đích, tái tạo đường đi
        if current == goal:
            path = []
            while current in came_from:
                prev = came_from[current]
                path.append((current[0] - prev[0], current[1] - prev[1]))
                current = prev
            path.reverse()  # Đảo ngược lại để có đường đi từ start đến goal
            return path
        
        # Kiểm tra các điểm lân cận
        for dx, dy in directions:
            next_row = current[0] + dx
            next_col = current[1] + dy
            neighbor = (next_row, next_col)
            
            # Kiểm tra điều kiện hợp lệ
            if 0 <= next_row < rows and 0 <= next_col < cols and maze[next_row][next_col] == 0:
                # Tính toán chi phí từ start đến neighbor
                tentative_g_score = current_cost + 1
                
                # Nếu chưa thăm hoặc tìm thấy đường đi tốt hơn
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    heapq.heappush(open_set, (tentative_g_score, neighbor))
    
    return None  # Không tìm thấy đường đi


def stochastic_hill_climbing(maze, start, goal, max_iterations=1000):
    current = start
    path = []
    iteration = 0

    while current != goal and iteration < max_iterations:
        neighbors = []
        
        # Tạo danh sách các vị trí lân cận hợp lệ
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            next_row, next_col = current[0] + dx, current[1] + dy
            if 0 <= next_row < len(maze) and 0 <= next_col < len(maze[0]) and maze[next_row][next_col] == 0:
                neighbors.append((next_row, next_col))

        # Nếu không có hàng xóm hợp lệ, dừng lại
        if not neighbors:
            print("Boat is stuck.")
            break

        # Chọn bước đi có chi phí thấp nhất
        next_position = min(neighbors, key=lambda x: heuristic(x, goal))

        # Nếu bước đi giúp giảm khoảng cách tới mục tiêu, tiếp tục di chuyển
        if heuristic(next_position, goal) < heuristic(current, goal):
            path.append((next_position[0] - start[0], next_position[1] - start[1]))
            current = next_position
        else:
            # Nếu không có cải tiến, dừng lại
            print(f"Stuck at {current}, no improvement found.")
            break

        iteration += 1

    return path if current == goal else None





def beam_search(maze, start, goal, beam_width=3):
    """Beam Search Algorithm"""
    # Danh sách các trạng thái đang mở
    open_list = []
    heapq.heappush(open_list, (0, start))  # Chi phí ban đầu là 0 và điểm bắt đầu

    # Duy trì các trạng thái đã thăm
    closed_set = set()

    # Tạo từ điển để tái tạo đường đi
    came_from = {}

    # Tính chi phí g từ start tới mỗi điểm
    g_score = {start: 0}

    # Duy trì số lượng các trạng thái con để mở (beam width)
    while open_list:
        # Lấy `beam_width` phần tử có chi phí thấp nhất từ open_list
        current = heapq.nsmallest(beam_width, open_list, key=lambda x: x[0])

        open_list = current[1:]  # Lọc các phần tử đã lấy ra khỏi open_list

        for _, state in current:
            if state == goal:
                # Tái tạo đường đi
                path = []
                while state in came_from:
                    prev = came_from[state]
                    path.append((state[0] - prev[0], state[1] - prev[1]))
                    state = prev
                path.reverse()
                return path

            # Thêm các trạng thái con vào
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_row, next_col = state[0] + dx, state[1] + dy
                if 0 <= next_row < len(maze) and 0 <= next_col < len(maze[0]) and maze[next_row][next_col] == 0:
                    neighbor = (next_row, next_col)

                    if neighbor not in closed_set:
                        tentative_g_score = g_score[state] + 1
                        if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                            came_from[neighbor] = state
                            g_score[neighbor] = tentative_g_score
                            heapq.heappush(open_list, (g_score[neighbor] + heuristic(neighbor, goal), neighbor))

                        closed_set.add(neighbor)

    return None  # Không tìm thấy đường đi
