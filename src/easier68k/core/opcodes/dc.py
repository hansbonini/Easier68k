from ...core.opcodes.opcode import Opcode
from ...core.util import opcode_util
from ...simulator.m68k import M68K
from ..util.parsing import parse_literal
import math


def command_matches(command: str) -> bool:
    """
    Checks whether a command string is an instance of this command type
    :param command: The command string to check (e.g. 'MOVE.B', 'LEA', etc.)
    :return: Whether the string is an instance of this command type
    """
    return opcode_util.command_matches(command, 'DC')


class_name = 'DC'


class DC(Opcode):
    allowed_sizes = 'BWL'

    def __init__(self, values: list, size='W'):
        assert size.upper() in DC.allowed_sizes
        self.size = size

        assert len(values) > 0
        self.values = values

    @classmethod
    def from_str(cls, command: str, parameters: str):
        """
        Parses a command string into an instance of the opcode class

        >>> test0 = DC.from_str("DC.B", "$0A, $0B")[0]
        >>> test0.size
        'B'
        >>> test0.values
        ['$0A', '$0B']

        >>> test1 = DC.from_str("DC.B", "\\'Hai!\\'")[0]
        >>> test1.size
        'B'
        >>> test1.values
        ['$48', '$61', '$69', '$21']

        >>> test2 = DC.from_str("DC.L", "\\'Hai\\'")[0]
        >>> test2.size
        'L'
        >>> test2.values
        ['$48', '$61', '$69', '$00']

        >>> test3 = DC.from_str("DC.L", "\\'Hai\\', $AB")[0]
        >>> test3.size
        'L'
        >>> test3.values
        ['$48', '$61', '$69', '$00', '$00', '$00', '$00', '$AB']

        >>> test4 = DC.from_str("DC.W", "\\'Hai\\', $AB")[0]
        >>> test4.size
        'W'
        >>> test4.values
        ['$48', '$61', '$69', '$00', '$00', '$AB']

        :param command: The command itself (e.g. 'MOVE.B', 'LEA', etc.)
        :param parameters: The parameters after the command (such as the source and destination of a move)
        """
        valid, issues = DC.is_valid(command, parameters)
        assert valid, 'Invalid command'
        # We're good without asserts from here on out

        parts = command.split('.')  # Split the command by period to get the size of the command
        if len(parts) == 1:  # Use the default size
            size = 'W'
        else:
            size = parts[1].upper()

        params = []
        quote_delim = None  # If None, we're not in a quote: if it has a value, we know what we're looking for to break the quote
        current_param = ''
        is_string = False

        for c in parameters:
            if c == ',' and not quote_delim:  # End of this parameter (and not a comma in a quote)
                if current_param:
                    if is_string:
                        temp_params = []
                        for char in current_param:
                            temp_params.append('$' + format(ord(char), "x"))

                        # Right pad the string with zeroes
                        if size == 'L':
                            while len(temp_params) % 4 != 0:
                                temp_params.append('$00')
                        if size == 'W':
                            while len(temp_params) % 2 != 0:
                                temp_params.append('$00')

                        params.extend(temp_params)
                    else:
                        # Make the value the right hex length
                        val = parse_literal(current_param.strip())
                        hexed = hex(val)[2:].upper()
                        if size == 'L':
                            while len(hexed) % 8 != 0:
                                hexed = '0' + hexed

                        if size == 'W':
                            while len(hexed) % 4 != 0:
                                hexed = '0' + hexed

                        if size == 'B':
                            while len(hexed) % 2 != 0:
                                hexed = '0' + hexed

                        # Length is now for sure even
                        for i in range(0, len(hexed), 2):
                            params.append('$' + hexed[i:i+2])

                is_string = False
                quote_delim = None
                current_param = ''
                continue

            if quote_delim and c == quote_delim:  # Breaking out of the quote
                quote_delim = None
                continue

            if c == '\'':
                if not quote_delim:  # This is the start of a quote
                    quote_delim = '\''
                    current_param = ''
                    is_string = True
                    continue

            if c == '\"':
                if not quote_delim:  # This is the start of a quote
                    quote_delim = '\"'
                    current_param = ''
                    is_string = True
                    continue

            current_param += c

        if current_param:
            if is_string:
                temp_params = []
                for c in current_param:
                    temp_params.append('$' + format(ord(c), "x"))

                # Right pad the string with zeroes
                if size == 'L':
                    while len(temp_params) % 4 != 0:
                        temp_params.append('$00')
                if size == 'W':
                    while len(temp_params) % 2 != 0:
                        temp_params.append('$00')

                params.extend(temp_params)
            else:
                # Make the value the right hex length
                val = parse_literal(current_param.strip())
                hexed = hex(val)[2:].upper()
                if size == 'L':
                    while len(hexed) % 8 != 0:
                        hexed = '0' + hexed

                if size == 'W':
                    while len(hexed) % 4 != 0:
                        hexed = '0' + hexed

                if size == 'B':
                    while len(hexed) % 2 != 0:
                        hexed = '0' + hexed

                # Length is now for sure even
                for i in range(0, len(hexed), 2):
                    params.append('$' + hexed[i:i+2])

        return DC(params, size), issues

    @staticmethod
    def is_valid(command: str, parameters: str) -> (bool, list):
        """
        Tests whether the given command is valid

        >>> DC.is_valid('DC.B', '\\'Hello, world!\\'')[0]
        True

        >>> DC.is_valid('DC.B', '\\'Hello\\'\\' world!\\'')[0]
        False

        >>> DC.is_valid('DC.W', '\\'Hello\\', \\' world!\\'')[0]
        True

        >>> DC.is_valid('DC.W', '$0A, $0B')[0]
        True

        >>> DC.is_valid('DC.L', '$0A')[0]
        True

        >>> DC.is_valid('DC.B', '')[0]
        False

        >>> DC.is_valid('DC.W', '\\'Hey!\\', $0A')[0]
        True

        >>> DC.is_valid('DC.G', '$0A')[0]
        False

        :param command: The command itself (e.g. 'MOVE.B', 'LEA', etc.)
        :param parameters: The parameters after the command (such as the source and destination of a move)
        :return: Whether the given command is valid and a list of issues/warnings encountered
        """
        issues = []
        try:
            assert opcode_util.check_valid_command(command, 'DC', valid_sizes=DC.allowed_sizes), 'Command invalid'
            # Can't just do a "split by comma" here because we could have commas inside of a string literal
            param_count = 0
            quote_delim = None  # If None, we're not in a quote: if it has a value, we know what we're looking for to break the quote
            current_param = ''
            is_string = False

            for c in parameters:
                if c == ',' and not quote_delim:  # End of this parameter (and not a comma in a quote)
                    if current_param:
                        if not is_string:  # Try parsing this value for a literal (if it's a string it's almost certainly fine)
                            assert parse_literal(current_param.strip()) is not None, 'Error parsing literal'
                        param_count += 1

                    is_string = False
                    quote_delim = None
                    current_param = ''
                    continue

                if quote_delim and c == quote_delim:  # Breaking out of the quote
                    quote_delim = None
                    continue

                if c == '\'':
                    if not quote_delim:  # This is the start of a quote
                        quote_delim = '\''
                        assert not current_param.strip(), "Can't have two quotes in a row in one parameter"
                        current_param = ''
                        is_string = True
                        continue

                if c == '\"':
                    if not quote_delim:  # This is the start of a quote
                        quote_delim = '\"'
                        assert not current_param.strip(), "Can't have two quotes in a row in one parameter"
                        current_param = ''
                        is_string = True
                        continue

                current_param += c

            assert not quote_delim, 'Unclosed quotes'
            if current_param:
                if not is_string:  # Try parsing this value for a literal (if it's a string it's almost certainly fine)
                    assert parse_literal(current_param.strip()) is not None, 'Error parsing literal'
                param_count += 1

            assert param_count > 0, 'Must have at least one parameter'

        except AssertionError as e:
            issues.append((e.args[0], 'ERROR'))
            return False, issues

        return True, issues

    @staticmethod
    def get_word_length(command: str, parameters: str) -> (int, list):
        """
        Gets the final length of a command in memory in words
        NOTE: for DC.B, this will round UP to make it a full word, even though it won't use the full memory

        >>> DC.get_word_length('DC.B', '$0A, $0B')[0]
        1

        >>> DC.get_word_length('DC.W', '$0A, $0B')[0]
        2

        >>> DC.get_word_length('DC.L', '$0A, $0B')[0]
        4

        >>> DC.get_word_length('DC.B', '\\'Hai!\\'')[0]
        2

        >>> DC.get_word_length('DC.W', '\\'Hai!\\'')[0]
        2

        >>> DC.get_word_length('DC.L', '\\'Hai!\\'')[0]
        4

        :param command: The command itself (e.g. 'MOVE.B', 'LEA', etc.)
        :param parameters:  The parameters after the command (such as the source and destination of a move)
        :return: The length of the command in memory (in words) and a list of issues/warnings encountered during assembly
        """
        valid, issues = DC.is_valid(command, parameters)
        assert valid, 'Invalid command'
        # We're good without asserts from here on out

        parts = command.split('.')  # Split the command by period to get the size of the command
        if len(parts) == 1:  # Use the default size
            size = 'W'
        else:
            size = parts[1].upper()

        length = 0.0
        quote_delim = None  # If None, we're not in a quote: if it has a value, we know what we're looking for to break the quote
        current_param = ''
        is_string = False

        for c in parameters:
            if c == ',' and not quote_delim:  # End of this parameter (and not a comma in a quote)
                if current_param:
                    if is_string:
                        length += len(current_param) * 0.5
                        if len(current_param) % 2 != 0:
                            length += 1
                    else:
                        if size == 'B':
                            length += 0.5
                        elif size == 'W':
                            length += 1
                        elif size == 'L':
                            length += 2

                is_string = False
                quote_delim = None
                current_param = ''
                continue

            if quote_delim and c == quote_delim:  # Breaking out of the quote
                quote_delim = None
                continue

            if c == '\'':
                if not quote_delim:  # This is the start of a quote
                    quote_delim = '\''
                    current_param = ''
                    is_string = True
                    continue

            if c == '\"':
                if not quote_delim:  # This is the start of a quote
                    quote_delim = '\"'
                    current_param = ''
                    is_string = True
                    continue

            current_param += c

        if current_param:
            if is_string:
                length += len(current_param) * 0.5
            else:
                if size == 'B':
                    length += 0.5
                elif size == 'W':
                    length += 1
                elif size == 'L':
                    length += 2

        length = math.ceil(length)
        if size == 'L' and length % 4 != 0:
            length = length + (length % 4)

        return length, issues

    def assemble(self) -> bytearray:
        """
        Assembles this opcode into hex to be inserted into memory
        :return: The hex version of this opcode
        """
        tr = ''
        for val in self.values:
            tr += '{0:08b}'.format(parse_literal(val))

        return bytearray.fromhex(hex(int(tr, 2))[2:])  # Convert to a bytearray

    def execute(self, simulator: M68K):
        """
        Executes this command in a simulator
        :param simulator: The simulator to execute the command on
        :return: Nothing
        """
        pass

    def __str__(self):
        return "DC command: Size {}, items: {}".format(self.size, self.values)
