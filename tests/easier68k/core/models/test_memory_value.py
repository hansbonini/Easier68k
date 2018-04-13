"""
Tests for core/models/memory_value
which represent some value in memory with a length and a value
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
    assert (val.unsigned_value == 0xFFFFFFF)

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
