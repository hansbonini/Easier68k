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
    """
    Representation of some value in memory
    """

    def __new__(cls, *args, **kwargs):
        pass

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
        self.length = len

        # consider adding CCR bits for the last operation?
        # or just have CCR bit getters, in the ops just compare before and after

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
        pass

    def set_value_unsigned_int(self, unsigned_int: int):
        """
        Sets the value of this MemoryValue from an unsigned int
        :param unsigned_int:
        :return:
        """

        # assert that the value can fit within the possible range for the size

        self.unsigned_value = unsigned_int

    def set_value_bytes(self, bytes_value: bytes):
        """
        Sets the value of this MemoryValue from an array of bytes
        :param bytes_value:
        :return:
        """

        # assert that the value can fit within the possible range for the size

        # set the unsigned value

    @staticmethod
    def __twos_complement(value: int, length: OpSize) -> int:
        """
        Returns the twos complement of the given value
        :pasram value: the value to take the 2s comp of
        :param length: the length in bytes of the value
        :return:
        """


        pass

    def get_value_unsigned(self):
        """
        Gets the unsigned value
        :return:
        """
        return self.unsigned_value

    def get_value_signed(self):
        """
        Gets the signed value
        :return:
        """
        # if the msb is set
        # take the 2s comp and *-1
        pass

    def get_value_bytes(self):
        """
        Get the byte array value
        :return:
        """
        pass

    def get_msb(self):
        """
        Get the most significant bit indicating that the value is negative
        :return:
        """
        pass

    def __eq__(self, other):
        """
        Equals, compares to see that the value and length are the same
        :param other:
        :return:
        """
        assert isinstance(other, MemoryValue)
        return self.unsigned_value == other.unsigned_value and self.length == other.length

    def __add__(self, other):
        """
        Add, adds the value of two MemoryValues to each other
        :param other:
        :return:
        """
        assert isinstance(other, MemoryValue)

        # convert to signed and add
        # self.unsigned_value + other.unsigned_value

        # return the result
        pass

    def __radd__(self, other):
        """
        Reverse add, adds the value of the values
        :param other:
        :return:
        """
        assert isinstance(other, MemoryValue)

        # convert to signed and add
        # return the result
        pass

    def __gt__(self, other):
        """
        Greater than
        :param other:
        :return:
        """
        assert isinstance(other, MemoryValue)

        # convert to signed and compare
        pass

    def __lt__(self, other):
        """
        Less than
        :param other:
        :return:
        """
        assert isinstance(other, MemoryValue)

        # convert to signed and compare
        pass

    def __le__(self, other):
        """
        Less than or equals
        :param other:
        :return:
        """
        assert isinstance(other, MemoryValue)
        # convert to signed and compare
        pass

    def __ne__(self, other):
        """
        Not equal
        :param other:
        :return:
        """
        assert isinstance(other, MemoryValue)
        return self.unsigned_value != other.unsigned_value or self.length != other.length

    def __ge__(self, other):
        """
        Greater or equal
        :param other:
        :return:
        """
        assert isinstance(other, MemoryValue)
        # convert to signed and compare
        pass

    def __str__(self):
        """
        to str, show the hex representation
        :return:
        """
        return 'MemoryValue'

    def __bytes__(self):
        """
        Get the bytes representation of this
        :return:
        """
        pass
