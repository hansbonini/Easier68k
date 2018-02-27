from src.assembler.parsing_util import strip_comments, get_label, strip_label


def find_labels(file):
    found_labels = {}

    line_number = 0

    for raw_line in file:
        line_number += 1
        line = strip_comments(raw_line)
        if not line.strip():
            continue  # Skip empty lines

        label = get_label(line)

        if label is not None:
            if label in found_labels.keys():
                raise Exception("Label {} is already defined".format(label))
            else:
                found_labels[label] = (line_number, strip_label(line))
    
    return labels


f = open("Easier68k/src/assembler/test_parse.txt", "r")

labels = find_labels(f)

print("Found labels:")
for l in labels.items():
    print(" - {} at line {}".format(l[0], l[1]))

f.close()
