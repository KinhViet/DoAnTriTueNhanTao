import pygame
from collections import deque
import copy
import random
import heapq
import math
import time
import numpy as np

pygame.init()

# Cấu hình giao diện
WIDTH = 300
HEIGHT = 570
TILE_SIZE = WIDTH // 3
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sliding Puzzle With Listbox")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Trạng thái ban đầu và đích
GOAL_STATE = [1, 2, 3, 4, 5, 6, 7, 8, 0]

# Danh sách thuật toán
ALGORITHMS = [
    "BFS", "DFS", "IDS", "UCS", "Greedy", "A*", "IDA*",
    "Hill Climbing", "Steepest Hill", "Stochastic Hill", "Local Beam",
    "Simulated Annealing", "Backtracking", "AND-OR Graph", "AC3", "Q-Learning"
]
LISTBOX_RECT = pygame.Rect(10, 310, 180, 240)
LISTBOX_ITEM_HEIGHT = 15
SELECT_BUTTON = pygame.Rect(200, 310, 90, 40)
RANDOM_BUTTON = pygame.Rect(200, 360, 90, 40)
EXPORT_BUTTON = pygame.Rect(200, 410, 90, 40)
selected_algorithm = None
last_solution = None

# Giới hạn thời gian
TIME_LIMIT = 15.0

def is_valid_state(state):
    return len(state) == 9 and all(0 <= x <= 8 for x in state)

def find_empty(state):
    return state.index(0)

def is_solvable(state):
    inversion_count = 0
    state_without_zero = [x for x in state if x != 0]
    for i in range(len(state_without_zero)):
        for j in range(i + 1, len(state_without_zero)):
            if state_without_zero[i] > state_without_zero[j]:
                inversion_count += 1
    return inversion_count % 2 == 0

def generate_random_start(goal, steps=50):
    current_state = goal.copy()
    for _ in range(steps):
        neighbors = get_neighbors(current_state)
        current_state = random.choice(neighbors)
    
    while not is_solvable(current_state):
        current_state = goal.copy()
        for _ in range(steps):
            neighbors = get_neighbors(current_state)
            current_state = random.choice(neighbors)
    
    return current_state

