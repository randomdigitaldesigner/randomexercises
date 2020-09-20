from nmigen_cocotb import run
import pytest


@pytest.mark.parametrize("width", [8, 16])
def test_ej1(width):
    from ej1 import Suma6
    core = Suma6(width)
    ports = core.inputs
    ports.append(core.output)
    run(core, 'tb_ej1', ports=ports, vcd_file='ej1.vcd')


@pytest.mark.parametrize("width_in, width_out", [(10, 7)])
def test_ej2(width_in, width_out):
    from ej2 import Truncador
    core = Truncador(width_in=width_in, width_out=width_out)
    ports = [core.input, core.output]
    run(core, 'tb_ej2', ports=ports, vcd_file='ej2.vcd')


@pytest.mark.parametrize("width_in, width_out", [(10, 7)])
def test_ej3(width_in, width_out):
    from ej3 import RoundNearest
    core = RoundNearest(width_in=width_in, width_out=width_out)
    ports = [core.input, core.output]
    run(core, 'tb_ej3', ports=ports, vcd_file='ej3.vcd')
