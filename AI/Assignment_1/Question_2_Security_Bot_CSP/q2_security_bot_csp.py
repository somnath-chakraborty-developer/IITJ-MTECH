"""
Security Bot Scheduling — CSP
AI Assignment 1 — Question 2
Backtracking, MRV, Forward Checking, AC-3
"""
import time
from copy import deepcopy

# ---- Parse input.txt ----
def parse_input(path="input.txt"):
    variables, domain, unary = [], [], []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("VARIABLES:"):
                variables = [v.strip() for v in line.split(":")[1].split(",")]
            elif line.startswith("DOMAIN:"):
                domain = [d.strip() for d in line.split(":")[1].split(",")]
            elif line.startswith("UNARY:"):
                parts = line.split(":")[1].strip().split("!=")
                unary.append((parts[0].strip(), parts[1].strip()))
    return variables, domain, unary

# ---- CSP setup ----
def make_csp(variables, base_domain, unary):
    domains = {v: list(base_domain) for v in variables}
    for var, val in unary:
        if var in domains and val in domains[var]:
            domains[var].remove(val)
    binary = [(variables[i], variables[i+1]) for i in range(len(variables)-1)]
    nbrs = {v: [] for v in variables}
    for a, b in binary:
        nbrs[a].append(b)
        nbrs[b].append(a)
    return domains, binary, nbrs, set(base_domain)

def consistent(assign, var, val, nbrs):
    for nb in nbrs[var]:
        if nb in assign and assign[nb] == val:
            return False
    return True

def all_bots_check(assign, all_bots, variables):
    if len(assign) < len(variables):
        return True
    return all_bots.issubset(set(assign.values()))

# ---- 1. Plain Backtracking ----
def backtrack_plain(variables, domains, nbrs, all_bots):
    stats = {"assigns": 0, "backtracks": 0}
    t0 = time.time()
    def solve(assign, idx):
        if idx == len(variables):
            if all_bots.issubset(set(assign.values())):
                return dict(assign)
            return None
        var = variables[idx]
        for val in domains[var]:
            stats["assigns"] += 1
            if consistent(assign, var, val, nbrs):
                assign[var] = val
                r = solve(assign, idx+1)
                if r: return r
                del assign[var]
                stats["backtracks"] += 1
        return None
    sol = solve({}, 0)
    return sol, stats, time.time()-t0

# ---- 2. Backtracking + MRV ----
def pick_mrv(unassigned, domains):
    return min(unassigned, key=lambda v: len(domains[v]))

def backtrack_mrv(variables, domains, nbrs, all_bots):
    stats = {"assigns": 0, "backtracks": 0}
    t0 = time.time()
    def solve(assign, remaining):
        if not remaining:
            if all_bots.issubset(set(assign.values())):
                return dict(assign)
            return None
        var = pick_mrv(remaining, domains)
        rest = [v for v in remaining if v != var]
        for val in domains[var]:
            stats["assigns"] += 1
            if consistent(assign, var, val, nbrs):
                assign[var] = val
                r = solve(assign, rest)
                if r: return r
                del assign[var]
                stats["backtracks"] += 1
        return None
    sol = solve({}, list(variables))
    return sol, stats, time.time()-t0

# ---- 3. Backtracking + MRV + Forward Checking ----
def forward_check(var, val, domains, nbrs):
    pruned = []
    for nb in nbrs[var]:
        if val in domains[nb]:
            domains[nb].remove(val)
            pruned.append((nb, val))
            if not domains[nb]:
                return pruned, True
    return pruned, False

def undo_fc(pruned, domains):
    for nb, val in pruned:
        domains[nb].append(val)

def backtrack_mrv_fc(variables, domains, nbrs, all_bots):
    stats = {"assigns": 0, "backtracks": 0, "prunes": 0}
    t0 = time.time()
    doms = deepcopy(domains)
    def solve(assign, remaining):
        if not remaining:
            if all_bots.issubset(set(assign.values())):
                return dict(assign)
            return None
        var = pick_mrv(remaining, doms)
        rest = [v for v in remaining if v != var]
        for val in list(doms[var]):
            stats["assigns"] += 1
            if consistent(assign, var, val, nbrs):
                assign[var] = val
                pruned, wipeout = forward_check(var, val, doms, nbrs)
                stats["prunes"] += len(pruned)
                if not wipeout:
                    r = solve(assign, rest)
                    if r: return r
                undo_fc(pruned, doms)
                del assign[var]
                stats["backtracks"] += 1
        return None
    sol = solve({}, list(variables))
    return sol, stats, time.time()-t0

# ---- 4. AC-3 ----
def ac3(domains, binary):
    doms = deepcopy(domains)
    queue = []
    for xi, xj in binary:
        queue.append((xi, xj))
        queue.append((xj, xi))
    removed = []
    while queue:
        xi, xj = queue.pop(0)
        to_rm = []
        for vi in list(doms[xi]):
            if not any(vi != vj for vj in doms[xj]):
                to_rm.append(vi)
        if to_rm:
            for v in to_rm:
                doms[xi].remove(v)
                removed.append((xi, v))
            if not doms[xi]:
                return doms, False, removed
            for xk, xl in binary:
                if xl == xi and xk != xj:
                    queue.append((xk, xi))
                if xk == xi and xl != xj:
                    queue.append((xl, xi))
    return doms, True, removed

