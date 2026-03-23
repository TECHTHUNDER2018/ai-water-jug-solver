import math
from enum import Enum
from typing import Tuple, List, Dict, Optional

class ActionType(Enum):
    FILL = "FILL"
    EMPTY = "EMPTY"
    POUR = "POUR"

class Action:
    def __init__(self, type: ActionType, jug_idx: int, target_jug_idx: Optional[int] = None):
        self.type = type
        self.jug_idx = jug_idx
        self.target_jug_idx = target_jug_idx

    def __str__(self):
        if self.type == ActionType.POUR:
            return f"POUR from Jug {self.jug_idx} to Jug {self.target_jug_idx}"
        return f"{self.type.value} Jug {self.jug_idx}"

class State:
    def __init__(self, volumes: Tuple[int, ...]):
        self.volumes = volumes

    def __hash__(self):
        return hash(self.volumes)

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return self.volumes == other.volumes

    def __lt__(self, other):
        # Used for priority queues when costs are equal
        return self.volumes < other.volumes

    def __str__(self):
        return str(self.volumes)

    def __repr__(self):
        return f"State({self.volumes})"

class JugEnvironment:
    def __init__(self, capacities: Tuple[int, ...], fill_cost: int = 3, empty_cost: int = 1, pour_cost: int = 2, k: float = 0.5):
        self.capacities = capacities
        self.num_jugs = len(capacities)
        self.fill_cost = fill_cost
        self.empty_cost = empty_cost
        self.pour_cost = pour_cost
        self.k = k # Leakage constant

    def get_actions(self, state: State) -> List[Action]:
        actions = []
        for i in range(self.num_jugs):
            # Can Fill
            if state.volumes[i] < self.capacities[i]:
                actions.append(Action(ActionType.FILL, i))
            # Can Empty
            if state.volumes[i] > 0:
                actions.append(Action(ActionType.EMPTY, i))
                # Can Pour
                for j in range(self.num_jugs):
                    if i != j and state.volumes[j] < self.capacities[j]:
                        actions.append(Action(ActionType.POUR, i, j))
        return actions

    def apply_action(self, state: State, action: Action) -> Tuple[State, int]:
        # Apply action without leakage first
        new_volumes = list(state.volumes)
        cost = 0

        if action.type == ActionType.FILL:
            new_volumes[action.jug_idx] = self.capacities[action.jug_idx]
            cost = self.fill_cost
        elif action.type == ActionType.EMPTY:
            new_volumes[action.jug_idx] = 0
            cost = self.empty_cost
        elif action.type == ActionType.POUR:
            assert action.target_jug_idx is not None
            pour_amount = min(new_volumes[action.jug_idx], self.capacities[action.target_jug_idx] - new_volumes[action.target_jug_idx])
            new_volumes[action.jug_idx] -= pour_amount
            new_volumes[action.target_jug_idx] += pour_amount
            cost = self.pour_cost

        return State(tuple(new_volumes)), cost

    def apply_leakage(self, state: State, multiplier: float = 1.0) -> State:
        # Non-linear leakage: v_{t+1} = max(0, floor(v_t - (k * multiplier * sqrt(v_t))))
        new_volumes = []
        for v in state.volumes:
            leak_amount = math.floor(self.k * multiplier * math.sqrt(v))
            new_volumes.append(max(0, v - leak_amount))
        return State(tuple(new_volumes))

    def get_successors(self, state: State) -> List[Tuple[Action, State, int]]:
        successors = []
        for action in self.get_actions(state):
            # Deterministic transition (with normal leakage)
            intermediate_state, cost = self.apply_action(state, action)
            final_state = self.apply_leakage(intermediate_state, multiplier=1.0)
            successors.append((action, final_state, cost))
        return successors

    def get_stochastic_successors(self, state: State) -> List[Tuple[Action, List[Tuple[State, float, int]]]]:
        # Returns [Action, [(NextState1, Prob1, Cost), (NextState2, Prob2, Cost)]]
        successors = []
        for action in self.get_actions(state):
            intermediate_state, cost = self.apply_action(state, action)
            
            # 80% normal leak, 20% double leak
            state_normal = self.apply_leakage(intermediate_state, multiplier=1.0)
            state_double = self.apply_leakage(intermediate_state, multiplier=2.0)
            
            # Combine probabilities if multiple branches lead to the same resulting states
            outcomes = {}
            outcomes[state_normal] = outcomes.get(state_normal, 0.0) + 0.8
            outcomes[state_double] = outcomes.get(state_double, 0.0) + 0.2
            
            stochastic_outcomes = [(s, p, cost) for s, p in outcomes.items()]
            successors.append((action, stochastic_outcomes))
            
        return successors
