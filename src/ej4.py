from nmigen import *
from ej3 import RoundNearest, sum_saturate


_one = Const(1, 1)
_zero = Const(0, 1)


class RoundConvergent(Elaboratable):

    def __init__(self, width_in, width_out):
        self.input = Signal(width_in)
        self.output = Signal(width_out)

    def elaborate(self, platform):
        m = Module() # creo un module

        wi = len(self.input)
        wo = len(self.output)
        diff = wi - wo

        m.submodules.nearest = nearest = RoundNearest(wi, wo)

        in_the_middle = Signal()
        truncated = Signal(signed(wo))

        dismissed_bits = self.input[:diff]
        half_of_scale = Cat(Repl(_zero, diff - 1), _one) # 100...0
        m.d.comb += in_the_middle.eq(dismissed_bits == half_of_scale)
        m.d.comb += nearest.input.eq(self.input)
        m.d.comb += truncated.eq(self.input[-wo:])

        with m.If(in_the_middle):
            with m.If(self.input[-wo] == _one):
                m.d.comb += self.output.eq(sum_saturate(truncated, _one))
            with m.Else():
                m.d.comb += self.output.eq(truncated)
        with m.Else():
            m.d.comb += self.output.eq(nearest.output)


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
    top = RoundConvergent(width_in=args.width_in, width_out=args.width_out)
    ports = [top.input, top.output]
    with open(filename, "w") as f:
        f.write(verilog.convert(top, ports=ports))


if __name__ == '__main__':
    main()
