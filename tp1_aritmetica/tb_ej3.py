import cocotb
from cocotb.triggers import Timer
from hdl_utils import int_from_twos_comp

import pytest
import random
from math import floor, ceil

# creo my_round() porque el round() de python redondea 2.5 --> 2
# El redondeo del core es al mas cercano, y los x.5 redondean al mas
# positivo, ceil()
def my_round(value):
    if abs(value - int(value)) == 0.5:
        return ceil(value)
    else:
        return round(value)


def saturate(value, limits):
    if value > max(limits):
        return max(limits)
    elif value < min(limits):
        return min(limits)
    else:
        return value


@cocotb.test()
async def round_nearest(dut):
    width_in = len(dut.input)
    width_out = len(dut.output)
    shift = width_in - width_out
    limits = (-2**(width_out - 1), +2**(width_out - 1) - 1)

    dut.input <= 0
    for i in range(2**width_in):
        dut.input <= i
        di_signed = int_from_twos_comp(i, width_in)
        expected = saturate(my_round(di_signed / 2**shift), limits)
        await Timer(1, units='ns')
        result = dut.output.value.signed_integer
        print(f'        in={bin(i)}, out={bin(result)}, exp={bin(expected)}')
        print(f'        input={di_signed}, output={bin(result)}, exp={bin(expected)}')
        assert result == expected, f'{result} != {expected}'
