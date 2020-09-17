import cocotb
from cocotb.triggers import Timer

import pytest
import random


def set_inputs(dut, data):
    assert len(data) == 6
    dut.input_0 <= data[0]
    dut.input_1 <= data[1]
    dut.input_2 <= data[2]
    dut.input_3 <= data[3]
    dut.input_4 <= data[4]
    dut.input_5 <= data[5]


@cocotb.test()
async def adder6(dut):
    width = len(dut.input_0)
    length = 10
    
    set_inputs(dut, [0 for _ in range(6)])
    for i in range(length):
        data = [random.getrandbits(width) for _ in range(6)]
        expected = sum(data)
        set_inputs(dut, data)
        await Timer(1, units='ns')
        results = int(dut.output.value)
        assert results == expected, f'{results} != {expected}'
