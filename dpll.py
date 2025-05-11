import sys
import time
import tracemalloc
from cnfParse import parse_dimacs
from copy import deepcopy

class DPLL:
    def __init__(self, cnf):
        self.cnf = [set(c) for c in cnf]
        self.vars = {abs(l) for c in self.cnf for l in c}

    def solve(self, assignment={}):
        self.unit_propagate()
        if any(not c for c in self.cnf):
            return False
        if not self.cnf:
            return True

        var = next(v for v in self.vars if v not in assignment)
        for val in [True, False]:
            new_solver = DPLL([list(c) for c in self.cnf])
            new_solver.vars = self.vars
            new_solver.assign(var, val)
            if new_solver.solve({**assignment, var: val}):
                return True
        return False

    def unit_propagate(self):
        changed = True
        while changed:
            changed = False
            unit_clauses = [c for c in self.cnf if len(c) == 1]
            for unit in unit_clauses:
                lit = next(iter(unit))
                self.assign(abs(lit), lit > 0)
                changed = True

    def assign(self, var, val):
        new_cnf = []
        for c in self.cnf:
            if (var if val else -var) in c:
                continue
            new_c = c - {(-var if val else var)}
            new_cnf.append(new_c)
        self.cnf = new_cnf

if __name__ == "__main__":
    cnf = parse_dimacs(sys.argv[1])
    solver = DPLL(cnf)

    tracemalloc.start()
    start = time.time()
    result = solver.solve()
    end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

import json
result_data = {
    "filename": sys.argv[1],
    "satisfiable": result,
    "time": round(end - start, 4),
    "memory_MB": round(peak / 10**6, 2)
}
print(json.dumps(result_data))