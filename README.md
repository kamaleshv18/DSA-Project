# DSA TRAFFIC RACER — DSA THEORY GAME

**Academic Course:** Data Structures and Algorithms (DSA) Theory  
**Target Audience:** First-Year M.Tech Software Engineering / B.Tech Computer Science  
**Demonstration:** 5–10 Minute Viva & College Project Evaluation

---

## 1. Project Title
**DSA TRAFFIC RACER: A Real-Time Algorithmically Driven 2D Urban Simulation & Racing Game**

---

## 2. Problem Statement
Traditional computer science education often teaches Data Structures and Algorithms (DSA) purely through abstract pseudocode, dry command-line text programs, or synthetic LeetCode-style puzzles. Students struggle to visualize how fundamental concepts—such as Queues, Stacks, Priority Queues, Graphs, Breadth-First Search (BFS), and Dijkstra's Algorithm—operate in real-time software systems like autonomous traffic controllers, GPS navigators, undo buffers, and dispatch schedulers.

**DSA Traffic Racer** bridges this gap by directly embedding these core DSA primitives into the operational mechanics of a 2D top-down car racing game, offering an interactive, visual, and demonstrably rigorous software engineering project.

---

## 3. Objectives
1. **Genuine Algorithmic Integration:** Ensure data structures are not passive comments or cosmetic labels, but actively compute and govern game mechanics (traffic dispatching, movement history, routing, leaderboard sorting).
2. **Custom DSA Implementations:** Develop custom, transparent Python classes for `Queue`, `Stack`, `PriorityQueue`, `Graph`, `BFS`, `Dijkstra`, and `Sorting` without leaning on black-box external abstractions.
3. **Dedicated DSA Visualizer Section:** Provide an interactive educational workbench where students and evaluators can step forward/backward through algorithmic execution states (queue enqueue/dequeue, min-heap sift-up/sift-down, BFS frontier expansion, Dijkstra edge relaxation, Merge Sort division).
4. **Viva-Ready Demonstrability:** Deliver a 5–10 minute presentation workflow allowing students to answer questions on Big-O time and space complexity with visual evidence.
5. **Robust, Zero-Dependency Execution:** Build a lightweight, object-oriented application using Python 3 and Pygame with procedural sound synthesis and geometric rendering that runs out-of-the-box on standard laptops.

---

## 4. Game Description
In **DSA Traffic Racer**, the player navigates an aerodynamic sports vehicle through a bustling metropolitan road grid across 5 progressively challenging academic levels:
- **Level 1 — Highway:** Basic highway driving with FIFO queue traffic management at highway toll choke-points.
- **Level 2 — City Traffic:** Multi-lane road intersections modeled as Graph nodes where traffic streams queue in arrival order.
- **Level 3 — Emergency Traffic:** High-speed ambulances and police cruisers dispatch through intersections with strict precedence via a Min-Heap Priority Queue.
- **Level 4 — Route Challenge:** Multi-path urban road graph where Breadth-First Search (BFS) calculates the shortest route by hop count.
- **Level 5 — Smart Navigation:** Real-world weighted road network with distance and congestion penalties navigated via Dijkstra's shortest-path algorithm to reach Silicon Tech Park.

Players can collect data packets (+50 score) and health repair kits (+25 health), pass checkpoints (+100 score), use the **DSA Stack Undo ('U' Key)** to rewind recent moves, and press **'M'** to inspect the live City Road Network Graph.

---

## 5. Technologies Used
- **Programming Language:** Python 3 (Python 3.10 - 3.14+)
- **Game Engine & Graphics:** Pygame / Pygame-CE (Community Edition)
- **Architecture:** Object-Oriented Design (OOP), Separation of Concerns (DSA Layer vs. Engine Layer)
- **Audio:** Procedural PCM sound synthesis using standard Python `math` and `struct` (no external audio files required)
- **Persistence:** JSON-based leaderboard storage
- **Testing:** Python `unittest` framework with 100% automated test coverage

---

## 6. DSA Concepts Used

