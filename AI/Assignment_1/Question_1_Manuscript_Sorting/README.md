# Question 1 — Manuscript Sorting (8-Puzzle)

## Problem
Given a 3×3 grid with 8 manuscript pages and one blank slot, rearrange from a start configuration to a goal configuration using various search algorithms.

## Algorithms Implemented
| Algorithm | Type |
|-----------|------|
| BFS | Uninformed |
| DFS | Uninformed |
| Greedy Best-First (h1) | Informed — Misplaced tiles |
| Greedy Best-First (h2) | Informed — Manhattan distance |
| A* (h1) | Informed — Misplaced tiles |
| A* (h2) | Informed — Manhattan distance |
| IDA* (h2) | Informed — Manhattan distance |
| Simulated Annealing | Local Search |
| Minimax (depth=5) | Adversarial |
| Alpha-Beta Pruning (depth=5) | Adversarial |

## Heuristics
- **h1** — Number of misplaced tiles (excludes blank)
- **h2** — Sum of Manhattan distances of each tile to its goal position

## Input Format (`input.txt`)
Two lines, semicolon-separated rows representing the 3×3 grid. Use `B` for the blank tile.
```
123;B46;758
123;456;7B8
```
- Line 1: Start state
- Line 2: Goal state

## How to Run
```bash
python manuscript_sorting.py
```

## Output
Each algorithm prints: success status, path of moves (U/D/L/R), path length, states explored, and time taken.