# ---- 5. Find all solutions ----
def find_all(variables, domains, nbrs, all_bots):
    results = []
    def solve(assign, idx):
        if idx == len(variables):
            if all_bots.issubset(set(assign.values())):
                results.append(dict(assign))
            return
        var = variables[idx]
        for val in domains[var]:
            if consistent(assign, var, val, nbrs):
                assign[var] = val
                solve(assign, idx+1)
                del assign[var]
    solve({}, 0)
    return results

# ---- Output (matches assignment spec) ----
def show_schedule(sol, variables):
    hdr = "    +" + "+".join(["--------"]*len(variables)) + "+"
    print(hdr)
    print("    |" + "|".join(f" {v:^6} " for v in variables) + "|")
    print(hdr)
    print("    |" + "|".join(f" Bot {sol[v]:^3}" for v in variables) + "|")
    print(hdr)

def show_result(name, sol, stats, t, variables, constraints, heur="None", infer="None"):
    print()
    print("=" * 60)
    print(f"  {name}")
    print("=" * 60)
    print(f"  Success/Failure:    {'SUCCESS' if sol else 'FAILURE'}")
    print(f"  Heuristic:          {heur}")
    print(f"  Inference:          {infer}")
    print(f"  Constraints:        {constraints}")
    print(f"  Final Assignment:   {sol}")
    print(f"  Total Assignments:  {stats['assigns']}")
    print(f"  Total Backtracks:   {stats['backtracks']}")
    if "prunes" in stats:
        print(f"  FC Prunes:          {stats['prunes']}")
    print(f"  Time Taken:         {t:.6f} s")
    if sol:
        print()
        show_schedule(sol, variables)

# ---- Main ----
def main():
    variables, base_domain, unary = parse_input("input.txt")
    domains, binary, nbrs, all_bots = make_csp(variables, base_domain, unary)

    constraints_str = "No-Back-to-Back"
    for var, val in unary:
        constraints_str += f", {var}!={val}"
    constraints_str += ", All-Bots-Used"

    print()
    print("=" * 60)
    print("  SECURITY BOT SCHEDULING — CSP")
    print("=" * 60)
    print(f"  Bots (Domain):  {base_domain}")
    print(f"  Shifts (Vars):  {variables}")
    print(f"  Domains:        {domains}")
    print(f"  Binary arcs:    {binary}")
    for var, val in unary:
        print(f"  Unary:          {var} != {val}")
    print(f"  Constraints:    {constraints_str}")

    # 1. Plain backtracking
    sol, stats, t = backtrack_plain(variables, domains, nbrs, all_bots)
    show_result("Plain Backtracking", sol, stats, t, variables, constraints_str)

    # 2. MRV
    sol, stats, t = backtrack_mrv(variables, domains, nbrs, all_bots)
    show_result("Backtracking + MRV", sol, stats, t, variables, constraints_str,
                heur="MRV (fail-first)", infer="Consistency check")

    # 3. MRV + FC
    sol, stats, t = backtrack_mrv_fc(variables, domains, nbrs, all_bots)
    show_result("Backtracking + MRV + Forward Checking", sol, stats, t, variables,
                constraints_str, heur="MRV", infer="Forward Checking")

    # 4. AC-3 preprocessing
    ac3_doms, ok, removed = ac3(domains, binary)
    print(f"\n  --- AC-3 Preprocessing ---")
    print(f"  Consistent: {ok}")
    print(f"  Domains after AC-3: {ac3_doms}")
    if removed:
        print(f"  Removed: {removed}")
    else:
        print(f"  No pruning — all arcs already consistent.")

    if ok:
        sol, stats, t = backtrack_mrv_fc(variables, ac3_doms, nbrs, all_bots)
        show_result("AC-3 + MRV + Forward Checking", sol, stats, t, variables,
                    constraints_str, heur="MRV", infer="AC-3 + Forward Checking")

    # All solutions
    all_sols = find_all(variables, domains, nbrs, all_bots)
    print(f"\n  Total valid solutions: {len(all_sols)}")
    for i, s in enumerate(all_sols, 1):
        print(f"  #{i}: {s}")
        show_schedule(s, variables)
        print()

    # Performance summary
    print("=" * 60)
    print("  PERFORMANCE SUMMARY")
    print("=" * 60)
    print(f"  {'Method':<35} {'Assigns':<10} {'Backtracks':<12} {'Time(s)':<10}")
    print("  " + "-" * 67)
    s1, st1, t1 = backtrack_plain(variables, domains, nbrs, all_bots)
    s2, st2, t2 = backtrack_mrv(variables, domains, nbrs, all_bots)
    s3, st3, t3 = backtrack_mrv_fc(variables, domains, nbrs, all_bots)
    for name, st, tm in [("Plain Backtracking",st1,t1),
                         ("MRV",st2,t2),
                         ("MRV + Forward Checking",st3,t3)]:
        print(f"  {name:<35} {st['assigns']:<10} {st['backtracks']:<12} {tm:.6f}")
    print()

if __name__ == "__main__":
    main()
