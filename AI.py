import pygame
from collections import deque
import heapq
import random
import time
import math
import numpy as np
import pickle

directions = [
    (-1, 0),  # lên
    (1, 0),   # xuống
    (0, -1),  # trái
    (0, 1),   # phải
]

# Hàm lưu và tải bảng Q riêng
def load_q_table():
    try:
        with open("q_table.pkl", "rb") as f:
            q_table = pickle.load(f)
            print("Loaded Q-table from file")
            return q_table
    except FileNotFoundError:
        print("Creating new Q-table")
        return {}

def save_q_table(q_table):
    try:
        with open("q_table.pkl", "wb") as f:
            pickle.dump(q_table, f)
        print("Saved Q-table to file")
    except Exception as e:
        print(f"Error saving Q-table: {e}")
        
# Hàm thuật toán BFS
def solve_maze_bfs(maze, start, goal):
    rows = len(maze)
    cols = len(maze[0])
    queue = deque([(start)])
    visited = {start}
    came_from = {}
    
    while queue:
        current = queue.popleft()
        if current == goal:
            path = []
            while current in came_from:
                prev = came_from[current]
                path.append((current[0] - prev[0], current[1] - prev[1]))
                current = prev
            path.reverse()
            return path
            
        for dx, dy in directions:
            next_row = current[0] + dx
            next_col = current[1] + dy
            neighbor = (next_row, next_col)
            if (0 <= next_row < rows and 
                0 <= next_col < cols and 
                maze[next_row][next_col] == 0 and
                neighbor not in visited):
                queue.append(neighbor)
                visited.add(neighbor)
                came_from[neighbor] = current
    
    return None

# Hàm thuật toán A*
def heuristic(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
def solve_maze_astar(maze, start, goal):
    rows = len(maze)
    cols = len(maze[0])
    closed_set = set()
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {start: 0}

    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == goal:
            path = []
            while current in came_from:
                prev = came_from[current]
                path.append((current[0] - prev[0], current[1] - prev[1]))
                current = prev
            path.reverse()
            return path
        
        closed_set.add(current)
        for dx, dy in directions:
            neighbor = (current[0] + dx, current[1] + dy)
            if (neighbor[0] < 0 or neighbor[0] >= rows or
                neighbor[1] < 0 or neighbor[1] >= cols or
                maze[neighbor[0]][neighbor[1]] == 1 or
                neighbor in closed_set):
                continue
            
            tentative_g_score = g_score[current] + 1
            if (neighbor not in g_score or tentative_g_score < g_score[neighbor]):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))
    
    return None

def calculate_max_depth(maze, complexity='medium'):
    size = len(maze) * len(maze[0])
    wall_density = sum(row.count(1) for row in maze) / size
    factor = {'simple': 0.3, 'medium': 0.5, 'complex': 0.7}.get(complexity, 0.5)
    if wall_density > 0.5:
        factor += 0.1
    return int(factor * size)

# SIMULATED ANNEALING
def schedule(t, k=20, lam=0.005, limit=1000):
    return (k * np.exp(-lam * t) if t < limit else 0)

def simulated_annealing_path(maze, start, goal, max_iterations=1000, initial_temp=100, cooling_rate=0.99):
    current = start
    current_cost = heuristic(current, goal)
    temperature = initial_temp
    path = []

    for t in range(max_iterations):
        if current == goal:
            print(f"Thuyền đến được người chơi sau {t} lần lặp.")
            return path

        neighbors = []
        for dx, dy in directions:
            next_row, next_col = current[0] + dx, current[1] + dy
            if 0 <= next_row < len(maze) and 0 <= next_col < len(maze[0]) and maze[next_row][next_col] == 0:
                neighbors.append((next_row, next_col))

        if not neighbors:
            print("Thuyền bị kẹt.")
            break

        next_position = random.choice(neighbors)
        next_cost = heuristic(next_position, goal)
        delta_cost = next_cost - current_cost

        if delta_cost < 0 or random.uniform(0, 1) < math.exp(-delta_cost / temperature):
            current = next_position
            current_cost = next_cost
            path.append((next_position[0] - start[0], next_position[1] - start[1]))

        temperature *= cooling_rate
        if temperature < 1e-3:
            print("Nhiệt độ quá thấp, dừng lại.")
            break

    return path if current == goal else None

def solve_maze_ucs(maze, start, goal):
    rows = len(maze)
    cols = len(maze[0])
    open_set = []
    heapq.heappush(open_set, (0, start))
    visited = set()
    came_from = {}
    g_score = {start: 0}

    while open_set:
        current_cost, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current in came_from:
                prev = came_from[current]
                path.append((current[0] - prev[0], current[1] - prev[1]))
                current = prev
            path.reverse()
            return path
        
        for dx, dy in directions:
            next_row = current[0] + dx
            next_col = current[1] + dy
            neighbor = (next_row, next_col)
            if 0 <= next_row < rows and 0 <= next_col < cols and maze[next_row][next_col] == 0:
                tentative_g_score = current_cost + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    heapq.heappush(open_set, (tentative_g_score, neighbor))
    
    return None

