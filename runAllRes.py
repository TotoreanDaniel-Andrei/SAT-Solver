# runAllDp.py
import os
import sys
import subprocess
import json
import csv

if len(sys.argv) != 2:
    print("Usage: python runAllDp.py <dataset_folder>")
    sys.exit(1)

dataset = sys.argv[1]
folder = os.path.join("cnf_files", dataset)
script = "resolution.py"
timeout_seconds = 30

if not os.path.exists(folder):
    print(f"Folder not found: {folder}")
    sys.exit(1)

results = []
timeouts = 0

for filename in os.listdir(folder):
    if filename.endswith(".cnf"):
        filepath = os.path.join(folder, filename)
        print(f"Running {filename}...")
        try:
            output = subprocess.check_output(
                ["python", script, filepath],
                stderr=subprocess.STDOUT,
                timeout=timeout_seconds
            )
            data = json.loads(output)
            data["filename"] = filename
            results.append(data)
        except subprocess.TimeoutExpired:
            print(f"Timeout on {filename}")
            results.append({
                "filename": filename,
                "satisfiable": False,
                "time": float('inf'),
                "memory_MB": 0.0
            })
            timeouts += 1
        except Exception as e:
            print(f"Error on {filename}: {e}")

# Filter out timeouts for stats
filtered = [r for r in results if r["time"] != float('inf')]

total = len(results)
solved = sum(1 for r in results if r["satisfiable"])
success_rate = (solved / total) * 100 if total > 0 else 0
avg_time = sum(r["time"] for r in filtered) / len(filtered) if filtered else 0
avg_mem = sum(r["memory_MB"] for r in filtered) / len(filtered) if filtered else 0

# Print summary
print("\n--- Summary ---")
print(f"Method: {script}")
print(f"Dataset: {dataset}")
print(f"Total: {total}")
print(f"Satisfiable: {solved}")
print(f"Timeouts: {timeouts}")
print(f"Success Rate: {success_rate:.1f}%")
print(f"Average Time (no timeouts): {avg_time:.4f}s")
print(f"Average Memory (no timeouts): {avg_mem:.2f}MB")

# Save to CSV
results_folder = "results"
os.makedirs(results_folder, exist_ok=True)

csv_name = f"results_{dataset}_res.csv"
csv_path = os.path.join(results_folder, csv_name)

with open(csv_path, "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["filename", "satisfiable", "time", "memory_MB"])
    writer.writeheader()
    writer.writerows(results)
    writer.writerow({
        "filename": "AVERAGE (no timeouts)",
        "satisfiable": f"{success_rate:.1f}%",
        "time": f"{avg_time:.4f}",
        "memory_MB": f"{avg_mem:.2f}"
    })

print(f"Results saved to {csv_path}")
