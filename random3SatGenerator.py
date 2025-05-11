import os
import random

def generate_3sat_cnf(n_vars, n_clauses, filename):
    clauses = []
    for _ in range(n_clauses):
        clause = set()
        while len(clause) < 3:
            lit = random.randint(1, n_vars)
            lit *= random.choice([-1, 1])
            clause.add(lit)
        clauses.append(list(clause))

    with open(filename, "w") as f:
        f.write(f"p cnf {n_vars} {n_clauses}\n")
        for clause in clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

# ---- Configuration ----
num_folders = 5
files_per_folder = 10
n_vars = 100
n_clauses = int(n_vars * 4.3)  # good phase-transition density

base_path = "cnf_files"

for i in range(1, num_folders + 1):
    folder = os.path.join(base_path, f"dataset_100_{i}")
    os.makedirs(folder, exist_ok=True)
    for j in range(1, files_per_folder + 1):
        filename = os.path.join(folder, f"rand_100_{j}.cnf")
        generate_3sat_cnf(n_vars, n_clauses, filename)