def stochastic_hill_climbing(maze, start, goal, max_iterations=1000):
    current = start
    path = []
    iteration = 0

    while current != goal and iteration < max_iterations:
        neighbors = []
        for dx, dy in directions:
            next_row, next_col = current[0] + dx, current[1] + dy
            if 0 <= next_row < len(maze) and 0 <= next_col < len(maze[0]) and maze[next_row][next_col] == 0:
                neighbors.append((next_row, next_col))

        if not neighbors:
            print("Thuyền bị kẹt.")
            break

        next_position = min(neighbors, key=lambda x: heuristic(x, goal))
        if heuristic(next_position, goal) < heuristic(current, goal):
            path.append((next_position[0] - start[0], next_position[1] - start[1]))
            current = next_position
        else:
            print(f"Kẹt tại {current}, không tìm thấy cải tiến.")
            break

        iteration += 1

    return path if current == goal else None

def beam_search(maze, start, goal, beam_width=3):
    open_list = []
    heapq.heappush(open_list, (0, start))
    closed_set = set()
    came_from = {}
    g_score = {start: 0}

    while open_list:
        current = heapq.nsmallest(beam_width, open_list, key=lambda x: x[0])
        open_list = current[1:]

        for _, state in current:
            if state == goal:
                path = []
                while state in came_from:
                    prev = came_from[state]
                    path.append((state[0] - prev[0], state[1] - prev[1]))
                    state = prev
                path.reverse()
                return path

            for dx, dy in directions:
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

    return None

def solve_maze_qlearning(maze, start, goal, episodes=200, alpha=0.1, gamma=0.9, epsilon=0.1):
    """
    Thuật toán Q-Learning tối ưu cho điều hướng mê cung.
    """
    rows, cols = len(maze), len(maze[0])
    actions = [0, 1, 2, 3]
    q_table = {}
    
    # Tải bảng Q nếu tồn tại
    try:
        with open("q_table.pkl", "rb") as f:
            q_table = pickle.load(f)
            print("Đã tải bảng Q từ file")
            # Nếu bảng Q có dữ liệu, giảm episodes xuống 50
            if len(q_table) > 0:
                episodes = 50
            else:
                episodes = max(100, episodes // 2)
    except FileNotFoundError:
        print("Tạo bảng Q mới")
    
    def get_valid_actions(state):
        valid = []
        for i, (dx, dy) in enumerate(directions):
            next_row, next_col = state[0] + dx, state[1] + dy
            if 0 <= next_row < rows and 0 <= next_col < cols and maze[next_row][next_col] == 0:
                valid.append(i)
        return valid

    def choose_action(state, valid_actions):
        if random.uniform(0, 1) < epsilon:
            return random.choice(valid_actions) if valid_actions else random.choice(actions)
        state_q = q_table.get(state, {a: 0 for a in actions})
        return max(valid_actions, key=lambda a: state_q.get(a, 0), default=random.choice(actions))

    def get_next_state(state, action):
        dx, dy = directions[action]
        next_row, next_col = state[0] + dx, state[1] + dy
        if 0 <= next_row < rows and 0 <= next_col < cols and maze[next_row][next_col] == 0:
            return (next_row, next_col)
        return state

    # Huấn luyện với giới hạn trạng thái
    for episode in range(episodes):
        state = start
        visited_states = set()
        while state != goal:
            if state not in visited_states:
                visited_states.add(state)
                if state not in q_table:
                    q_table[state] = {a: 0 for a in actions}  # Khởi tạo trạng thái mới
            valid_actions = get_valid_actions(state)
            if not valid_actions:
                break
            action = choose_action(state, valid_actions)
            next_state = get_next_state(state, action)
            
            reward = 100 if next_state == goal else -1
            if next_state == state:
                reward = -10
                
            # Đảm bảo next_state được khởi tạo trước khi truy cập
            if next_state not in q_table:
                q_table[next_state] = {a: 0 for a in actions}
            
            next_valid_actions = get_valid_actions(next_state)
            next_max_q = max([q_table[next_state].get(a, 0) for a in next_valid_actions], default=0)
            q_table[state][action] += alpha * (reward + gamma * next_max_q - q_table[state][action])
            
            state = next_state

    # Tạo đường đi
    path = []
    current = start
    visited = set()
    max_steps = rows * cols
    step = 0

    while current != goal and step < max_steps and current not in visited:
        visited.add(current)
        valid_actions = get_valid_actions(current)
        if not valid_actions:
            break
        state_q = q_table.get(current, {a: 0 for a in actions})
        action = max(valid_actions, key=lambda a: state_q.get(a, 0), default=random.choice(valid_actions))
        dx, dy = directions[action]
        next_state = (current[0] + dx, current[1] + dy)
        if next_state == current:
            break
        path.append((dx, dy))
        current = next_state
        step += 1

    # Lưu bảng Q nếu tìm được đường đi
    if path and current == goal:
        try:
            with open("q_table.pkl", "wb") as f:
                pickle.dump(q_table, f)
            print("Đã lưu bảng Q vào file")
        except Exception as e:
            print(f"Lỗi khi lưu bảng Q: {e}")

    return path if current == goal else None