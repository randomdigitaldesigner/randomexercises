from nmigen_cocotb import run
from ej1 import Suma6
import pytest


@pytest.mark.parametrize("width", [8, 16])
def test_suma6(width):
    core = Suma6(width)
    ports = core.inputs
    ports.append(core.output)
    run(core, 'tb_ej1', ports=ports, vcd_file='ej1.vcd')

