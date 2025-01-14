def print_hierarchical(statement, depth = 0):
    prefix = "│  " * (depth-1) + "├─ " if depth > 0 else "\n"
    print(prefix+statement)


