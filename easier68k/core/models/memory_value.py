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

    def get_size(self) -> OpSize:
        """
        Gets the length of this memory value as an OpSize
        :return: the length in bytes of this value as defined by an OpSize
        """
        return self.length

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
        if self.length is OpSize.LONG:
            assert (0 <= unsigned_int <= 0xFFFFFFFF), 'Value must fit in the range [0, 0xFFFFFFFF].'
        if self.length is OpSize.WORD:
            assert (0 <= unsigned_int <= 0xFFFF), 'Value must fit in the range [0, 0xFFFF]'
        if self.length is OpSize.BYTE:
            assert (0 <= unsigned_int <= 0xFF), 'Value must fit in the range [0, 0xFF]'

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

        mask = 0xFF
        if length is OpSize.WORD:
            mask = 0xFFFF
        elif length is OpSize.LONG:
            mask = 0xFFFFFFFF

        return (value ^ mask) + 1

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
        if self.get_msb():
            ret_val = self.__twos_complement(self.unsigned_value, self.length)
            return -1 * ret_val
        # otherwise, is positive and don't have to convert
        return self.unsigned_value

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

        # default mask is one byte
        mask = 0x80
        if self.length is OpSize.WORD:
            mask = 0x8000
        elif self.length is OpSize.LONG:
            mask = 0x80000000

        # determine if the unsigned value MSB is set to 1
        # by masking only the MSB and checking that the result
        # has some value set
        return self.unsigned_value & mask > 0

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
        return 'MemoryValue {0}'.format(hex(self.unsigned_value))

    def __bytes__(self):
        """
        Get the bytes representation of this
        :return:
        """
        return self.unsigned_value.to_bytes(self.length.get_number_of_bytes(), byteorder='big', signed=False)
