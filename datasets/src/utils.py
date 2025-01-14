def read_list_from_file(filename):
    lst = []
    with open(filename, 'r') as file:
        for line in file:
            lst.append(line.strip())
    return lst

def print_hierarchical(statement, depth = 0):
    prefix = "│  " * (depth-1) + "├─ " if depth > 0 else "\n"
    print(prefix+statement)