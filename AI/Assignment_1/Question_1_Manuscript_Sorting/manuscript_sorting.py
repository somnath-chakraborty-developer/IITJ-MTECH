"""
Manuscript Sorting (8-Puzzle) — AI Assignment Q1
BFS, DFS, Greedy(h1/h2), A*(h1/h2), IDA*(h2), Simulated Annealing, Minimax, Alpha-Beta
"""
import time, math, random, heapq
from collections import deque

# read input.txt: two lines, semicolon-separated rows
def read_input(path="input.txt"):
    with open(path) as f:
        lines = [l.strip() for l in f if l.strip()]
    start = tuple(lines[0].replace(";",""))
    goal  = tuple(lines[1].replace(";",""))
    return start, goal

def blank(s):
    return s.index("B")

def neighbors(state):
    i = blank(state)
    r, c = divmod(i, 3)
    out = []
    for dr, dc, mv in [(-1,0,"U"),(1,0,"D"),(0,-1,"L"),(0,1,"R")]:
        nr, nc = r+dr, c+dc
        if 0 <= nr < 3 and 0 <= nc < 3:
            j = nr*3+nc
            s = list(state)
            s[i], s[j] = s[j], s[i]
            out.append((tuple(s), mv))
    return out

# heuristics
def h1(state, goal):
    return sum(1 for i in range(9) if state[i]!="B" and state[i]!=goal[i])