| Game Feature | Data Structure | Algorithm | Role & Justification |
| :--- | :--- | :--- | :--- |
| **Highway Traffic Flow** | `Queue` | FIFO (First-In First-Out) | Normal civilian cars are processed and cleared in arrival order |
| **Movement Undo Buffer** | `Stack` | LIFO (Last-In First-Out) | Player position & speed snapshots push on top; pressing 'U' pops recent state |
| **Emergency Clearance** | `PriorityQueue` | Min-Heap (Sift-Up / Down) | Ambulance (Rank 1) and Police (Rank 2) overtake civilian traffic (Rank 3) |
| **Metropolitan Road Map** | `Graph` | Adjacency List `O(V + E)` | Models 8 landmark vertices and weighted bidirectional road edges |
| **Unweighted Navigation** | `Queue` + `Graph` | Breadth-First Search (BFS) | Discovers route with minimum number of road intersections/hops |
| **Intelligent GPS Nav** | `Min-Heap` + `Graph` | Dijkstra's Algorithm | Solves single-source shortest path minimizing travel time & distance weights |
| **High Score Leaderboard**| Array | Merge Sort / Quick Sort | Sorts high scores descending in `O(N log N)` time |
| **Landmark Directory** | Array | Binary Search | Divides-and-conquers sorted landmark list in `O(log N)` |

---

## 7. Data Structures Implemented

### 1. Custom Queue (`dsa/queue.py`)
- **Operations:** `enqueue(item)`, `dequeue()`, `peek()`, `is_empty()`, `size()`, `clear()`, `get_items()`
- **Implementation:** Uses a list with a floating front index pointer and periodic compaction. Guarantees amortized **O(1)** dequeue time (unlike standard `list.pop(0)` which is O(N)).

### 2. Custom Stack (`dsa/stack.py`)
- **Operations:** `push(item)`, `pop()`, `peek()`, `is_empty()`, `size()`, `clear()`, `get_items()`
- **Implementation:** Clean LIFO container with bounded capacity for memory safety in real-time games. **O(1)** time for push and pop.

### 3. Custom Priority Queue (`dsa/priority_queue.py`)
- **Operations:** `enqueue(item, priority)`, `dequeue()`, `peek()`, `peek_priority()`, `is_empty()`, `size()`
- **Implementation:** Custom binary min-heap implemented from scratch featuring `_sift_up` and `_sift_down` methods. Includes arrival sequence tie-breakers to maintain stable FIFO ordering among equal-priority vehicles. Guaranteed **O(log N)** enqueue and dequeue.

### 4. Graph Adjacency List (`dsa/graph.py`)
- **Operations:** `add_node(id, name, x, y, type)`, `add_edge(u, v, weight, name)`, `get_neighbors(node_id)`, `get_edge_weight(u, v)`, `get_all_edges()`
- **Implementation:** Stores vertices in a dictionary and edges in adjacency lists. Space complexity is **O(V + E)**.

---

## 8. Algorithms Implemented

### 1. Breadth-First Search (`dsa/bfs.py`)
- Explores graph level-by-level using our custom `Queue`.
- Records full execution history steps (visited set, current queue, parent pointers) for step-by-step rendering in the DSA Visualizer.

### 2. Dijkstra's Shortest Path (`dsa/dijkstra.py`)
- Maintains a tentative distance table and greedy frontier backed by our custom `PriorityQueue`.
- Relaxes edges `dist[u] + weight(u, v) < dist[v]` and reconstructs the minimum-cost route.

### 3. Merge Sort & Quick Sort (`dsa/sorting.py`)
- **Merge Sort:** Classic divide-and-conquer splitting list into halves and merging sorted halves in `O(N log N)`. Stable.
- **Quick Sort:** In-place partitioning around a median pivot.
- Includes `merge_sort_trace()` which produces animation snapshots for the visualizer.

### 4. Searching (`dsa/searching.py`)
- **Linear Search:** Sequential inspection for dynamic traffic objects in `O(N)`.
- **Binary Search:** Interval-halving search on sorted landmark arrays in `O(log N)`.

---

## 9. Game Flow Architecture

```
                       +-----------------------+
                       |       MAIN MENU       |
                       +-----------------------+
                                   |
         +-----------------+-------+-------+-----------------+
         |                 |               |                 |
         v                 v               v                 v
   [ START GAME ]    [ VISUALIZER ]  [ LEADERBOARD ]   [ HOW TO PLAY ]
         |                 |               |                 |
         v                 v               v                 v
   +-----------+     +-----------+   +-----------+     +-----------+
   |  Level 1  |     |   Queue   |   |Merge Sort |     | Controls  |
   |  Level 2  |     |   Stack   |   |   vs      |     |  Powerups |
   |  Level 3  |     |   PQ      |   |Quick Sort |     |  Chrono   |
   |  Level 4  |     |   BFS     |   +-----------+     |  Rewind   |
   |  Level 5  |     | Dijkstra  |                     +-----------+
   +-----------+     |  Sorting  |
         |           +-----------+
         +-----> [ PAUSE ] / [ GAME OVER ] / [ VICTORY ]
```

