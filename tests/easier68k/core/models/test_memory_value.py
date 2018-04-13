"""
Tests for core/models/memory_value
which represent some value in memory with a length and a value
"""

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
