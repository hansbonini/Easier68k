"""
<<<<<<< d92706f647ee633eaa9c92ef347d44f5a8051017
<<<<<<< 37baa921f537e7a4fa188a262d0c6f0bd5b26e5f
<<<<<<< 6dbc4e879427374bddda73a92cc7771cc1c5c0da
>>> str(Move.from_str('MOVE.B', '-(A0), D1')[0])
=======
<<<<<<< 2d6ea7cab68fbdedabbb096d9d755f1eae7d7112
=======
>>>>>>> Added some code reuse to the move opcode
>>> str(Move.from_str('MOVE.B', '-(A0), D1'))
>>>>>>> Completed phase 3 of the assembler
=======
>>> str(Move.from_str('MOVE.B', '-(A0), D1')[0])
>>>>>>> Rebased onto Chris's PR
'Move command: Size B, src EA Mode: EAMode.ARIPD, Data: 0, dest EA Mode: EAMode.DRD, Data: 1'

>>> str(Move.from_str('MOVE.L', 'D3, (A0)')[0])
'Move command: Size L, src EA Mode: EAMode.DRD, Data: 3, dest EA Mode: EAMode.ARI, Data: 0'

>>> Move.from_str('MOVE.W', 'D3, A3')[1]
[('Invalid addressing mode', 'ERROR')]
"""
from ...core.enum.ea_mode import EAMode
from ...core.enum.op_size import MoveSize
from ...core.enum.ea_mode_bin import EAModeBinary
from ...simulator.m68k import M68K
from ...core.opcodes.opcode import Opcode
from ...core.util import opcode_util
from ...core.util.conversions import get_number_of_bytes
from ..util.parsing import parse_assembly_parameter


def command_matches(command: str) -> bool:
    """
    Checks whether a command string is an instance of this command type
    :param command: The command string to check (e.g. 'MOVE.B', 'LEA', etc.)
    :return: Whether the string is an instance of this command type
    """
    return opcode_util.command_matches(command, 'MOVE')


class_name = 'Move'


class Move(Opcode):
    # Allowed values: nothing, or some combination of B, W, and L (for byte, word, and long)
    # For example, MOVE would have 'BWL' because it can operate on any size of data, while MOVEA would have 'WL' because
    # it can't operate on byte-sized data
    allowed_sizes = 'BWL'

    @classmethod
    def from_str(cls, command: str, parameters: str):
        """
        Parses a MOVE command from memory.

        :param command: The command itself (e.g. 'MOVE.B', 'LEA', etc.)
        :param parameters: The parameters after the command (such as the source and destination of a move)
        """
        valid, issues = Move.is_valid(command, parameters)
        if not valid:
            return None, issues
        # We can forego asserts in here because we've now confirmed this is valid assembly code

        size = opcode_util.get_size(command)

        # Split the parameters into EA modes
        params = parameters.split(',')
        src = parse_assembly_parameter(params[0].strip())
        dest = parse_assembly_parameter(params[1].strip())

        return cls(src, dest, size), issues

    def __init__(self, src: EAMode, dest: EAMode, size='W'):
        # Check that the src is of the proper type (for example, can't move from an address register for a move command)
        assert src.mode != EAMode.ARD  # Only invalid src is address register direct
        self.src = src

        # Check that the destination is of a proper type
        assert dest.mode != EAMode.ARD and dest.mode != EAMode.IMM  # Can't take address register direct or immediates
        self.dest = dest

        # Check that this is a valid size (for example, 'MOVEA.B' is not a valid command)
        assert size.upper() in Move.allowed_sizes
        self.size = size

    def assemble(self) -> bytearray:
        """
        Assembles this opcode into hex to be inserted into memory
        :return: The hex version of this opcode
        """
        # Create a binary string to append to, which we'll convert to hex at the end
        tr = '00'  # Opcode
        tr += '{0:02b}'.format(MoveSize.parse(self.size))  # Size bits
        tr += EAModeBinary.parse_from_ea_mode_xnfirst(self.dest)  # Destination first
        tr += EAModeBinary.parse_from_ea_mode_mfirst(self.src)  # Source second
        # Append immediates/absolute addresses after the command
        tr += opcode_util.ea_to_binary_post_op(self.src, self.size)
        tr += opcode_util.ea_to_binary_post_op(self.dest, self.size)

        to_return = bytearray.fromhex(hex(int(tr, 2))[2:])  # Convert to a bytearray
        return to_return

    def execute(self, simulator: M68K):
        """
        Executes this command in a simulator
        :param simulator: The simulator to execute the command on
        :return: Nothing
        """
        # get the length
        val_length = get_number_of_bytes(self.size)

        # get the value of src from the simulator
        src_val = self.src.get_value(simulator, val_length)

        # and set the value
<<<<<<< 6dbc4e879427374bddda73a92cc7771cc1c5c0da
        self.dest.set_value(simulator, src_val, val_length)
