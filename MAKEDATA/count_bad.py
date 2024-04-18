from files2txt2files import read_list_from_file


def count_occurrences(elements):
    occurrences = {}
    for element in elements:
        prefix = element.split('-')[0]
        if prefix in occurrences:
            occurrences[prefix] += 1
        else:
            occurrences[prefix] = 1
    return occurrences





if __name__ == "__main__":
    elements = read_list_from_file("/Users/andershelbo/Desktop/MRI2CT/MAKEDATA/bad_data.txt")

    occurrences = count_occurrences(elements)

    sorted_occurrences = dict(sorted(occurrences.items(), key=lambda x: x[1], reverse=True))


    # Print occurrences
    for prefix, count in sorted_occurrences.items():
        print(f"{prefix}: {count}")