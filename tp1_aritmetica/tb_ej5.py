import cocotb
from cocotb.triggers import Timer
from hdl_utils import int_from_twos_comp
from tb_ej3 import saturate
from tb_ej4 import round_convergent
import logging

import pytest
import random
import numpy as np

logger = logging.getLogger(__name__)

def mean(values):
    return np.mean(values)

def get_random_inputs(width, n_inputs):
    return [random.getrandbits(width) for _ in range(n_inputs)]

def set_inputs(dut, inputs):
    for i in range(len(inputs)):
        getattr(dut, 'input_' + str(i)) <= inputs[i]


@cocotb.test()
async def check_core(dut):
    n_inputs = 8
    width_in = len(dut.input_0)
    width_out = len(dut.output)
    shift = width_in - width_out
    limits = (-2**(width_out - 1), +2**(width_out - 1) - 1)
    test_size = 1000

    set_inputs(dut, [0] * n_inputs)
    for i in range(test_size):
        inputs = get_random_inputs(width_in, n_inputs)
        inputs_signed = [int_from_twos_comp(di, width_in) for di in inputs]
        set_inputs(dut, inputs)
        expected = saturate(round_convergent(np.mean(inputs_signed) / 2**shift), limits)
        await Timer(1, units='ns')
        result = dut.output.value.signed_integer
        assert result == expected, f'{result} != {expected}'
