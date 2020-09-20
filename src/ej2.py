from nmigen import *


class Truncador(Elaboratable):

    def __init__(self, width_in, width_out):
        self.input = Signal(width_in)
        self.output = Signal(width_out)

    def elaborate(self, platform):
        m = Module() # creo un module

        # Trunco y me quedo con los MSB. Que se interpreta como fraccion y que
        # como entero es problema del de afuera.
        width_out = len(self.output)
        m.d.comb += self.output.eq(self.input[-width_out:])

        return m


# si llamas este script, genera el verilog para el caso de 8 bits
if __name__ == '__main__':
    from nmigen.back import verilog
    top = Truncador(width_in=10, width_out=7)
    ports = [top.input, top.output]
    with open("trunc.v", "w") as f:
        f.write(verilog.convert(top, ports=ports))