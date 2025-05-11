import sys
import time
import tracemalloc
from cnfParse import parse_dimacs
from copy import deepcopy

class DPSolver:
    def __init__(self, cnf):
        self.clauses = [set(c) for c in cnf]
        self.vars = {abs(l) for c in self.clauses for l in c}

    def solve(self):
        return self._dp(self.clauses, self.vars)

    def _dp(self, clauses, variables):
        if not clauses:
            return True
        if any(not c for c in clauses):
            return False
        var = next(iter(variables))
        new_vars = variables - {var}

        for val in [True, False]:
            new_clauses = []
            for c in clauses:
                if (var if val else -var) in c:
                    continue
                new_c = c - {(-var if val else var)}
                new_clauses.append(new_c)
            if self._dp(new_clauses, new_vars):
                return True
        return False

if __name__ == "__main__":
    cnf = parse_dimacs(sys.argv[1])
    solver = DPSolver(cnf)

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