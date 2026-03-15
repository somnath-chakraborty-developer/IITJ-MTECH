# Question 2 — Security Bot Scheduling (CSP)

## Problem
Schedule security bots across shifts using Constraint Satisfaction Problem (CSP) techniques. Each shift must be assigned a bot such that no two consecutive shifts use the same bot, all bots are used at least once, and certain unary constraints are respected.

## Algorithms Implemented
| Algorithm | Description |
|-----------|-------------|
| Plain Backtracking | Basic recursive backtracking |
| Backtracking + MRV | Minimum Remaining Values heuristic (fail-first) |
| Backtracking + MRV + Forward Checking | MRV with domain pruning after each assignment |
| AC-3 + MRV + Forward Checking | Arc Consistency preprocessing before search |

## Constraints
- **No-Back-to-Back**: Adjacent slots cannot have the same bot
- **All-Bots-Used**: Every bot in the domain must appear at least once
- **Unary constraints**: Specific bots excluded from specific slots (e.g., `Slot4 != C`)

## Input Format (`input.txt`)
```
DOMAIN: A, B, C
VARIABLES: Slot1, Slot2, Slot3, Slot4
CONSTRAINT: NO_CONSECUTIVE
UNARY: Slot4 != C
CONSTRAINT: ALL_BOTS_USED
```

## How to Run
```bash
python q2_security_bot_csp.py
```

## Output
Each method prints: success/failure, heuristic used, inference method, final assignment, total assignments, backtracks, and time taken. A performance summary table is printed at the end.
