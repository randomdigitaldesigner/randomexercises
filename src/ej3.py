from nmigen import *


def sum_saturate(a, b):
    w = len(a)
    suma_con_saturacion = (a.as_signed() + b)[:w]
    max_a = 2**(w - 1) - 1
    print(f'max_a={max_a}, b={b}')
    return Mux(a.as_signed() < max_a - b, suma_con_saturacion, max_a)


class RoundNearest(Elaboratable):

    def __init__(self, width_in, width_out):
        self.input = Signal(width_in)
        self.output = Signal(width_out)

    def elaborate(self, platform):
        m = Module() # creo un module

        wi = len(self.input)
        wo = len(self.output)

        # incremento la senial de entrada en este valor para que el redondeo
        # sea al mas cercano.
        # Caso A: los "0.5" se redondean hacia el mas positivo
        _inc = (1 << (wi - wo - 1))
        # Caso B: los "0.5" se redondean hacia el mas negativo
        # _inc = (1 << (wi - wo - 1)) - 1
        offseteada = Signal(signed(wi))
        m.d.comb += offseteada.eq(sum_saturate(self.input, _inc))

        m.d.comb += self.output.eq(offseteada[-wo:])

        return m


# si llamas este script, genera el verilog!
if __name__ == '__main__':
    from nmigen.back import verilog
    top = RoundNearest(width_in=10, width_out=7)
    ports = [top.input, top.output]
    with open("round_nearest.v", "w") as f:
        f.write(verilog.convert(top, ports=ports))