def h2(state, goal):
    d = 0
    for i in range(9):
        if state[i]!="B":
            j = goal.index(state[i])
            d += abs(i//3 - j//3) + abs(i%3 - j%3)
    return d

# reconstruct path from came_from dict
def path_from(came_from, node):
    moves = []
    while came_from[node][0] is not None:
        prev, mv = came_from[node]
        moves.append(mv)
        node = prev
    moves.reverse()
    return moves

# ---- BFS ----
def bfs(start, goal):
    if start == goal: return True, [], 0, 0.0
    t0 = time.time()
    q = deque([start])
    vis = {start}
    came = {start: (None, None)}
    exp = 0
    while q:
        cur = q.popleft()
        exp += 1
        for nb, mv in neighbors(cur):
            if nb not in vis:
                vis.add(nb)
                came[nb] = (cur, mv)
                if nb == goal:
                    return True, path_from(came, nb), exp, time.time()-t0
                q.append(nb)
    return False, [], exp, time.time()-t0

# ---- DFS ----
def dfs(start, goal, maxd=50):
    if start == goal: return True, [], 0, 0.0
    t0 = time.time()
    stack = [(start, [])]
    vis = {start}
    exp = 0
    while stack:
        cur, path = stack.pop()
        exp += 1
        if len(path) >= maxd:
            continue
        for nb, mv in neighbors(cur):
            if nb not in vis:
                vis.add(nb)
                np = path + [mv]
                if nb == goal:
                    return True, np, exp, time.time()-t0
                stack.append((nb, np))
    return False, [], exp, time.time()-t0

# ---- Greedy Best-First ----
def greedy(start, goal, hfn, hname="h2"):
    if start == goal: return True, [], 0, 0.0
    t0 = time.time()
    ctr = 0
    pq = [(hfn(start,goal), ctr, start)]
    vis = {start}
    came = {start: (None, None)}
    exp = 0
    while pq:
        _, _, cur = heapq.heappop(pq)
        exp += 1
        if cur == goal:
            return True, path_from(came, cur), exp, time.time()-t0
        for nb, mv in neighbors(cur):
            if nb not in vis:
                vis.add(nb)
                came[nb] = (cur, mv)
                ctr += 1
                heapq.heappush(pq, (hfn(nb,goal), ctr, nb))
    return False, [], exp, time.time()-t0

# ---- A* ----
def astar(start, goal, hfn, hname="h2"):
    if start == goal: return True, [], 0, 0.0
    t0 = time.time()
    ctr = 0
    g = {start: 0}
    pq = [(hfn(start,goal), ctr, start)]
    closed = set()
    came = {start: (None, None)}
    exp = 0
    while pq:
        f, _, cur = heapq.heappop(pq)
        if cur == goal:
            return True, path_from(came, cur), exp, time.time()-t0
        if cur in closed:
            continue
        closed.add(cur)
        exp += 1
        for nb, mv in neighbors(cur):
            ng = g[cur] + 1
            if nb not in g or ng < g[nb]:
                g[nb] = ng
                came[nb] = (cur, mv)
                ctr += 1
                heapq.heappush(pq, (ng + hfn(nb,goal), ctr, nb))
    return False, [], exp, time.time()-t0

# ---- IDA* ----
def idastar(start, goal, hfn):
    t0 = time.time()
    total = [0]
    def search(cur, path_set, moves, g, thresh):
        f = g + hfn(cur, goal)
        if f > thresh: return f
        if cur == goal: return "FOUND"
        total[0] += 1
        mn = float("inf")
        for nb, mv in neighbors(cur):
            if nb not in path_set:
                path_set.add(nb)
                moves.append(mv)
                r = search(nb, path_set, moves, g+1, thresh)
                if r == "FOUND": return "FOUND"
                if r < mn: mn = r
                moves.pop()
                path_set.remove(nb)
        return mn
    thresh = hfn(start, goal)
    moves = []
    while True:
        path_set = {start}
        r = search(start, path_set, moves, 0, thresh)
        if r == "FOUND":
            return True, list(moves), total[0], time.time()-t0
        if r == float("inf"):
            return False, [], total[0], time.time()-t0
        thresh = r

# ---- Simulated Annealing ----
def sa(start, goal, hfn, T0=100.0, Tmin=0.01, alpha=0.995, maxiter=100000, restarts=5):
    t0 = time.time()
    total_exp = 0
    for r in range(restarts):
        random.seed(42+r)
        cur = start
        ch = hfn(cur, goal)
        T = T0
        path = []
        for i in range(maxiter):
            if cur == goal:
                params = f"T0={T0}, T_min={Tmin}, exponential"
                return True, path, total_exp, time.time()-t0, params
            total_exp += 1
            nbs = neighbors(cur)
            nxt, mv = random.choice(nbs)
            nh = hfn(nxt, goal)
            delta = nh - ch
            if delta <= 0 or random.random() < math.exp(-delta/T):
                cur = nxt
                ch = nh
                path.append(mv)
            T = max(T * alpha, Tmin)
            if T <= Tmin and ch > 0:
                break
    params = f"T0={T0}, T_min={Tmin}, exponential"
    return cur==goal, path if cur==goal else [], total_exp, time.time()-t0, params

# ---- Minimax / Alpha-Beta ----
def utility(state, goal):
    if state == goal: return 100
    return -h2(state, goal)

def minimax(state, goal, depth, is_max, stats):
    stats[0] += 1
    if state == goal or depth == 0:
        return utility(state, goal), None
    nbs = neighbors(state)
    if is_max:
        best, bmv = float("-inf"), None
        for nb, mv in nbs:
            v, _ = minimax(nb, goal, depth-1, False, stats)
            if v > best: best, bmv = v, mv
        return best, bmv
    else:
        best, bmv = float("inf"), None
        for nb, mv in nbs:
            v, _ = minimax(nb, goal, depth-1, True, stats)
            if v < best: best, bmv = v, mv
        return best, bmv

def alphabeta(state, goal, depth, a, b, is_max, stats):
    stats[0] += 1
    if state == goal or depth == 0:
        return utility(state, goal), None
    nbs = neighbors(state)
    if is_max:
        best, bmv = float("-inf"), None
        for nb, mv in nbs:
            v, _ = alphabeta(nb, goal, depth-1, a, b, False, stats)
            if v > best: best, bmv = v, mv
            a = max(a, best)
            if a >= b:
                stats[1] += 1
                break
        return best, bmv
    else:
        best, bmv = float("inf"), None
        for nb, mv in nbs:
            v, _ = alphabeta(nb, goal, depth-1, a, b, True, stats)
            if v < best: best, bmv = v, mv
            b = min(b, best)
            if a >= b:
                stats[1] += 1
                break
        return best, bmv

# ---- Output ----
def show(name, ok, path, exp, t, hinfo):
    print()
    print("="*60)
    print(f"  {name}")
    print("="*60)
    print(f"  Success:        {ok}")
    print(f"  Heuristic/Params: {hinfo}")
    print(f"  Path:           {path}")
    print(f"  Path length:    {len(path)} moves")
    print(f"  States explored: {exp}")
    print(f"  Time taken:     {t:.4f} s")

# ---- Main ----
def main():
    start, goal = read_input("input.txt")
    print(f"Manuscript Sorting — Start: {start} Goal: {goal}")

    ok, p, e, t = bfs(start, goal)
    show("BFS", ok, p, e, t, "BFS (uninformed)")

    ok, p, e, t = dfs(start, goal, maxd=50)
    show("DFS", ok, p, e, t, "DFS (uninformed)")

    ok, p, e, t = greedy(start, goal, h1, "h1")
    show("Greedy (h1)", ok, p, e, t, "Greedy Best-First (h1 (misplaced))")

    ok, p, e, t = greedy(start, goal, h2, "h2")
    show("Greedy (h2)", ok, p, e, t, "Greedy Best-First (h2 (Manhattan))")

    ok, p, e, t = astar(start, goal, h1, "h1")
    show("A* (h1)", ok, p, e, t, "A* (h1 (misplaced))")

    ok, p, e, t = astar(start, goal, h2, "h2")
    show("A* (h2)", ok, p, e, t, "A* (h2 (Manhattan))")

    ok, p, e, t = idastar(start, goal, h2)
    show("IDA* (h2)", ok, p, e, t, "IDA* (h2 (Manhattan))")

    ok, p, e, t, pr = sa(start, goal, h2)
    show("Simulated Annealing", ok, p, e, t, f"Simulated Annealing ({pr})")

    # Adversarial
    depth = 5
    mm_stats = [0]
    t0 = time.time()
    mm_val, mm_mv = minimax(start, goal, depth, True, mm_stats)
    mm_t = time.time()-t0
    show("Minimax (depth=5)", True, [mm_mv] if mm_mv else [], mm_stats[0], mm_t,
         f"Minimax (depth={depth}, utility=-Manhattan)")

    ab_stats = [0, 0]
    t0 = time.time()
    ab_val, ab_mv = alphabeta(start, goal, depth, float("-inf"), float("inf"), True, ab_stats)
    ab_t = time.time()-t0
    show("Alpha-Beta (depth=5)", True, [ab_mv] if ab_mv else [], ab_stats[0], ab_t,
         f"Alpha-Beta (depth={depth}, utility=-Manhattan)")

if __name__ == "__main__":
    main()
