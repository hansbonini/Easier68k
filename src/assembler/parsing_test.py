import io
import os
from parsing_util import strip_comments, get_label, strip_label

def find_labels(file):
    labels = {}

    line_number = 0

    for raw_line in f:
        line_number += 1
        line = strip_comments(raw_line)
        if not line.strip(): continue # Skip empty lines

        label = get_label(line)

        if label is not None:
            if label in labels.keys():
                raise Exception("Label {} is already defined".format(label))
            else:
                labels[label] = (line_number, strip_label(line))
    
    return labels

f = open("Easier68k/src/assembler/test_parse.txt", "r")

line_number = 0
labels = find_labels(f)

print("Found labels:")
for label in labels.items():
    print(" - {} at line {}".format(label[0], label[1]))

f.close()
