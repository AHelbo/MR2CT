import os

def list_from_folder(folder):
    elms = [elm[:-5] for elm in os.listdir(folder) if not elm == ".DS_Store"]
    return elms

def save_list_to_file(lst, filename):
    with open(filename, 'w') as file:
        for item in lst:
            file.write(str(item) + '\n')

def read_list_from_file(filename):
    lst = []
    with open(filename, 'r') as file:
        for line in file:
            lst.append(line.strip())
    return lst

# # # Example usage:
# # my_list = list_from_folder("/Users/andershelbo/Desktop/MAKEDATA/test_data")
# filename = 'test_data.txt'

# # # Save the list to a file
# # save_list_to_file(my_list, filename)

# # Read the list from the file
# read_list = read_list_from_file(filename)
# print(len(read_list))

# print(f"{len(my_list) = } {len(read_list) = } {my_list[123] = } {read_list[123] = }")
