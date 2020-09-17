import cocotb
from cocotb.triggers import Timer
from hdl_utils import int_from_twos_comp

import pytest
import random
from math import floor


@cocotb.test()
async def trunc(dut):
    width_in = len(dut.input)
    width_out = len(dut.output)
    shift = width_out - width_in

    dut.input <= 0
    for i in range(2**width_in):
        dut.input <= i
        di_signed = int_from_twos_comp(i, width_in)
        expected = floor(di_signed / 8) # or: di_signed >> shift
        await Timer(1, units='ns')
        result = dut.output.value.signed_integer
        assert result == expected, f'{result} != {expected}'
