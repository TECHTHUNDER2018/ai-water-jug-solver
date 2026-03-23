# 💧 AI Water Jug Solver

<div align="center">

![AI Water Jug Solver](https://img.shields.io/badge/AI-Water%20Jug%20Solver-0ea5e9?style=for-the-badge&logo=python&logoColor=white)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-Render-46E3B7?style=for-the-badge&logo=render&logoColor=white)](https://ai-water-jug-solver.onrender.com)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Three.js](https://img.shields.io/badge/Three.js-000000?style=for-the-badge&logo=three.js&logoColor=white)

**An interactive AI-powered solver for the classic Water Jug problem, featuring six search algorithms, real-time 3D visualization, and stochastic (leaky) jug dynamics.**

🌐 **Live App:** [https://ai-water-jug-solver.onrender.com](https://ai-water-jug-solver.onrender.com)

</div>

---

## 📖 About

The **AI Water Jug Solver** is a full-stack web application that brings the classic Water Jug problem to life using Artificial Intelligence. The Water Jug problem is a well-known combinatorial puzzle in AI: given a set of jugs with fixed capacities, a starting configuration of water volumes, and a target volume to measure out, find the sequence of fill, empty, and pour operations that achieves the goal.

This project goes beyond a simple textbook demonstration. It adds:

- **Non-linear leakage dynamics** — water slowly evaporates after each action using the model `v_new = max(0, floor(v - k·√v))`, making the problem a realistic stochastic planning challenge.
- **Six AI search algorithms** — from uninformed search (BFS, DFS) to cost-optimal search (UCS, A\*) and probabilistic planning (Expectimax).
- **Interactive 3D visualization** — Three.js renders jugs as glass cylinders with animated water levels, letting you step through or auto-play the solution path.
- **Live performance metrics** — execution time, peak memory usage, nodes expanded, effective branching factor, solution cost, and heuristic admissibility are reported after every solve.

Whether you are a student learning search algorithms, a teacher demonstrating AI concepts, or just curious about how different algorithms perform on the same problem, this tool provides an intuitive, visual, and quantitative playground.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🔢 **Multi-Jug Support** | Configure 1–5 jugs, each with a capacity of 1–100 units |
| 🎯 **Custom Targets** | Set any target volume to measure out |
| 💧 **Leakage Simulation** | Adjustable leak constant `k` models non-linear water loss after each operation |
| 🤖 **6 AI Algorithms** | BFS, DFS, UCS, A\*, Greedy Best-First, Expectimax |
| 🎲 **Stochastic Transitions** | Expectimax models 80% normal / 20% double leakage per step |
| 📊 **Performance Metrics** | Time, memory, nodes expanded, branching factor, cost, admissibility |
| 🌐 **3D Visualization** | WebGL-rendered jugs with animated water using Three.js |
| ⏯️ **Step-by-Step Playback** | Navigate the solution manually or use auto-play with speed control |
| 📋 **History Log** | Full trace of every action and resulting jug volumes |
| 🛡️ **Server Protections** | Request validation prevents memory exhaustion and tree-explosion DoS |

---

## 🧠 Algorithms

### Uninformed Search

| Algorithm | Strategy | Optimal? | Complete? |
|---|---|---|---|
| **BFS** — Breadth-First Search | Explores level-by-level | ✅ (unit cost) | ✅ |
| **DFS** — Depth-First Search | Explores depth-first (max depth 50) | ❌ | ❌ |

### Informed Search

| Algorithm | Strategy | Optimal? | Complete? |
|---|---|---|---|
| **UCS** — Uniform Cost Search | Expands cheapest node first (Dijkstra) | ✅ | ✅ |
| **A\*** — A-Star Search | `f = g + h`, admissible heuristic | ✅ | ✅ |
| **Greedy** — Greedy Best-First | `f = h` only (volume proximity) | ❌ | ❌ |

### Probabilistic Planning

| Algorithm | Strategy | Notes |
|---|---|---|
| **Expectimax** | Minimizes expected cost over stochastic leakage outcomes | Depth-limited (1–4), returns the single best next action |

#### Heuristic (A\* and Greedy)
- **A\***: Returns `0` if any jug holds the target volume, `1` otherwise (admissible — never overestimates the true remaining cost of `≥1`).
- **Greedy**: Returns `min |v_i − target|` over all jug volumes (non-admissible, more aggressive).

#### Action Costs (defaults, configurable in code)
| Action | Cost |
|---|---|
| Fill a jug to capacity | 3 |
| Empty a jug | 1 |
| Pour between jugs | 2 |

---

## 🏗️ Project Structure

```
ai-water-jug-solver/
├── backend/
│   ├── __init__.py         # Package marker
│   ├── app.py              # FastAPI application & REST API endpoint
│   ├── environment.py      # JugEnvironment, State, Action, leakage model
│   ├── solvers.py          # All six AI search algorithm implementations
│   └── metrics.py          # Performance metrics tracker (time, memory, b*)
├── frontend/
│   ├── index.html          # Single-page application UI
│   ├── script.js           # Three.js 3D scene, API calls, playback controls
│   └── styles.css          # Responsive dark-theme styles
├── requirements.txt        # Python dependencies
├── run.py                  # Local dev entry point (Uvicorn)
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip

### Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/TECHTHUNDER2018/ai-water-jug-solver.git
   cd ai-water-jug-solver
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the development server**

   ```bash
   python run.py
   ```

4. **Open the app**

   Navigate to [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## 🖥️ Usage

1. **Set Jug Capacities** — Enter comma-separated values (e.g., `5,7,12` for three jugs).
2. **Set Start Volumes** — Enter the initial water in each jug (e.g., `0,0,0`).
3. **Set Target** — The volume you want to measure out in any single jug.
4. **Set Leak Constant `k`** — Controls how much water leaks after each step. Set to `0` for no leakage.
5. **Choose Algorithm** — Select one of the six search algorithms from the dropdown.
6. **Click "Run Simulation"** — The backend solves the problem and returns the solution path.
7. **Step through the solution** — Use ⏮ / ⏭ buttons or "Auto Play" to animate the 3D jugs.

---

## 📡 API Reference

### `POST /api/solve`

Solve a water jug problem and return the solution path with performance metrics.

**Request Body** (`application/json`):

```json
{
  "capacities":      [5, 7, 12],
  "start_volumes":   [0, 0, 0],
  "target":          6,
  "algorithm":       "astar",
  "fill_cost":       3,
  "empty_cost":      1,
  "pour_cost":       2,
  "k":               0.5,
  "expectimax_depth": 3
}
```

| Field | Type | Required | Description |
|---|---|---|---|
| `capacities` | `int[]` | ✅ | Capacity of each jug (1–100, max 5 jugs) |
| `start_volumes` | `int[]` | ✅ | Initial water volume in each jug |
| `target` | `int` | ✅ | Target volume to achieve in any jug |
| `algorithm` | `string` | ✅ | One of: `bfs`, `dfs`, `ucs`, `astar`, `greedy`, `expectimax` |
| `fill_cost` | `int` | ❌ | Cost to fill a jug (default: `3`) |
| `empty_cost` | `int` | ❌ | Cost to empty a jug (default: `1`) |
| `pour_cost` | `int` | ❌ | Cost to pour between jugs (default: `2`) |
| `k` | `float` | ❌ | Leakage constant (default: `0.5`) |
| `expectimax_depth` | `int` | ❌ | Search depth for Expectimax (1–4, default: `3`) |

**Response Body**:

```json
{
  "path": [
    { "action": "FILL Jug 1", "volumes": [0, 7, 0] },
    { "action": "POUR from Jug 1 to Jug 0", "volumes": [5, 2, 0] }
  ],
  "metrics": {
    "execution_time_ms": 12.34,
    "peak_memory_kb": 256.0,
    "nodes_expanded": 42,
    "effective_branching_factor": 2.71,
    "solution_cost": 14,
    "heuristic_admissible": true
  }
}
```

**Error Responses**:

| Status | Condition |
|---|---|
| `400` | More than 5 jugs, capacity out of range, negative volumes, volume exceeds capacity, mismatched array lengths, unknown algorithm |
| `500` | Internal solver error |

---

## 🔬 Technical Details

### Leakage Model

After every action, each jug loses water according to:

```
v_new = max(0, floor(v - k · multiplier · √v))
```

where `k` is the user-configurable leak constant and `multiplier` is `1.0` for deterministic algorithms or sampled stochastically (`1.0` with 80% probability, `2.0` with 20% probability) for Expectimax.

### Heuristic Admissibility Check

After every solve, the API automatically runs both UCS and A\* and compares their solution costs. If A\* returns a higher cost than UCS, the heuristic is flagged as non-admissible (`heuristic_admissible: false`).

### Effective Branching Factor (b\*)

Computed via binary search over the polynomial `b + b² + … + b^d = N`, where `N` is the number of nodes expanded and `d` is the solution depth. A value close to `1.0` indicates a highly informed search.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Backend** | Python 3, FastAPI, Uvicorn, Pydantic |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |
| **3D Rendering** | Three.js r128, OrbitControls |
| **Animations** | GSAP 3.12 |
| **Fonts** | Plus Jakarta Sans (Google Fonts) |
| **Hosting** | [Render](https://render.com) |

---

## 🌐 Live Demo

Try the live application here:

**[https://ai-water-jug-solver.onrender.com](https://ai-water-jug-solver.onrender.com)**

> **Note:** The app is hosted on Render's free tier. The server may take 30–60 seconds to wake up after a period of inactivity.

---

## 📄 License

This project is open source. Feel free to use, modify, and distribute it.

---

<div align="center">
  Made with ❤️ by <a href="https://github.com/TECHTHUNDER2018">TECHTHUNDER2018</a>
</div>
