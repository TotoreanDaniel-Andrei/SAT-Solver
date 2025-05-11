def parse_dimacs(filename):
    clauses = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith(('c', 'p', '%', '0')):
                continue
            try:
                nums = list(map(int, line.split()))
                if nums:
                    clauses.append(nums[:-1])  # remove trailing 0
            except ValueError:
                continue
    return clauses
