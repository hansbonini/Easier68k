"""
Tests for core/models/memory_value
which represent some value in memory with a length and a value

Test just this file with:
pytest -v tests/easier68k/core/models/test_memory_value.py
"""

import pytest

from easier68k.core.models.memory_value import MemoryValue
from easier68k.core.enum.op_size import OpSize

def test_memory_value_cstr_and_eq():
    """
    Tests the behavior of the constructor

    Under the assumption that the equals overload behaves correctly as well
    :return:
    """

    # make a default value (0 len WORD)
    val = MemoryValue()

    # make a value with the length defined
    another_val = MemoryValue(OpSize.WORD)

    # check that they are equal
    assert (val == another_val)

    # check that the sizes are correct without using eq
    assert (val.length == OpSize.WORD)
    assert (another_val.length == OpSize.WORD)

    # check the default value
    assert (val.unsigned_value == 0)
    assert (another_val.unsigned_value == 0)

    # check for other sizes
    another_val = MemoryValue(OpSize.LONG)
    assert (another_val.length == OpSize.LONG)
    assert (another_val.unsigned_value == 0)

    # check for other sizes
    another_val = MemoryValue(OpSize.BYTE)
    assert (another_val.length == OpSize.BYTE)
    assert (another_val.unsigned_value == 0)

def test_set_value_unsigned():
    """
    Tests the way that unsigned values are set and ensures that
    values out of range for unsigned values cannot be set
    :return:
    """

    val = MemoryValue(OpSize.LONG)
    # try setting values that are good
    val.set_value_unsigned_int(123)
    assert (val.unsigned_value == 123)
    val.set_value_unsigned_int(0xFFF)
    assert (val.unsigned_value == 0xFFF)
    val.set_value_unsigned_int(0xFFFFFFFF)
    assert (val.unsigned_value == 0xFFFFFFFF)

    # try setting values that are out of bounds, they should all throw AssertException

    # for len byte
    val = MemoryValue(OpSize.BYTE)

    # check that the max can be used correctly
    val.set_value_unsigned_int(0xFF)
    assert (val.unsigned_value == 0xFF)

    # negative value
    with pytest.raises(AssertionError):
        val.set_value_unsigned_int(-1)
    with pytest.raises(AssertionError):
        val.set_value_unsigned_int(-12345)
    # value that is too big for byte
    with pytest.raises(AssertionError):
        val.set_value_unsigned_int(0xFF + 1)

    # for len word
    val = MemoryValue(OpSize.WORD)

    # check that the max can be used correctly
    val.set_value_unsigned_int(0xFFFF)
    assert (val.unsigned_value == 0xFFFF)

    # negative value
    with pytest.raises(AssertionError):
        val.set_value_unsigned_int(-1)
    with pytest.raises(AssertionError):
        val.set_value_unsigned_int(-12345)
    # value that is too big for word
    with pytest.raises(AssertionError):
        val.set_value_unsigned_int(0xFFFF + 1)

    # for len long
    val = MemoryValue(OpSize.LONG)

    # check that the max can be used correctly
    val.set_value_unsigned_int(0xFFFFFFFF)
    assert (val.unsigned_value == 0xFFFFFFFF)

    # negative value
    with pytest.raises(AssertionError):
        val.set_value_unsigned_int(-1)
    with pytest.raises(AssertionError):
        val.set_value_unsigned_int(-12345)
    # value that is too big for word
    with pytest.raises(AssertionError):
        val.set_value_unsigned_int(0xFFFFFFFF + 1)

def test_set_memory_value_bytes():
    """
    Tests for __bytes__
    :return:
    """

    val = MemoryValue(OpSize.BYTE)
    val.set_value_unsigned_int(100)

    x = bytes(val)
    assert (int.from_bytes(x, byteorder='big', signed=False) == 100)

    val = MemoryValue(OpSize.WORD)
    val.set_value_unsigned_int(100)

    x = bytes(val)
    assert (int.from_bytes(x, byteorder='big', signed=False) == 100)

    val = MemoryValue(OpSize.LONG)
    val.set_value_unsigned_int(100)

    x = bytes(val)
    assert (int.from_bytes(x, byteorder='big', signed=False) == 100)


def test_memory_value_str():
    """
    Tests for __str__ to ensure that it produces the correct output
    :return:
    """

    val = MemoryValue(OpSize.BYTE)
    val.set_value_unsigned_int(0xAB)

    assert (str(val) == 'MemoryValue 0xab')

    val = MemoryValue(OpSize.WORD)
    val.set_value_unsigned_int(0xABCD)

    assert (str(val) == 'MemoryValue 0xabcd')

    val = MemoryValue(OpSize.LONG)
    val.set_value_unsigned_int(0xABCD1234)

    assert (str(val) == 'MemoryValue 0xabcd1234')

def test_memory_value_get_msb():
    """
    Tests for get_msb
    :return:
    """

    val = MemoryValue(OpSize.BYTE)
    val.set_value_unsigned_int(0x01)
    assert (val.get_msb() is False)

    val.set_value_unsigned_int(0x80)
    assert (val.get_msb() is True)

    val.set_value_unsigned_int(0xFF)
    assert (val.get_msb() is True)

    val = MemoryValue(OpSize.WORD)
    val.set_value_unsigned_int(0x0100)
    assert (val.get_msb() is False)

    val.set_value_unsigned_int(0x8000)
    assert (val.get_msb() is True)

    val.set_value_unsigned_int(0xFF00)
    assert (val.get_msb() is True)

    val = MemoryValue(OpSize.LONG)
    val.set_value_unsigned_int(0x01000000)
    assert (val.get_msb() is False)

    val.set_value_unsigned_int(0x80000000)
    assert (val.get_msb() is True)

    val.set_value_unsigned_int(0xFF000000)
    assert (val.get_msb() is True)

def test_get_value_signed():
    """
    Tests for get_value_signed
    :return:
    """

    val = MemoryValue(OpSize.BYTE)
    val.set_value_unsigned_int(0x8F)
    assert (val.get_value_signed() == -113)

def test_set_value_signed():
    """
    Tests for set_value_signed
    :return:
    """

    val = MemoryValue(OpSize.BYTE)
    val.set_value_signed_int(-113)
    assert (val.get_value_signed() == -113)
    assert (val.get_value_unsigned() == 0x8F)