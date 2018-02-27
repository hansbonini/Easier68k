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

    if line[0] == ' ': # Simply just trim the line, since it isn't a label
        return line.strip()
    
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


