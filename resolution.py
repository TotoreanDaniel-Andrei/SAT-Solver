import sys
import time
import tracemalloc
import json
from itertools import combinations

def parse_dimacs(filename):
    clauses = []
    with open(filename, 'r') as file:
        for line_num, line in enumerate(file, start=1):
            line = line.strip()
            if not line or line.startswith(('c', 'p', '%')):
                continue
            try:
                nums = list(map(int, line.split()))
                if not nums or nums[-1] != 0:
                    raise ValueError(f"Line {line_num} missing terminating 0: {line}")
                clause = nums[:-1]  # exclude the ending 0
                if clause:
                    clauses.append(clause)
            except ValueError as ve:
                raise ValueError(f"Invalid CNF format at line {line_num}: {ve}")
    return clauses

class ResolutionSolver:
    def __init__(self, cnf):
        self.clauses = [frozenset(clause) for clause in cnf]

    def solve(self, max_clauses=100000):
        while True:
            new_clauses = set()
            for c1, c2 in combinations(self.clauses, 2):
                resolvent = self._resolve(c1, c2)
                if resolvent is not None:
                    if not resolvent:
                        return False
                    new_clauses.add(resolvent)
            if new_clauses.issubset(set(self.clauses)):
                return True
            self.clauses += list(new_clauses)
            if len(self.clauses) > max_clauses:
                raise MemoryError("Clause limit exceeded")

    def _resolve(self, c1, c2):
        for lit in c1:
            if -lit in c2:
                return (c1 | c2) - {lit, -lit}
        return None

if __name__ == "__main__":
    try:
        if len(sys.argv) < 2:
            raise ValueError("Please provide a CNF file as an argument.")

        cnf = parse_dimacs(sys.argv[1])
        if not cnf:
            raise ValueError("No clauses found in CNF file.")

        solver = ResolutionSolver(cnf)

        tracemalloc.start()
        start = time.time()
        result = solver.solve()
        end = time.time()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        output = {
            "filename": sys.argv[1],
            "satisfiable": result,
            "time": round(end - start, 4),
            "memory_MB": round(peak / 10**6, 2)
        }
        print(json.dumps(output))

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
