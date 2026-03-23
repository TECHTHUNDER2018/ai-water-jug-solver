import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from .environment import JugEnvironment, State
from .solvers import uniform_cost_search, a_star_search, expectimax, check_heuristic_admissibility
from .solvers import breadth_first_search, depth_first_search, greedy_best_first_search
from .metrics import MetricsTracker

app = FastAPI(title="Water Jug AI Solver")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SolveRequest(BaseModel):
    capacities: List[int]
    start_volumes: List[int]
    target: int
    algorithm: str
    fill_cost: int = 3
    empty_cost: int = 1
    pour_cost: int = 2
    k: float = 0.5
    expectimax_depth: int = 3

@app.post("/api/solve")
def solve(request: SolveRequest):
    # SECURITY & BUG PROTECTIONS:
    # 1. Prevent out-of-memory DOS by limiting the Number of Jugs.
    if not (1 <= len(request.capacities) <= 5):
        raise HTTPException(status_code=400, detail="Server Protection: Max 5 jugs allowed.")
    
    # 2. Prevent massive state spaces by limiting the Max Capacity allowed per jug
    if any(c <= 0 or c > 100 for c in request.capacities):
        raise HTTPException(status_code=400, detail="Server Protection: Jug capacity must be 1 to 100.")

    # 3. Prevent Negative Volumes or starting with more water than capacity
    if any(s < 0 for s in request.start_volumes):
        raise HTTPException(status_code=400, detail="Start volumes cannot be negative.")
    if any(s > c for s, c in zip(request.start_volumes, request.capacities)):
        raise HTTPException(status_code=400, detail="Start volume cannot exceed capacity.")
        
    # 4. Prevent Expectimax tree-explosion DOS by forcing a hard cap on depth
    request.expectimax_depth = min(request.expectimax_depth, 4)
    request.expectimax_depth = max(request.expectimax_depth, 1)

    if len(request.capacities) != len(request.start_volumes):
        raise HTTPException(status_code=400, detail=f"Mismatch: passed {len(request.capacities)} capacities but {len(request.start_volumes)} start volumes.")

    env = JugEnvironment(
        capacities=tuple(request.capacities),
        fill_cost=request.fill_cost,
        empty_cost=request.empty_cost,
        pour_cost=request.pour_cost,
        k=request.k
    )
    start_state = State(tuple(request.start_volumes))
    target = request.target
    
    tracker = MetricsTracker()
    
    result_path = []
    
    try:
        if request.algorithm == 'ucs':
            path, cost, _ = tracker.wrap_solver(uniform_cost_search, env, start_state, target)
            for action, state in path:
                result_path.append({
                    "action": str(action),
                    "volumes": list(state.volumes)
                })
        elif request.algorithm == 'astar':
            path, cost, _ = tracker.wrap_solver(a_star_search, env, start_state, target)
            for action, state in path:
                result_path.append({
                    "action": str(action),
                    "volumes": list(state.volumes)
                })
        elif request.algorithm == 'bfs':
            path, cost, _ = tracker.wrap_solver(breadth_first_search, env, start_state, target)
            for action, state in path:
                result_path.append({
                    "action": str(action),
                    "volumes": list(state.volumes)
                })
        elif request.algorithm == 'dfs':
            path, cost, _ = tracker.wrap_solver(depth_first_search, env, start_state, target, 50)
            for action, state in path:
                result_path.append({
                    "action": str(action),
                    "volumes": list(state.volumes)
                })
        elif request.algorithm == 'greedy':
            path, cost, _ = tracker.wrap_solver(greedy_best_first_search, env, start_state, target)
            for action, state in path:
                result_path.append({
                    "action": str(action),
                    "volumes": list(state.volumes)
                })
        elif request.algorithm == 'expectimax':
            path, cost, _ = tracker.wrap_solver(expectimax, env, start_state, target, request.expectimax_depth)
            action = path[0] if path else None
            if action:
                next_state, _ = env.apply_action(start_state, action)
                final_state = env.apply_leakage(next_state, 1.0)
                result_path.append({
                    "action": str(action),
                    "volumes": list(final_state.volumes)
                })
        else:
            raise HTTPException(status_code=400, detail="Unknown algorithm")
            
        admissible = check_heuristic_admissibility(env, start_state, target)
        if hasattr(tracker, 'nodes_expanded') and tracker.nodes_expanded == 0:
            tracker.nodes_expanded = 1 # avoid edge bugs visually
            
        return {
            "path": result_path,
            "metrics": {
                "execution_time_ms": tracker.execution_time_ms,
                "peak_memory_kb": tracker.peak_memory_kb,
                "nodes_expanded": tracker.nodes_expanded,
                "effective_branching_factor": tracker.effective_branching_factor,
                "solution_cost": tracker.solution_cost,
                "heuristic_admissible": admissible
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")
