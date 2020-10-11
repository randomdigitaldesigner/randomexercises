import cocotb
from cocotb.triggers import Timer
from hdl_utils import int_from_twos_comp, twos_comp_from_int
from tb_ej3 import saturate
from tb_ej4 import round_convergent

import pytest
import random
import numpy as np
from math import ceil, log2


@cocotb.test()
async def check_core(dut):
    width_in = len(dut.input)
    width_gain = len(dut.gain)
    width_out = len(dut.output)
    max_gain = 10
    gain_required_bits = int(ceil(log2(max_gain + 1)))
    gain_decimal_bits = width_gain - gain_required_bits
    gain_shift = gain_decimal_bits
    shift = width_in - width_out
    limits = (-2**(width_out - 1), +2**(width_out - 1) - 1)
    test_size = 1000

    dut.input <= 0
    dut.gain <= 0
    for i in range(test_size):
        pix = random.getrandbits(width_in)
        pig = random.getrandbits(width_gain)
        pix_signed = int_from_twos_comp(pix, width_in)
        dut.input <= pix
        dut.gain <= pig
        gain = saturate(pig / 2**gain_decimal_bits, (0, 10))
        expected = saturate(round_convergent(pix_signed * gain), limits)
        await Timer(1, units='ns')
        result = dut.output.value.signed_integer
        # print(f'pix={pix_signed:15} (0b {twos_comp_from_int(pix_signed, 12):>012b})')
        # print(f'pig={pig:15} (0b {twos_comp_from_int(pig, 11):>010b})')
        # print(f'expected={expected:15} (0b {twos_comp_from_int(expected, 14):>014b})')
        # print(f'result={result:15} (0b {twos_comp_from_int(result, 14):>014b})')
        assert result == expected, f'{result} != {expected}'
