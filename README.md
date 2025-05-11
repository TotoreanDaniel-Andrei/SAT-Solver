
# SAT Solvers - README

## Overview
This repository contains Python implementations of three SAT solvers: Resolution, Davis–Putnam (DP), and Davis–Putnam–Logemann–Loveland (DPLL). These solvers are designed to resolve Boolean satisfiability problems (SAT) using various methods.

## Getting Started

### Step 1: Prepare CNF Files
After downloading the code, you need to obtain CNF (Conjunctive Normal Form) files, which are the input format for the solvers. You can either:

1. **Download pre-made CNF files** from [SATLIB Benchmarks](https://www.cs.ubc.ca/~hoos/SATLIB/benchm.html).
2. **Generate new random CNF datasets** by running the `random3SatGenerator.py` script. You can do this by executing the following command:

   ```bash
   python random3SatGenerator.py
   ```

   In the generator script, you can change the number of variables by modifying the line:

   ```python
   n_vars = <desired_number_of_variables>
   ```

   Replace `<desired_number_of_variables>` with the number of variables you'd like to use for your generated CNF files.

### Step 2: Run the SAT Solvers
Once you have your CNF files (either downloaded or generated), you can run any of the SAT solvers. To do this, execute the corresponding Python script with the dataset as an argument:

- To run the **Davis–Putnam (DP)** solver:

  ```bash
  python runAllDp.py dataset_xx_x
  ```

- To run the **DPLL** solver:

  ```bash
  python runAllDpll.py dataset_xx_x
  ```

- To run the **Resolution** solver:

  ```bash
  python runAllRes.py dataset_xx_x
  ```

Replace `dataset_xx_x` with the appropriate file name of your CNF dataset (e.g., `dataset_20_100`).

### Step 3: View Results
Each solver will generate a CSV file with the results of the execution. These files contain information about the time taken, memory usage, and the success rate for solving the SAT problem.
