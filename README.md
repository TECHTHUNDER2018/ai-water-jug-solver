# 💧 AI Water Jug Solver

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Three.js](https://img.shields.io/badge/Three.js-r128-black?style=for-the-badge&logo=three.js&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6%2B-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)

**An interactive AI-powered Water Jug Problem solver featuring six classic search algorithms, real-time 3D visualization, and live performance metrics.**

🌐 **[Live Demo → https://ai-water-jug-solver.onrender.com](https://ai-water-jug-solver.onrender.com)**

</div>

---

## 📖 About

The **AI Water Jug Solver** is a full-stack web application that brings the classic Water Jug Problem to life using artificial intelligence search algorithms. The Water Jug Problem is a well-known puzzle in AI and computer science: given jugs of various capacities and a target volume, find the minimum sequence of **Fill**, **Empty**, and **Pour** operations to measure exactly the target amount of water.

This project goes beyond the traditional formulation by introducing:

- **Non-linear stochastic leakage** — water evaporates between steps using the formula `leak = floor(k × √v)`, simulating real-world uncertainty.
- **Configurable action costs** — fill, empty, and pour operations each carry a distinct cost, enabling cost-aware search.
- **Multiple AI algorithms** — compare deterministic, heuristic, and stochastic solvers side-by-side.
- **Live 3D visualization** — watch the jugs animate in real time using WebGL via Three.js and GSAP.
- **Performance analytics** — measure execution time, peak memory, nodes expanded, effective branching factor (b*), and heuristic admissibility for every run.

Whether you are a student learning AI fundamentals, a developer exploring search algorithms, or just curious about the problem, this tool gives you an intuitive, visual way to explore how different algorithms tackle the same problem.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔍 **6 Search Algorithms** | BFS, DFS, UCS (Dijkstra), A\*, Greedy Best-First, and Expectimax |
| 🧊 **3D Jug Visualization** | Interactive WebGL scene powered by Three.js with smooth GSAP animations |
| 💧 **Stochastic Leakage** | Non-linear water loss `floor(k × √v)` between every step |
| ⚖️ **Weighted Action Costs** | Configurable fill, empty, and pour costs for cost-sensitive planning |
| 📊 **Performance Metrics** | Execution time, peak memory (KB), nodes expanded, b* branching factor |
| ✅ **Heuristic Admissibility Check** | Automatically verifies whether the heuristic is admissible (UCS vs A\*) |
| 🎮 **Step-by-Step Playback** | Navigate forward/back or autoplay the solution with a speed slider |
| 📜 **History Log** | Scrollable log showing every action and jug volumes at each step |
| 🛡️ **Input Validation & DoS Protection** | Server-side limits on jug count (≤ 5), jug capacity (≤ 100), and Expectimax depth (≤ 4) |
| 📱 **Responsive UI** | Glassmorphism sidebar layout that works across screen sizes |

---

## 🤖 Algorithms

### Deterministic Search

| Algorithm | Strategy | Optimal? | Complete? | Notes |
|---|---|---|---|---|
| **BFS** | Expand shallowest node first (FIFO queue) | ✅ (unweighted) | ✅ | Finds shortest path by step count |
| **DFS** | Expand deepest node first (LIFO stack) | ❌ | ✅ (depth limit 50) | Memory efficient, not cost-optimal |
| **UCS (Dijkstra)** | Expand lowest-cost node first (min-heap) | ✅ | ✅ | Optimal with weighted actions |
| **A\*** | UCS + admissible heuristic `h(n)` | ✅ | ✅ | Fastest optimal search |
| **Greedy Best-First** | Expand node closest to goal `min|v - target|` | ❌ | ✅ | Fast but suboptimal |

### Stochastic Search

| Algorithm | Strategy | Notes |
|---|---|---|
| **Expectimax** | Minimizes expected cost over probabilistic outcomes | 80% normal leak, 20% double leak per step |

### Heuristic Design

- **A\* heuristic** — Binary admissible heuristic: `h(n) = 0` if any jug holds exactly the target, otherwise `h(n) = 1`. Guarantees admissibility (never overestimates true cost ≥ 1).
- **Greedy heuristic** — `min|v - target|` across all jugs. Non-admissible but guides search aggressively toward the goal.

---

## 🏗️ Project Structure

```
ai-water-jug-solver/
├── backend/
│   ├── __init__.py        # Package init
│   ├── app.py             # FastAPI routes, CORS, input validation, static file serving
│   ├── environment.py     # JugEnvironment, State, Action, leakage model
│   ├── solvers.py         # BFS, DFS, UCS, A*, Greedy, Expectimax implementations
│   └── metrics.py         # MetricsTracker: time, memory, nodes expanded, b* factor
├── frontend/
│   ├── index.html         # Single-page application entry point
│   ├── script.js          # Three.js 3D scene, GSAP animations, API calls, playback
│   └── styles.css         # Glassmorphism UI, dark theme, responsive layout
├── run.py                 # Local dev server entry point (uvicorn)
├── requirements.txt       # Python dependencies
└── README.md
```

---

## 🛠️ Tech Stack

**Backend**
- [Python 3.9+](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/) — high-performance REST API framework
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- [Pydantic](https://docs.pydantic.dev/) — request/response data validation

**Frontend**
- Vanilla JavaScript (ES6+)
- [Three.js r128](https://threejs.org/) — WebGL 3D rendering
- [GSAP 3](https://gsap.com/) — animation library
- [Three.js OrbitControls](https://threejs.org/docs/#examples/en/controls/OrbitControls) — interactive camera
- [Plus Jakarta Sans](https://fonts.google.com/specimen/Plus+Jakarta+Sans) — typography

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9 or higher
- `pip` package manager

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/TECHTHUNDER2018/ai-water-jug-solver.git
cd ai-water-jug-solver

# 2. (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. Install Python dependencies
pip install -r requirements.txt
```

### Running Locally

```bash
python run.py
```

Open your browser and navigate to **http://127.0.0.1:8000**.

The FastAPI backend automatically serves the frontend at the root URL (`/`), so no separate frontend build step is needed.

---

## 🎮 How to Use

1. **Configure Jugs** — Enter jug capacities as a comma-separated list (e.g. `5,7,12`). Up to 5 jugs supported, each up to capacity 100.
2. **Set Starting Volumes** — Enter the initial water level for each jug (e.g. `0,0,0`).
3. **Set Target** — Enter the volume you want to measure in any single jug.
4. **Tune the Leak Constant (k)** — Controls how aggressively water leaks between steps. Higher k = more leakage.
5. **Choose Algorithm** — Select from the six available algorithms in the dropdown.
6. **Run Simulation** — Click **Run Simulation**. The solver computes the optimal (or near-optimal) path and animates it in 3D.
7. **Step Through** — Use **⏮ / ⏭** buttons to step forward or back, or click **▶ Auto Play** for continuous playback. Use the speed slider to control playback rate.
8. **Review Metrics** — Check the Performance Metrics panel for execution stats and heuristic admissibility.
9. **Review History Log** — Scroll the right-hand log panel to see every action and volume state.

---

## 🌐 API Reference

The backend exposes a single REST endpoint.

### `POST /api/solve`

Solves the water jug problem and returns the action path and performance metrics.

**Request Body**

```json
{
  "capacities":       [5, 7],
  "start_volumes":    [0, 0],
  "target":           4,
  "algorithm":        "astar",
  "fill_cost":        3,
  "empty_cost":       1,
  "pour_cost":        2,
  "k":                0.5,
  "expectimax_depth": 3
}
```

| Field | Type | Default | Description |
|---|---|---|---|
| `capacities` | `int[]` | required | Max capacity of each jug (1–100 each, max 5 jugs) |
| `start_volumes` | `int[]` | required | Initial water level for each jug |
| `target` | `int` | required | Target volume to achieve in any jug |
| `algorithm` | `string` | required | One of: `bfs`, `dfs`, `ucs`, `astar`, `greedy`, `expectimax` |
| `fill_cost` | `int` | `3` | Cost to fill a jug to capacity |
| `empty_cost` | `int` | `1` | Cost to empty a jug |
| `pour_cost` | `int` | `2` | Cost to pour between jugs |
| `k` | `float` | `0.5` | Leakage constant for `floor(k × √v)` model |
| `expectimax_depth` | `int` | `3` | Search depth for Expectimax (capped at 4) |

**Response**

```json
{
  "path": [
    { "action": "FILL Jug 0",               "volumes": [5, 0] },
    { "action": "POUR from Jug 0 to Jug 1", "volumes": [0, 5] },
    { "action": "FILL Jug 0",               "volumes": [5, 5] },
    { "action": "POUR from Jug 0 to Jug 1", "volumes": [3, 7] }
  ],
  "metrics": {
    "execution_time_ms":        12.34,
    "peak_memory_kb":           48.0,
    "nodes_expanded":           17,
    "effective_branching_factor": 2.41,
    "solution_cost":            10,
    "heuristic_admissible":     true
  }
}
```

An empty `path` array (`[]`) with `solution_cost: -1` indicates the target is unreachable.

**Error Responses**

| Status | Reason |
|---|---|
| `400` | Invalid input (too many jugs, capacity out of range, mismatched arrays, unknown algorithm) |
| `500` | Internal solver error |

---

## 🔢 Leakage Model

After every action, each jug loses water according to a non-linear square-root leakage formula:

```
v_new = max(0, floor(v - k × multiplier × √v))
```

- For **deterministic algorithms** (BFS, DFS, UCS, A\*, Greedy): `multiplier = 1.0` always.
- For **Expectimax** (stochastic): `multiplier = 1.0` with probability **0.8**, `multiplier = 2.0` with probability **0.2**, modelling environmental uncertainty.

---

## 📊 Performance Metrics Explained

| Metric | Description |
|---|---|
| **Execution Time (ms)** | Wall-clock time from search start to first solution found |
| **Peak Memory (KB)** | Maximum heap memory allocated during the search (via `tracemalloc`) |
| **Nodes Expanded** | Total number of states popped from the frontier and evaluated |
| **b\* Factor** | Effective branching factor — the uniform *b* satisfying `1 + b + b² + … + b^d = N` (nodes expanded at depth *d*). Lower is better. |
| **Solution Cost** | Total weighted action cost of the returned path |
| **Heuristic Admissible** | `true` if A\* cost ≤ UCS cost, confirming the heuristic never overestimates |

---

## 🔒 Server Protections

To prevent denial-of-service and memory exhaustion, the API enforces these hard limits:

- Maximum **5 jugs** per request
- Jug capacity must be between **1 and 100** (inclusive)
- Start volumes must be **≥ 0** and **≤ capacity**
- Expectimax depth is **clamped to [1, 4]** to prevent tree explosion

---

## 📄 License

This project is open-source. See the repository for licensing details.
