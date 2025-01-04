def read_list_from_file(filename):
    lst = []
    with open(filename, 'r') as file:
        for line in file:
            lst.append(line.strip())
    return lst

def print_hierarchical(statement, d):
    prefix = ["","├─ ", "│  ├─ ", "│     ├─ "]
    print(f"{prefix[d]}{statement}")
