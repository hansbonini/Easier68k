"""
Memory Value

Representation of some value in memory with a length of a Byte, Word or Long Word,
which can either be an array of bytes, an integer number, a single character
or an array of characters.

Supports operations like adding, subtracting, shift left, shift right, bitwise OR AND XOR, equals

Supports getting the most significant bit, determining the signed or unsigned integer values, the value
as a array of bytes, the value as a hex string.

This was done to keep the interal handling of memory values consistent, instead of conversions back and forth between
integers, hex strings and byte arrays.
"""

from ..enum.op_size import OpSize

class MemoryValue:

    def __init__(self, len: OpSize = OpSize.WORD):
        """
        Constructor

        Sets the initial value to zero with a length of OpSize.Word
        :param len the length in bytes of this memory value
        """

        # use integers as the interal storage of the value
        # this should be an UNSIGNED value
        self.unsigned_value = 0

        # use OpSize for length in bytes
        self.length = size

    def set_size(self, size: OpSize):
        """
        Sets the length of this memory value
        :param size: the length in bytes of this value, defined by OpSize
        :return: None
        """
        self.length = size

    def set_value_signed_int(self, signed_int: int):
        """
        Sets the value of this MemoryValue from a signed int
        :param signed_int:
        :return:
        """

        # assert that the value can fit within the possible range for the size

        # if the value is negative, take the 2s comp for the length

        # if the value is positive and MSB not set, set the value


    @staticmethod
    def __twos_complement(value: int, length: OpSize) -> int:
        """
        Returns the twos complement of the given value
        :param value: the value to take the 2s comp of
        :param length: the length in bytes of the value
        :return:
        """



