from src.assembler.parsing_util import get_opword, strip_opword

callbacks = {}
labels = {}


def set_labels(l):
    labels = l


def register_callback(opword, callback):
    callbacks[opword.upper()] = callback


def parse_line(line):
    op = get_opword(line).upper()

    args = strip_opword(line)

    if op not in callbacks.keys():
        print("No callback for opword {}".format(op))
        return

    callbacks[op](args)
