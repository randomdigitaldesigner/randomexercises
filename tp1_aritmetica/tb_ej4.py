import cocotb
from cocotb.triggers import Timer
from hdl_utils import int_from_twos_comp
from tb_ej3 import saturate

import pytest
import random
from math import floor, ceil


def round_convergent(value):
    if abs(value - int(value)) == 0.5:
        if floor(value) % 2 == 0:
            return int(floor(value)) # even
        else:
            return int(ceil(value)) # odd
    else:
        return int(round(value))


@cocotb.test()
async def check_core(dut):
    width_in = len(dut.input)
    width_out = len(dut.output)
    shift = width_in - width_out
    limits = (-2**(width_out - 1), +2**(width_out - 1) - 1)

    dut.input <= 0
    for i in range(2**width_in):
        dut.input <= i
        di_signed = int_from_twos_comp(i, width_in)
        expected = saturate(round_convergent(di_signed / 2**shift), limits)
        await Timer(1, units='ns')
        result = dut.output.value.signed_integer
        print(f'        in={bin(i)}, out={bin(result)}, exp={bin(expected)}')
        print(f'        input={di_signed}, output={bin(result)}, exp={bin(expected)}')
        assert result == expected, f'{result} != {expected}'