---

## 10. Project Structure
```
DSA_Traffic_Racer/
├── main.py                     # Game launcher, event dispatcher & main loop
├── requirements.txt            # Dependency specification (pygame-ce)
├── README.md                   # Full documentation & viva reference
│
├── game/                       # Game Engine & Gameplay Systems
│   ├── __init__.py             # Game package exposure
│   ├── config.py               # Constants, screen resolution, RGB palettes
│   ├── player.py               # Player sports car & Stack movement undo
│   ├── traffic.py              # Civilian/emergency cars & Queue/PQ management
│   ├── road.py                 # Highway scrolling, lane dashes, checkpoints, coins
│   ├── collision.py            # Bounding box detection & spark particle fx
│   ├── level.py                # 5 academic levels & progression objectives
│   ├── city_map.py             # 8-landmark city graph & topological map overlay
│   ├── visualizer.py           # Interactive step-by-step DSA workbench
│   ├── ui.py                   # HUD, menus, leaderboard, complexity screens
│   └── sound_manager.py        # Procedural PCM audio synthesizer
│
├── dsa/                        # Core Data Structures & Algorithms
│   ├── __init__.py             # DSA module exports
│   ├── queue.py                # Custom FIFO Queue
│   ├── stack.py                # Custom LIFO Stack
│   ├── priority_queue.py       # Custom Min-Heap Priority Queue
│   ├── graph.py                # Adjacency List Graph
│   ├── bfs.py                  # Breadth-First Search shortest path
│   ├── dijkstra.py             # Dijkstra minimum-weight shortest path
│   ├── sorting.py              # Merge Sort and Quick Sort
│   └── searching.py            # Linear and Binary search
│
├── assets/                     # Asset directory for optional custom media
│   ├── images/
│   └── sounds/
│
└── tests/                      # Automated Test Suite (100% Pass)
    ├── __init__.py
    ├── test_queue.py           # Unit tests for Queue FIFO logic
    ├── test_stack.py           # Unit tests for Stack LIFO logic
    ├── test_priority_queue.py  # Unit tests for Min-Heap prioritization
    ├── test_graph.py           # Unit tests for Adjacency List
    ├── test_algorithms.py      # Tests for BFS, Dijkstra, Sorts, Searches
    └── test_gameplay.py        # Headless integration tests for all levels
```

---

## 11. Installation Instructions

### Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14+ installed.

### Setup Steps
1. Open PowerShell or Command Prompt.
2. Navigate to the project directory:
   ```powershell
   cd C:\Users\kamal\.gemini\antigravity\scratch\DSA_Traffic_Racer
   ```
3. Install required packages:
   ```powershell
   py -m pip install -r requirements.txt
   ```
   *(Note: `pygame-ce` is installed automatically, ensuring full compatibility with Python 3.14.)*

---

## 12. How to Run

### Run the Playable Game
```powershell
py main.py
```

### Run the Automated Test Suite (29 Tests)
```powershell
py -m unittest discover tests -v
```

### Run Headless Verification (for automated validation)
```powershell
py main.py --headless --test-run
```

---

## 13. Controls
- **W / Up Arrow:** Accelerate forward (increase speed)
- **S / Down Arrow:** Brake / Reverse (slow down)
- **A / Left Arrow:** Steer left across lanes
- **D / Right Arrow:** Steer right across lanes
- **U Key:** **UNDO MOVEMENT** (Pops recent snapshot from DSA Stack)
- **M Key:** Toggle Fullscreen City Road Map & Navigation Overlay
- **P Key / ESC:** Pause / Unpause game
- **R Key:** Quick restart current level

---

## 14. Complexity Analysis Reference