=======
        self.dest.set_value(simulator, src_val)
>>>>>>> Completed phase 3 of the assembler

    def __str__(self):
        # Makes this a bit easier to read in doctest output
        return 'Move command: Size {}, src {}, dest {}'.format(self.size, self.src, self.dest)

    @staticmethod
    def is_valid(command: str, parameters: str) -> (bool, list):
        """
        Tests whether the given command is valid

        >>> Move.is_valid('MOVE.B', 'D0, D1')[0]
        True

        >>> Move.is_valid('MOVE.W', 'D0')[0]
        False

        >>> Move.is_valid('MOVE.G', 'D0, D1')[0]
        False

        >>> Move.is_valid('MOVE.L', 'D0, A2')[0]
        False

        >>> Move.is_valid('MOV.L', 'D0, D1')[0]
        False

        >>> Move.is_valid('MOVE.', 'D0, D1')[0]
        False

        :param command: The command itself (e.g. 'MOVE.B', 'LEA', etc.)
        :param parameters: The parameters after the command (such as the source and destination of a move)
        :return: Whether the given command is valid and a list of issues/warnings encountered
        """
        issues = []
        try:
            assert opcode_util.check_valid_command(command, 'MOVE', valid_sizes=Move.allowed_sizes), 'Command invalid'

            # Split the parameters into EA modes
            params = parameters.split(',')
            assert len(params) == 2, 'Must have two parameters'

            src = parse_assembly_parameter(params[0].strip())  # Parse the source and make sure it parsed right
            assert src, 'Error parsing src'

            dest = parse_assembly_parameter(params[1].strip())
            assert dest, 'Error parsing dest'

            assert src.mode != EAMode.ARD, 'Invalid addressing mode'  # Only invalid src is address register direct
            assert dest.mode != EAMode.ARD and dest.mode != EAMode.IMM, 'Invalid addressing mode'

            return True, issues
        except AssertionError as e:
            issues.append((e.args[0], 'ERROR'))
            return False, issues

    @staticmethod
    def get_word_length(command: str, parameters: str) -> (int, list):
        """
        >>> Move.get_word_length('MOVE', 'D0, D1')
        (1, [])

        >>> Move.get_word_length('MOVE.L', '#$90, D3')
        (3, [])

        >>> Move.get_word_length('MOVE.W', '#$90, D3')
        (2, [])

        >>> Move.get_word_length('MOVE.W', '($AAAA).L, D7')
        (3, [])

        >>> Move.get_word_length('MOVE.W', 'D0, ($BBBB).L')
        (3, [])

        >>> Move.get_word_length('MOVE.W', '($AAAA).L, ($BBBB).L')
        (5, [])

        >>> Move.get_word_length('MOVE.W', '#$AAAA, ($BBBB).L')
        (4, [])

        Gets what the end length of this command will be in memory
        :param command: The text of the command itself (e.g. "LEA", "MOVE.B", etc.)
        :param parameters: The parameters after the command
        :return: The length of the bytes in memory in words, as well as a list of warnings or errors encountered
        """
        valid, issues = Move.is_valid(command, parameters)
        if not valid:
            return 0, issues
        # We can forego asserts in here because we've now confirmed this is valid assembly code

        issues = []  # Set up our issues list (warnings + errors)
        parts = command.split('.')  # Split the command by period to get the size of the command
        if len(parts) == 1:  # Use the default size
            size = 'W'
        else:
            size = parts[1]

        # Split the parameters into EA modes
        params = parameters.split(',')

        if len(params) != 2:  # We need exactly 2 parameters
            issues.append(('Invalid syntax (missing a parameter/too many parameters)', 'ERROR'))
            return 0, issues

<<<<<<< d92706f647ee633eaa9c92ef347d44f5a8051017
        src = parse_assembly_parameter(params[0].strip())  # Parse the source and make sure it parsed right
        dest = parse_assembly_parameter(params[1].strip())

        if len(params) != 2:  # We need exactly 2 parameters
            issues.append(('Invalid syntax (missing a parameter/too many parameters)', 'ERROR'))
            return 0, issues

        src = EAMode.parse_ea(params[0].strip())  # Parse the source and make sure it parsed right
        dest = EAMode.parse_ea(params[1].strip())

=======
>>>>>>> Rebased onto Chris's PR
        length = 1  # Always 1 word not counting additions to end

        if src.mode == EAMode.IMM:  # If we're moving an immediate we have to append the value afterwards
            if size == 'L':
                length += 2  # Longs are 2 words long
            else:
                length += 1  # This is a word or byte, so only 1 word

        if src.mode == EAMode.AWA:  # Appends a word
            length += 1

        if src.mode == EAMode.ALA:  # Appends a long, so 2 words
            length += 2

        if dest.mode == EAMode.AWA:  # Appends a word
            length += 1

        if dest.mode == EAMode.ALA:  # Appends a long, so 2 words
            length += 2

        return length, issues
