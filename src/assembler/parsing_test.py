from src.assembler.parsing_util import strip_comments, get_label, strip_label, find_labels, get_opword, strip_opword
from src.assembler.parser import register_callback, parse_line, set_labels


def process_org(args):
    print("ORGing at {}".format(args))


# -------- BEGIN TEST CODE --------
f = open("test_parse.txt", "r")

labels = find_labels(f)

print("Found labels:")
for label in labels.items():
    print(" - {} at line {}".format(label[0], label[1]))

f.seek(0)

register_callback("ORG", process_org)
set_labels(labels)

for raw_line in f:
    l = strip_label(strip_comments(raw_line))
    if not l.strip():
        continue  # Skip empty lines

    # print(l)
    parse_line(l)

f.close()
