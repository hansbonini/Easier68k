def strip_comments(line):
    assert type(line) is str

    comment_index = len(line)
    semicolon_index = line.find(';')

    if semicolon_index != -1:
        comment_index = min(comment_index, semicolon_index)

    asterisk_index = line.find('*')
    if asterisk_index != -1:
        comment_index = min(comment_index, asterisk_index)
    
    return line[0:comment_index].replace('\r', '').replace('\n', '')


def get_label(line):
    assert type(line) is str

    if line[0] == ' ':
        return None # This isn't a label
    
    label = ''
    for c in line:
        if c == ' ' or c == ':': break
        label += c
    
    return label


def strip_label(line):
    assert type(line) is str

    if not line:
        return line  # This line is empty, just return it straight up

    if line[0] == ' ':
        return line.strip()  # Simply just trim the line, since it isn't a label
    
    # This is a label, we have to trim the label specifically
    to_return = ''
    past_label = False
    started_line = False
    for c in line:
        if c == ' ' and not past_label:
            past_label = True
            continue

        if c != ' ' and past_label and not started_line:
            started_line = True

        if started_line:
            to_return += c
        
    return to_return


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

    return found_labels


def get_opword(line):
    opword = ""
    for c in line:
        if c == ' ':
            return opword  # Found the end of the opword, return it

        opword += c


def strip_opword(line):
    to_return = ""

    past_opword = False
    past_spaces = False

    for c in line:
        if c == ' ' and not past_opword:
            past_opword = True
            continue

        if c != ' ' and past_opword and not past_spaces:
            past_spaces = True

        if past_spaces:
            to_return += c

    return to_return
