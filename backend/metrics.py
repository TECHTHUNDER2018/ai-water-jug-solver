import time
import tracemalloc
from typing import Callable, Any

class MetricsTracker:
    def __init__(self):
        self.execution_time_ms = 0.0
        self.peak_memory_kb = 0.0
        self.nodes_expanded = 0
        self.effective_branching_factor = 0.0
        self.solution_cost = 0

    def wrap_solver(self, solver_func: Callable, *args, **kwargs) -> Any:
        tracemalloc.start()
        start_time = time.perf_counter()
        
        result = solver_func(*args, **kwargs)
        
        end_time = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        self.execution_time_ms = (end_time - start_time) * 1000
        self.peak_memory_kb = peak / 1024
        
        if len(result) >= 3:
            path, cost, nodes_expanded = result[:3]
            self.nodes_expanded = nodes_expanded
            self.solution_cost = cost
            depth = len(path) if isinstance(path, list) else 0
            self.effective_branching_factor = self._calculate_b_star(nodes_expanded, depth)
            
        return result

    def _calculate_b_star(self, n: int, d: int, epsilon: float = 0.01) -> float:
        if d <= 0 or n <= 1:
            return 1.0
        
        low = 1.0
        high = float(n)
        
        def polynomial(b: float, d: int) -> float:
            if b == 1.0:
                return float(d)
            return (b**(d+1) - 1) / (b - 1) - 1
            
        while high - low > epsilon:
            mid = (low + high) / 2
            val = polynomial(mid, d)
            if val > n:
                high = mid
            else:
                low = mid
        return (low + high) / 2
