import cocotb
from cocotb.triggers import Timer
from hdl_utils import int_from_twos_comp

import pytest
import random
import numpy as np


@cocotb.test()
async def check_core(dut):
    width_in = len(dut.PiX0)
    width_weight = len(dut.PiW0)
    width_out = len(dut.PoZ)
    test_size = 1000

    dec_data = (4, 0, 5)
    dec_weig = (3, 2, 1)
    partial_shifts = [a + b for a, b in zip(dec_data, dec_weig)]
    total_shift = max(partial_shifts)

    dut.PiX0 <= 0
    dut.PiX1 <= 0
    dut.PiX2 <= 0
    dut.PiW0 <= 0
    dut.PiW1 <= 0
    dut.PiW2 <= 0
    for i in range(test_size):
        pix0 = random.getrandbits(width_in)
        pix1 = random.getrandbits(width_in)
        pix2 = random.getrandbits(width_in)
        piw0 = random.getrandbits(width_weight)
        piw1 = random.getrandbits(width_weight)
        piw2 = random.getrandbits(width_weight)
        pix0_value = int_from_twos_comp(pix0, width_in) / 2**dec_data[0]
        pix1_value = int_from_twos_comp(pix1, width_in) / 2**dec_data[1]
        pix2_value = int_from_twos_comp(pix2, width_in) / 2**dec_data[2]
        piw0_value = int_from_twos_comp(piw0, width_weight) / 2**dec_weig[0]
        piw1_value = int_from_twos_comp(piw1, width_weight) / 2**dec_weig[1]
        piw2_value = int_from_twos_comp(piw2, width_weight) / 2**dec_weig[2]
        dut.PiX0 <= pix0
        dut.PiX1 <= pix1
        dut.PiX2 <= pix2
        dut.PiW0 <= piw0
        dut.PiW1 <= piw1
        dut.PiW2 <= piw2
        expected = (pix0_value * piw0_value + \
                    pix1_value * piw1_value + \
                    pix2_value * piw2_value) * 2**total_shift
        await Timer(1, units='ns')
        result = dut.PoZ.value.signed_integer
        assert result == expected, f'{result} != {expected}'
