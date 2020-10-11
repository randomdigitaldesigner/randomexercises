from nmigen import *


def sum_saturate(a, b):
    """
    equivalente VHDL:
    a: std_logic_vector(N-1 downto 0)
    max_a: constante con valor (2^(N-1) - 1)
    b: constante
    x: constante Signed con valor (2^(N-1) - 1 - b)

    wrapped_sum <= std_logic_vector(signed(a) + to_signed(b, N))
    result <= wrapped_sum WHEN signed(a) < to_signed(x, N) ELSE
              max_a;
    """
    w = len(a)
    wrapped_sum = (a.as_signed() + b)[:w]
    max_a = 2**(w - 1) - 1
    result = Mux(a.as_signed() < max_a - b, wrapped_sum, max_a)
    return result


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


def main(cmd_args=None):
    import argparse
    from nmigen.back import verilog
    parser = argparse.ArgumentParser()
    parser.add_argument('--width-in', '-wi', type=int, default=10,
                        help='Input port width')
    parser.add_argument('--width-out', '-wo', type=int, default=7,
                        help='Output port width')
    parser.add_argument('output', type=str, help='Output file (Verilog)')
    args = parser.parse_args(cmd_args)
    filename = args.output if args.output.endswith('.v') else args.output + '.v'
    top = RoundNearest(width_in=args.width_in, width_out=args.width_out)
    ports = [top.input, top.output]
    with open(filename, "w") as f:
        f.write(verilog.convert(top, ports=ports))


if __name__ == '__main__':
    main()