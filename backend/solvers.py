import heapq
from collections import deque
from typing import List, Tuple, Optional
from .environment import JugEnvironment, State, Action

def heuristic(state: State, target: int) -> int:
    # Admissible heuristic: 0 if goal reached, 1 otherwise
    if any(v == target for v in state.volumes):
        return 0
    return 1

def greedy_heuristic(state: State, target: int) -> int:
    # Non-admissible, aggressive heuristic based on volume proximity
    if any(v == target for v in state.volumes):
        return 0
    return min(abs(v - target) for v in state.volumes)

def is_goal(state: State, target: int) -> bool:
    return any(v == target for v in state.volumes)

def uniform_cost_search(env: JugEnvironment, start_state: State, target: int) -> Tuple[List[Tuple[Action, State]], int, int]:
    counter = 0
    frontier = [(0, counter, start_state, [])]
    visited = {}
    nodes_expanded = 0
    
    while frontier:
        cost_so_far, _, current_state, path = heapq.heappop(frontier)
        
        if current_state in visited and visited[current_state] <= cost_so_far:
            continue
            
        visited[current_state] = cost_so_far
        nodes_expanded += 1
        
        if is_goal(current_state, target):
            return path, cost_so_far, nodes_expanded
            
        for action, next_state, action_cost in env.get_successors(current_state):
            new_cost = cost_so_far + action_cost
            if next_state not in visited or new_cost < visited.get(next_state, float('inf')):
                counter += 1
                heapq.heappush(frontier, (new_cost, counter, next_state, path + [(action, next_state)]))
                
    return [], -1, nodes_expanded

def a_star_search(env: JugEnvironment, start_state: State, target: int) -> Tuple[List[Tuple[Action, State]], int, int]:
    counter = 0
    frontier = [(heuristic(start_state, target), counter, 0, start_state, [])]
    visited = {}
    nodes_expanded = 0
    
    while frontier:
        f_cost, _, g_cost, current_state, path = heapq.heappop(frontier)
        
        if current_state in visited and visited[current_state] <= g_cost:
            continue
            
        visited[current_state] = g_cost
        nodes_expanded += 1
        
        if is_goal(current_state, target):
            return path, g_cost, nodes_expanded
            
        for action, next_state, action_cost in env.get_successors(current_state):
            new_g_cost = g_cost + action_cost
            if next_state not in visited or new_g_cost < visited.get(next_state, float('inf')):
                counter += 1
                new_f_cost = new_g_cost + heuristic(next_state, target)
                heapq.heappush(frontier, (new_f_cost, counter, new_g_cost, next_state, path + [(action, next_state)]))
                
    return [], -1, nodes_expanded

def check_heuristic_admissibility(env: JugEnvironment, start_state: State, target: int) -> bool:
    _, ucs_cost, _ = uniform_cost_search(env, start_state, target)
    _, astar_cost, _ = a_star_search(env, start_state, target)
    
    if ucs_cost == -1 or astar_cost == -1:
        return True
        
    if astar_cost > ucs_cost:
        return False
    return True

def expectimax(env: JugEnvironment, state: State, target: int, depth: int) -> Tuple[Optional[Action], float, int]:
    nodes_expanded = [0]
    
    def value(current_state: State, current_depth: int) -> float:
        if is_goal(current_state, target):
            return 0.0
        if current_depth == 0:
            return 1000.0
            
        nodes_expanded[0] += 1
        return min_node(current_state, current_depth)
        
    def min_node(current_state: State, current_depth: int) -> float:
        best_expected_cost = float('inf')
        for action, stochastic_outcomes in env.get_stochastic_successors(current_state):
            expected_cost = 0.0
            for next_state, prob, action_cost in stochastic_outcomes:
                expected_cost += prob * (action_cost + value(next_state, current_depth - 1))
            if expected_cost < best_expected_cost:
                best_expected_cost = expected_cost
        return best_expected_cost

    best_action = None
    best_expected_cost = float('inf')
    
    nodes_expanded[0] += 1
    for action, stochastic_outcomes in env.get_stochastic_successors(state):
        expected_cost = 0.0
        for next_state, prob, action_cost in stochastic_outcomes:
            expected_cost += prob * (action_cost + value(next_state, depth - 1))
        
        if expected_cost < best_expected_cost:
            best_expected_cost = expected_cost
            best_action = action
            
    # For compatibility with metrics tracker, we return a list as the first element
    # expectimax doesn't naturally return a single path down multiple stochastic branches,
    # so we mock a path variable here just holding the action.
    mock_path = [best_action] if best_action else []
    return mock_path, best_expected_cost, nodes_expanded[0]

def breadth_first_search(env: JugEnvironment, start_state: State, target: int) -> Tuple[List[Tuple[Action, State]], int, int]:
    frontier = deque([(start_state, [], 0)])
    visited = {start_state}
    nodes_expanded = 0
    
    if is_goal(start_state, target):
        return [], 0, nodes_expanded
        
    while frontier:
        current_state, path, cost_so_far = frontier.popleft()
        nodes_expanded += 1
        
        for action, next_state, action_cost in env.get_successors(current_state):
            if next_state not in visited:
                new_cost = cost_so_far + action_cost
                new_path = path + [(action, next_state)]
                
                if is_goal(next_state, target):
                    return new_path, new_cost, nodes_expanded
                    
                visited.add(next_state)
                frontier.append((next_state, new_path, new_cost))
                
    return [], -1, nodes_expanded

def depth_first_search(env: JugEnvironment, start_state: State, target: int, max_depth: int = 50) -> Tuple[List[Tuple[Action, State]], int, int]:
    frontier = [(start_state, [], 0)]
    visited = {start_state: 0}
    nodes_expanded = 0
    
    while frontier:
        current_state, path, cost_so_far = frontier.pop()
        nodes_expanded += 1
        
        if is_goal(current_state, target):
            return path, cost_so_far, nodes_expanded
            
        if len(path) >= max_depth:
            continue
            
        # Sort so we pop the first generated action first
        for action, next_state, action_cost in sorted(env.get_successors(current_state), key=lambda x: str(x[0]), reverse=True):
            new_depth = len(path) + 1
            if next_state not in visited or new_depth < visited.get(next_state, float('inf')):
                visited[next_state] = new_depth
                new_cost = cost_so_far + action_cost
                frontier.append((next_state, path + [(action, next_state)], new_cost))
                
    return [], -1, nodes_expanded

def greedy_best_first_search(env: JugEnvironment, start_state: State, target: int) -> Tuple[List[Tuple[Action, State]], int, int]:
    counter = 0
    frontier = [(greedy_heuristic(start_state, target), counter, start_state, [], 0)]
    visited = set()
    nodes_expanded = 0
    
    while frontier:
        h_cost, _, current_state, path, true_cost = heapq.heappop(frontier)
        
        if current_state in visited:
            continue
            
        visited.add(current_state)
        nodes_expanded += 1
        
        if is_goal(current_state, target):
            return path, true_cost, nodes_expanded
            
        for action, next_state, action_cost in env.get_successors(current_state):
            if next_state not in visited:
                counter += 1
                new_h = greedy_heuristic(next_state, target)
                new_cost = true_cost + action_cost
                heapq.heappush(frontier, (new_h, counter, next_state, path + [(action, next_state)], new_cost))
                
    return [], -1, nodes_expanded
