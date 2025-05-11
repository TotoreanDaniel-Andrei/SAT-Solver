import os
import pandas as pd

results_folder = "results"
output_file = "latex_tables.tex"

summary = {}

# Process all CSVs
for filename in os.listdir(results_folder):
    if not filename.endswith(".csv") or not filename.startswith("results_dataset_"):
        continue

    parts = filename.replace(".csv", "").split("_")
    if len(parts) < 5:
        continue

    try:
        var = int(parts[2])           # e.g., 20
        solver = parts[4].upper()     # e.g., RES
    except ValueError:
        continue

    path = os.path.join(results_folder, filename)
    df = pd.read_csv(path)

    # Look for the row where filename is AVERAGE (case insensitive)
    avg_row = df[df["filename"].str.upper() == "AVERAGE"]
    if avg_row.empty:
        continue

    time = avg_row["time"].values[0]
    memory = avg_row["memory_MB"].values[0]
    success = avg_row["satisfiable"].values[0]

    summary.setdefault(var, {})[solver] = {
        "time": time,
        "memory": memory,
        "success": success
    }

# Generate LaTeX tables
latex = ""
for var in sorted(summary.keys()):
    latex += f"\\begin{{table}}[H]\n\\centering\n"
    latex += f"\\caption{{Performance on {var}-variable Instances}}\n"
    latex += "\\begin{tabular}{lccc}\n\\toprule\n"
    latex += "Solver & Avg Time (s) & Avg Memory (MB) & Success Rate \\\\\n\\midrule\n"
    for solver in ["RES", "DP", "DPLL"]:
        if solver in summary[var]:
            s = summary[var][solver]
            latex += f"{solver} & {s['time']} & {s['memory']} & {s['success']} \\\\\n"
        else:
            latex += f"{solver} & -- & -- & -- \\\\\n"
    latex += "\\bottomrule\n\\end{tabular}\n\\end{table}\n\n"

# Save output
with open(output_file, "w") as f:
    f.write(latex)

print(f"LaTeX tables saved to {output_file}")