def draw_board(state):
    screen.fill(WHITE)
    for i in range(3):
        for j in range(3):
            idx = i * 3 + j
            value = state[idx]
            if value == 0:
                pygame.draw.rect(screen, GRAY, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else:
                pygame.draw.rect(screen, WHITE, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE), 2)
                font = pygame.font.Font(None, 50)
                text = font.render(str(value), True, BLACK)
                text_rect = text.get_rect(center=(j * TILE_SIZE + TILE_SIZE // 2, i * TILE_SIZE + TILE_SIZE // 2))
                screen.blit(text, text_rect)

    pygame.draw.rect(screen, GRAY, LISTBOX_RECT, 2)
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for i, algo in enumerate(ALGORITHMS):
        item_rect = pygame.Rect(LISTBOX_RECT.x, LISTBOX_RECT.y + i * LISTBOX_ITEM_HEIGHT, LISTBOX_RECT.width, LISTBOX_ITEM_HEIGHT)
        if item_rect.collidepoint((mouse_x, mouse_y)) or algo == selected_algorithm:
            pygame.draw.rect(screen, BLUE, item_rect)
        else:
            pygame.draw.rect(screen, WHITE, item_rect)
        font = pygame.font.Font(None, 20)
        text = font.render(algo, True, BLACK)
        text_rect = text.get_rect(center=item_rect.center)
        screen.blit(text, text_rect)

    if SELECT_BUTTON.collidepoint((mouse_x, mouse_y)):
        pygame.draw.rect(screen, RED, SELECT_BUTTON)
    else:
        pygame.draw.rect(screen, BLUE, SELECT_BUTTON)
    font = pygame.font.Font(None, 24)
    text = font.render("Select", True, WHITE)
    text_rect = text.get_rect(center=SELECT_BUTTON.center)
    screen.blit(text, text_rect)

    if RANDOM_BUTTON.collidepoint((mouse_x, mouse_y)):
        pygame.draw.rect(screen, RED, RANDOM_BUTTON)
    else:
        pygame.draw.rect(screen, BLUE, RANDOM_BUTTON)
    text = font.render("Random", True, WHITE)
    text_rect = text.get_rect(center=RANDOM_BUTTON.center)
    screen.blit(text, text_rect)

    if EXPORT_BUTTON.collidepoint((mouse_x, mouse_y)):
        pygame.draw.rect(screen, RED, EXPORT_BUTTON)
    else:
        pygame.draw.rect(screen, BLUE, EXPORT_BUTTON)
    text = font.render("Export Path", True, WHITE)
    text_rect = text.get_rect(center=EXPORT_BUTTON.center)
    screen.blit(text, text_rect)

    pygame.display.flip()

def move_tile(state, direction):
    empty_idx = find_empty(state)
    row, col = divmod(empty_idx, 3)
    new_row, new_col = row, col
    if direction == "up" and row > 0:
        new_row -= 1
    elif direction == "down" and row < 2:
        new_row += 1
    elif direction == "left" and col > 0:
        new_col -= 1
    elif direction == "right" and col < 2:
        new_col += 1
    else:
        return state
    new_idx = new_row * 3 + new_col
    new_state = copy.deepcopy(state)
    new_state[empty_idx], new_state[new_idx] = new_state[new_idx], new_state[empty_idx]
    return new_state

def get_neighbors(state):
    neighbors = []
    empty_idx = find_empty(state)
    row, col = divmod(empty_idx, 3)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for dx, dy in directions:
        new_row, new_col = row + dx, col + dy
        if 0 <= new_row < 3 and 0 <= new_col < 3:
            new_idx = new_row * 3 + new_col
            new_state = copy.deepcopy(state)
            new_state[empty_idx], new_state[new_idx] = new_state[new_idx], new_state[empty_idx]
            neighbors.append(new_state)
    return neighbors

def manhattan_distance(state, goal):
    distance = 0
    for i in range(9):
        if state[i] != 0:
            goal_pos = goal.index(state[i])
            row, col = divmod(i, 3)
            goal_row, goal_col = divmod(goal_pos, 3)
            distance += abs(row - goal_row) + abs(col - goal_col)
    return distance

def time_algorithm(algorithm, start_state, goal_state):
    start_time = time.time()
    try:
        solution = algorithm(start_state, goal_state)
        execution_time = time.time() - start_time
        if execution_time > TIME_LIMIT:
            print(f"{algorithm.__name__} exceeded time limit of {TIME_LIMIT} seconds!")
            return None, execution_time
        return solution, execution_time
    except Exception as e:
        execution_time = time.time() - start_time
        print(f"Error in {algorithm.__name__}: {str(e)}")
        return None, execution_time

# BFS
def bfs(start_state, goal_state):
    if not is_valid_state(start_state) or not is_valid_state(goal_state):
        return None
    queue = deque([(start_state, [])])
    visited = {tuple(start_state)}
    while queue:
        current_state, path = queue.popleft()
        if current_state == goal_state:
            return path
        for next_state in get_neighbors(current_state):
            if tuple(next_state) not in visited:
                visited.add(tuple(next_state))
                queue.append((next_state, path + [next_state]))
    return None

# DFS
def dfs(start_state, goal_state):
    if not is_valid_state(start_state) or not is_valid_state(goal_state):
        return None
    stack = [(start_state, [])]
    visited = {tuple(start_state)}
    while stack:
        current_state, path = stack.pop()
        if current_state == goal_state:
            return path
        for next_state in get_neighbors(current_state):
            if tuple(next_state) not in visited:
                visited.add(tuple(next_state))
                stack.append((next_state, path + [next_state]))
    return None

# IDS
def ids(start_state, goal_state):
    if not is_valid_state(start_state) or not is_valid_state(goal_state):
        return None
    def dls(state, path, depth, visited):
        if state == goal_state:
            return path
        if depth <= 0:
            return None
        for next_state in get_neighbors(state):
            if tuple(next_state) not in visited:
                visited.add(tuple(next_state))
                result = dls(next_state, path + [next_state], depth - 1, visited)
                if result is not None:
                    return result
        return None
    depth = 0
    while True:
        visited = {tuple(start_state)}
        result = dls(start_state, [], depth, visited)
        if result is not None:
            return result
        depth += 1

# UCS
def ucs(start_state, goal_state):
    if not is_valid_state(start_state) or not is_valid_state(goal_state):
        return None
    priority_queue = [(0, start_state, [])]
    visited = {tuple(start_state): 0}
    while priority_queue:
        cost, current_state, path = heapq.heappop(priority_queue)
        if current_state == goal_state:
            return path
        for next_state in get_neighbors(current_state):
            new_cost = cost + 1
            if tuple(next_state) not in visited or new_cost < visited[tuple(next_state)]:
                visited[tuple(next_state)] = new_cost
                heapq.heappush(priority_queue, (new_cost, next_state, path + [next_state]))
    return None

# Greedy Best-First Search
def greedy(start_state, goal_state):
    if not is_valid_state(start_state) or not is_valid_state(goal_state):
        return None
    priority_queue = [(manhattan_distance(start_state, goal_state), start_state, [])]
    visited = {tuple(start_state)}
    while priority_queue:
        _, current_state, path = heapq.heappop(priority_queue)
        if current_state == goal_state:
            return path
        for next_state in get_neighbors(current_state):
            if tuple(next_state) not in visited:
                visited.add(tuple(next_state))
                priority = manhattan_distance(next_state, goal_state)
                heapq.heappush(priority_queue, (priority, next_state, path + [next_state]))
    return None

# A* Search
def astar(start_state, goal_state):
    if not is_valid_state(start_state) or not is_valid_state(goal_state):
        return None
    priority_queue = [(manhattan_distance(start_state, goal_state), 0, start_state, [])]
    visited = {tuple(start_state): 0}
    while priority_queue:
        _, g_score, current_state, path = heapq.heappop(priority_queue)
        if current_state == goal_state:
            return path
        for next_state in get_neighbors(current_state):
            new_g_score = g_score + 1
            if tuple(next_state) not in visited or new_g_score < visited[tuple(next_state)]:
                visited[tuple(next_state)] = new_g_score
                h_score = manhattan_distance(next_state, goal_state)
                f_score = new_g_score + h_score
                heapq.heappush(priority_queue, (f_score, new_g_score, next_state, path + [next_state]))
    return None

# IDA* Search
def idastar(start_state, goal_state):
    if not is_valid_state(start_state) or not is_valid_state(goal_state):
        return None
    def search(state, g_score, path, bound, visited):
        f_score = g_score + manhattan_distance(state, goal_state)
        if f_score > bound:
            return None, f_score
        if state == goal_state:
            return path, bound
        min_bound = float('inf')
        for next_state in get_neighbors(state):
            if tuple(next_state) not in visited:
                visited.add(tuple(next_state))
                new_path = path + [next_state]
                result, new_bound = search(next_state, g_score + 1, new_path, bound, visited)
                visited.remove(tuple(next_state))
                if result is not None:
                    return result, bound
                min_bound = min(min_bound, new_bound)
        return None, min_bound
    bound = manhattan_distance(start_state, goal_state)
    while True:
        visited = {tuple(start_state)}
        result, new_bound = search(start_state, 0, [], bound, visited)
        if result is not None:
            return result
        if new_bound == float('inf'):
            return None
        bound = new_bound

# Hill Climbing
def hill_climbing(start_state, goal_state):
    if not is_valid_state(start_state) or not is_valid_state(goal_state):
        return None
    current_state = start_state
    path = []
    visited = {tuple(current_state)}
    max_steps = 1000
    current_distance = manhattan_distance(current_state, goal_state)
    step = 0
    while current_state != goal_state and step < max_steps:
        neighbors = get_neighbors(current_state)
        best_neighbor = None
        best_distance = current_distance
        for neighbor in neighbors:
            if tuple(neighbor) not in visited:
                distance = manhattan_distance(neighbor, goal_state)
                if distance < best_distance:
                    best_distance = distance
                    best_neighbor = neighbor
                    break
        if best_neighbor is None:
            return None
        current_state = best_neighbor
        current_distance = best_distance
        path.append(current_state)
        visited.add(tuple(current_state))
        step += 1
    if step >= max_steps:
        return None
    return path

# Steepest Hill Climbing
def steepest_hill(start_state, goal_state):
    if not is_valid_state(start_state) or not is_valid_state(goal_state):
        return None
    current_state = start_state
    path = []
    visited = {tuple(current_state)}
    max_steps = 1000
    current_distance = manhattan_distance(current_state, goal_state)
    step = 0
    while current_state != goal_state and step < max_steps:
        neighbors = get_neighbors(current_state)
        best_neighbor = None
        best_distance = float('inf')
        for neighbor in neighbors:
            if tuple(neighbor) not in visited:
                distance = manhattan_distance(neighbor, goal_state)
                if distance < best_distance:
                    best_distance = distance
                    best_neighbor = neighbor
        if best_neighbor is None or best_distance >= current_distance:
            return None
        current_state = best_neighbor
        current_distance = best_distance
        path.append(current_state)
        visited.add(tuple(current_state))
        step += 1
    if step >= max_steps:
        return None
    return path

# Stochastic Hill Climbing
def stochastic_hill(start_state, goal_state):
    if not is_valid_state(start_state) or not is_valid_state(goal_state):
        return None
    current_state = start_state
    path = []
    visited = {tuple(current_state)}
    max_steps = 1000
    step = 0
    current_distance = manhattan_distance(current_state, goal_state)
    while current_state != goal_state and step < max_steps:
        neighbors = get_neighbors(current_state)
        better_neighbors = []
        for neighbor in neighbors:
            if tuple(neighbor) not in visited:
                distance = manhattan_distance(neighbor, goal_state)
                if distance < current_distance:
                    better_neighbors.append((neighbor, distance))
        if not better_neighbors:
            return None
        next_state, next_distance = random.choice(better_neighbors)
        current_state = next_state
        current_distance = next_distance
        path.append(current_state)
        visited.add(tuple(current_state))
        step += 1
    if step >= max_steps:
        return None
    return path

# Local Beam Search
def local_beam(start_state, goal_state):
    if not is_valid_state(start_state) or not is_valid_state(goal_state):
        return None
    beam_width = 3
    states = [(start_state, [])]
    visited = {tuple(start_state)}
    max_steps = 1000
    step = 0
    while states and step < max_steps:
        new_states = []
        for current_state, path in states:
            if current_state == goal_state:
                return path
            for next_state in get_neighbors(current_state):
                if tuple(next_state) not in visited:
                    visited.add(tuple(next_state))
                    new_states.append((next_state, path + [next_state]))
        new_states.sort(key=lambda x: manhattan_distance(x[0], goal_state))
        states = new_states[:beam_width]
        step += 1
    return None

# Simulated Annealing
def simulated_annealing(start_state, goal_state):
    if not is_valid_state(start_state) or not is_valid_state(goal_state):
        return None
    current_state = start_state
    path = []
    visited = {tuple(current_state)}
    initial_temperature = 1000.0
    cooling_rate = 0.995
    min_temperature = 0.01
    max_steps = 10000
    temperature = initial_temperature
    step = 0
    current_distance = manhattan_distance(current_state, goal_state)
    while current_state != goal_state and step < max_steps and temperature > min_temperature:
        neighbors = get_neighbors(current_state)
        next_state = random.choice(neighbors)
        if tuple(next_state) in visited:
            continue
        next_distance = manhattan_distance(next_state, goal_state)
        delta_e = next_distance - current_distance
        if delta_e < 0 or random.random() < math.exp(-delta_e / temperature):
            current_state = next_state
            current_distance = next_distance
            path.append(current_state)
            visited.add(tuple(current_state))
        step += 1
        temperature *= cooling_rate
    if current_state != goal_state:
        return None
    return path

# Backtracking
def backtracking(start_state, goal_state):
    if not is_valid_state(start_state) or not is_valid_state(goal_state):
        return None
    visited = set()
    max_depth = 50
    def backtrack(state, path, depth):
        if state == goal_state:
            return path
        if depth > max_depth:
            return None
        state_tuple = tuple(state)
        if state_tuple in visited:
            return None
        visited.add(state_tuple)
        neighbors = get_neighbors(state)
        neighbors.sort(key=lambda x: manhattan_distance(x, goal_state))
        for next_state in neighbors:
            result = backtrack(next_state, path + [next_state], depth + 1)
            if result is not None:
                return result
        return None
    return backtrack(start_state, [], 0)

# AND-OR Graph Search
def and_or_graph(start_state, goal_state):
    if not is_valid_state(start_state) or not is_valid_state(goal_state):
        return None
    priority_queue = [(manhattan_distance(start_state, goal_state), 0, start_state, [])]
    visited = {tuple(start_state): 0}
    while priority_queue:
        _, g_score, current_state, path = heapq.heappop(priority_queue)
        if current_state == goal_state:
            return path
        for next_state in get_neighbors(current_state):
            new_g_score = g_score + 1
            if tuple(next_state) not in visited or new_g_score < visited[tuple(next_state)]:
                visited[tuple(next_state)] = new_g_score
                h_score = manhattan_distance(next_state, goal_state)
                f_score = new_g_score + h_score
                heapq.heappush(priority_queue, (f_score, new_g_score, next_state, path + [next_state]))
    return None

# AC3 (Constraint Satisfaction Problem)
def ac3(start_state, goal_state):
    if not is_valid_state(start_state) or not is_valid_state(goal_state):
        return None
    def revise(domain, constraints, pos1, pos2):
        revised = False
        new_domain = domain[pos1].copy()
        for x in domain[pos1]:
            if not any(y in domain[pos2] for y in constraints[(pos1, pos2)] if y != x):
                new_domain.remove(x)
                revised = True
        domain[pos1] = new_domain
        return revised
    domain = {i: list(range(9)) for i in range(9)}
    domain[find_empty(start_state)] = [0]
    constraints = {(i, j): list(range(9)) for i in range(9) for j in range(9) if i != j}
    queue = [(i, j) for i in range(9) for j in range(9) if i != j]
    while queue:
        pos1, pos2 = queue.pop(0)
        if revise(domain, constraints, pos1, pos2):
            if not domain[pos1]:
                return None
            for pos3 in range(9):
                if pos3 != pos1 and pos3 != pos2:
                    queue.append((pos3, pos1))
    state = [0] * 9
    for i in range(9):
        if domain[i]:
            state[i] = domain[i][0]
    if state == goal_state:
        return [state]
    return None

# Q-Learning
def q_learning(start_state, goal_state):
    if not is_valid_state(start_state) or not is_valid_state(goal_state):
        return None
    q_table = {}
    alpha = 0.1
    gamma = 0.9
    epsilon = 0.1
    episodes = 1000
    max_steps = 100
    actions = ["up", "down", "left", "right"]
    def state_to_tuple(state):
        return tuple(state)
    def get_action(state):
        if random.random() < epsilon:
            return random.choice(actions)
        state_tuple = state_to_tuple(state)
        if state_tuple not in q_table:
            q_table[state_tuple] = {a: 0.0 for a in actions}
        return max(q_table[state_tuple], key=q_table[state_tuple].get)
    path = []
    current_state = start_state
    for _ in range(episodes):
        current_state = start_state
        for _ in range(max_steps):
            state_tuple = state_to_tuple(current_state)
            if state_tuple not in q_table:
                q_table[state_tuple] = {a: 0.0 for a in actions}
            action = get_action(current_state)
            next_state = move_tile(current_state, action)
            reward = -manhattan_distance(next_state, goal_state)
            if next_state == goal_state:
                reward = 100
            next_state_tuple = state_to_tuple(next_state)
            if next_state_tuple not in q_table:
                q_table[next_state_tuple] = {a: 0.0 for a in actions}
            q_table[state_tuple][action] += alpha * (
                reward + gamma * max(q_table[next_state_tuple].values()) - q_table[state_tuple][action]
            )
            current_state = next_state
            if current_state == goal_state:
                break
    current_state = start_state
    steps = 0
    while current_state != goal_state and steps < max_steps:
        state_tuple = state_to_tuple(current_state)
        if state_tuple not in q_table:
            return None
        action = max(q_table[state_tuple], key=q_table[state_tuple].get)
        next_state = move_tile(current_state, action)
        path.append(next_state)
        current_state = next_state
        steps += 1
    if current_state != goal_state:
        return None
    return path

def export_path(solution, algorithm_name):
    if not solution:
        print("No solution to export!")
        return
    with open("solution_path.txt", "w") as f:
        f.write(f"Solution Path for {algorithm_name}\n")
        f.write(f"Number of steps: {len(solution)}\n\n")
        for i, state in enumerate(solution):
            f.write(f"Step {i + 1}:\n")
            for row in range(3):
                f.write(" ".join(map(str, state[row * 3:(row + 1) * 3])) + "\n")
            f.write("\n")
    print("Solution path exported to solution_path.txt")

current_state = generate_random_start(GOAL_STATE, steps=20)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if LISTBOX_RECT.collidepoint(x, y):
                index = (y - LISTBOX_RECT.y) // LISTBOX_ITEM_HEIGHT
                if 0 <= index < len(ALGORITHMS):
                    selected_algorithm = ALGORITHMS[index]
                    print(f"Selected algorithm: {selected_algorithm}")
            elif SELECT_BUTTON.collidepoint(x, y) and selected_algorithm:
                print(f"Solving with {selected_algorithm}...")
                solution, execution_time = None, 0.0
                if selected_algorithm == "BFS":
                    solution, execution_time = time_algorithm(bfs, current_state, GOAL_STATE)
                elif selected_algorithm == "DFS":
                    solution, execution_time = time_algorithm(dfs, current_state, GOAL_STATE)
                elif selected_algorithm == "IDS":
                    solution, execution_time = time_algorithm(ids, current_state, GOAL_STATE)
                elif selected_algorithm == "UCS":
                    solution, execution_time = time_algorithm(ucs, current_state, GOAL_STATE)
                elif selected_algorithm == "Greedy":
                    solution, execution_time = time_algorithm(greedy, current_state, GOAL_STATE)
                elif selected_algorithm == "A*":
                    solution, execution_time = time_algorithm(astar, current_state, GOAL_STATE)
                elif selected_algorithm == "IDA*":
                    solution, execution_time = time_algorithm(idastar, current_state, GOAL_STATE)
                elif selected_algorithm == "Hill Climbing":
                    solution, execution_time = time_algorithm(hill_climbing, current_state, GOAL_STATE)
                elif selected_algorithm == "Steepest Hill":
                    solution, execution_time = time_algorithm(steepest_hill, current_state, GOAL_STATE)
                elif selected_algorithm == "Stochastic Hill":
                    solution, execution_time = time_algorithm(stochastic_hill, current_state, GOAL_STATE)
                elif selected_algorithm == "Local Beam":
                    solution, execution_time = time_algorithm(local_beam, current_state, GOAL_STATE)
                elif selected_algorithm == "Simulated Annealing":
                    solution, execution_time = time_algorithm(simulated_annealing, current_state, GOAL_STATE)
                elif selected_algorithm == "Backtracking":
                    solution, execution_time = time_algorithm(backtracking, current_state, GOAL_STATE)
                elif selected_algorithm == "AND-OR Graph":
                    solution, execution_time = time_algorithm(and_or_graph, current_state, GOAL_STATE)
                elif selected_algorithm == "AC3":
                    solution, execution_time = time_algorithm(ac3, current_state, GOAL_STATE)
                elif selected_algorithm == "Q-Learning":
                    solution, execution_time = time_algorithm(q_learning, current_state, GOAL_STATE)
                print(f"Execution time: {execution_time:.3f} seconds")
                last_solution = solution
                if solution:
                    print(f"Solution found with {selected_algorithm}! Steps: {len(solution)}")
                    for state in solution:
                        current_state = state
                        draw_board(current_state)
                        pygame.time.wait(500)
                else:
                    print(f"No solution found with {selected_algorithm}!")
            elif RANDOM_BUTTON.collidepoint(x, y):
                current_state = generate_random_start(GOAL_STATE, steps=20)
                print("Generated new random state:", current_state)
                last_solution = None
            elif EXPORT_BUTTON.collidepoint(x, y):
                if last_solution and selected_algorithm:
                    export_path(last_solution, selected_algorithm)
                else:
                    print("No solution to export!")
            if y < 300:
                row, col = y // TILE_SIZE, x // TILE_SIZE
                idx = row * 3 + col
                empty_idx = find_empty(current_state)
                empty_row, empty_col = divmod(empty_idx, 3)
                if abs(row - empty_row) + abs(col - empty_col) == 1:
                    current_state[idx], current_state[empty_idx] = current_state[empty_idx], current_state[idx]
                    last_solution = None
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                current_state = move_tile(current_state, "up")
                last_solution = None
            elif event.key == pygame.K_DOWN:
                current_state = move_tile(current_state, "down")
                last_solution = None
            elif event.key == pygame.K_LEFT:
                current_state = move_tile(current_state, "left")
                last_solution = None
            elif event.key == pygame.K_RIGHT:
                current_state = move_tile(current_state, "right")
                last_solution = None
    draw_board(current_state)

pygame.quit()