| Structure / Algorithm | Time (Best) | Time (Average) | Time (Worst) | Space | Viva Explanation |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Queue** | $O(1)$ | $O(1)$ | $O(1)$ amortized | $O(N)$ | Front-pointer index prevents $O(N)$ array shifting |
| **Stack** | $O(1)$ | $O(1)$ | $O(1)$ | $O(N)$ | Top pointer enables instant push and pop snapshots |
| **Priority Queue** | $O(1)$ peek | $O(\log N)$ | $O(\log N)$ | $O(N)$ | Binary min-heap keeps smallest priority number at root |
| **Graph (Adj List)** | $O(1)$ add node | $O(V + E)$ | $O(V + E)$ | $O(V + E)$ | Efficient for sparse road grids where $E \ll V^2$ |
| **BFS** | $O(V + E)$ | $O(V + E)$ | $O(V + E)$ | $O(V)$ | Optimal for unweighted graphs (hop count) |
| **Dijkstra** | $O((V+E)\log V)$ | $O((V+E)\log V)$ | $O((V+E)\log V)$ | $O(V)$ | Greedy relaxation using Min-Heap priority queue |
| **Merge Sort** | $O(N \log N)$ | $O(N \log N)$ | $O(N \log N)$ | $O(N)$ | Guaranteed $O(N \log N)$ stable divide-and-conquer |
| **Quick Sort** | $O(N \log N)$ | $O(N \log N)$ | $O(N^2)$ | $O(\log N)$ | In-place partitioning; median pivot avoids worst-case |
| **Binary Search** | $O(1)$ | $O(\log N)$ | $O(\log N)$ | $O(1)$ | Halves candidate space each iteration on sorted list |

---

## 15. College Viva Demonstration Guide (5–10 Minutes)

Follow this script to demonstrate the project to professors and evaluators:

1. **Introduction (1 Min):**
   - Launch `py main.py`. Point out the clean academic interface.
   - Click **COMPLEXITY ANALYSIS** to show the evaluators the complete Big-O table covering all structures.

2. **Demonstrate Interactive DSA Visualizer (3 Mins):**
   - Click **DSA VISUALIZER** from the Main Menu.
   - **Queue Tab:** Click `+ Enqueue Car` and `- Dequeue (FIFO)`. Explain how vehicles move in arrival order.
   - **Stack Tab:** Click `+ Push Action` and `- Pop Undo (LIFO)`. Explain the LIFO stack pointer.
   - **Priority Queue Tab:** Click `+ Ambulance (P1)` and `Dispatch Next`. Show how the Ambulance bypasses civil cars due to min-heap ordering.
   - **BFS & Dijkstra Tabs:** Click `Next Step >` or `Auto Play` to demonstrate step-by-step node exploration and tentative distance relaxation on the city road graph.
   - **Sorting Tab:** Step through Merge Sort dividing and merging high scores.

3. **Demonstrate Real-Time Gameplay (3 Mins):**
   - Return to Menu and click **START GAME**.
   - **Level 1 (Queue):** Drive forward using W/A/S/D. Point to the HUD showing the active traffic queue.
   - **Demonstrate Stack Undo:** Collide with a car or make a turn, then press **'U'**. Show the evaluator how the car position rewinds instantly via `Stack.pop()`.
   - **Level 3 (Priority Queue):** Point to emergency vehicles overtaking normal traffic.
   - **Level 4 & 5 (BFS & Dijkstra):** Press **'M'** to expand the City Road Map. Explain how Dijkstra calculates the green route to Silicon Tech Park minimizing road travel weights.

4. **Leaderboard & Code Inspection (2 Mins):**
   - Show the Leaderboard and click **Switch to Quick Sort / Merge Sort** to demonstrate both sorting algorithms.
   - Show the modular codebase (`dsa/` and `game/`) and run `py -m unittest discover tests -v` to prove all 29 automated tests pass.

---

## 16. Future Enhancements
- Addition of A* (A-Star) heuristic navigation algorithm with Euclidean distance weighting.
- Dynamic road traffic blockages triggering real-time Dijkstra path recalculations.
- Graphical texture pack and day/night atmospheric weather cycles.

---

## 17. Conclusion
**DSA Traffic Racer** successfully proves that academic Data Structures and Algorithms can be organically unified with engaging, real-time gameplay. By cleanly separating the theoretical algorithmic layer (`dsa/`) from the game presentation layer (`game/`), the project serves as an ideal software engineering showcase for M.Tech/B.Tech academic presentations and viva examinations.
