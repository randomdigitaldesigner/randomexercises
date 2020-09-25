import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge
import random


CLK_PERIOD = 10


async def init_test(dut):
    """ esto es comun a todos los test asi que lo agrupo en una funcion.
    - seteo inicial de signals para que no tengan estados inciertos
    - creacion del clock
    - reset inicial
    """
    dut.enable <= 0
    cocotb.fork(Clock(dut.clk, CLK_PERIOD, 'ns').start())
    dut.reset <= 1
    await RisingEdge(dut.clk)
    dut.reset <= 0
    await RisingEdge(dut.clk)


@cocotb.test()
async def check_reset(dut):
    """ check de que tras un reset, el contador vuelve a cero
    """
    dut._log.info("Test started")
    await init_test(dut)
    for _ in range(random.randint(1, 50)):
        dut.enable <= random.randint(0, 1)
        await RisingEdge(dut.clk)
    dut.reset <= 1
    await RisingEdge(dut.clk)
    dut.reset <= 0
    assert dut.cout.value.integer == 0, 'Count is not zero after reset!'
    dut._log.info("Test finished")


@cocotb.test()
async def check_ce(dut):
    """ check de que cada vez que CE=1, la cuenta se incrementa en 1
    (volviendo a 0 al hacer overflow).
    """
    width = len(dut.cout)
    mod = 2 ** width
    dut._log.info("Test started")
    await init_test(dut)
    last_count = 0
    expected = 0
    vueltas = 0
    while vueltas < 2:
        ce = random.randint(0, 1)
        dut.enable <= ce
        await RisingEdge(dut.clk)
        assert dut.cout.value.integer == expected, (
            '{} != {}'.format(dut.cout.value.integer, expected))
        if ce:
            expected += 1
            expected %= mod
            if expected == 0:
                vueltas += 1
    dut._log.info("Test finished")