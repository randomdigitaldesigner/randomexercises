from nmigen import *
from ej2 import Truncador
from ej3 import RoundNearest
from ej4 import RoundConvergent


_one = Const(1, 1)
_zero = Const(0, 1)


class Mean8(Elaboratable):

    def __init__(self, width_in, width_out, rounding='convergent'):
        assert rounding in ('nearest', 'convergent', 'truncate')
        self.rounding = rounding
        self.inputs = [Signal(signed(width_in), name='input_' + str(i)) for i in range(8)]
        self.output = Signal(signed(width_out))

    def elaborate(self, platform):
        m = Module()

        wi = len(self.inputs[0])
        wo = len(self.output)
        diff = wi - wo

        # N + 1 bits
        stage_1 = [self.inputs[i] + self.inputs[i+1] for i in range(0, 8, 2)]
        # N + 2 bits
        stage_2 = [stage_1[i] + stage_1[i + 1] for i in range(0, 4, 2)]
        # N + 3 bits
        stage_3 = [stage_2[i] + stage_2[i + 1] for i in range(0, 2, 2)]

        mean = stage_3[0]
        w_mean = len(mean)

        if self.rounding == 'nearest':
            m.submodules.round_nearest = rounding = RoundNearest(w_mean, wo)
        elif self.rounding == 'convergent':
            m.submodules.round_conv = rounding = RoundConvergent(w_mean, wo)
        elif self.rounding == 'truncate':
            m.submodules.truncator = rounding = Truncador(w_mean, wo)

        m.d.comb += rounding.input.eq(mean)
        m.d.comb += self.output.eq(rounding.output)

        return m


def main(cmd_args=None):
    import argparse
    from nmigen.back import verilog
    parser = argparse.ArgumentParser()
    parser.add_argument('--width-in', '-wi', type=int, default=12,
                        help='Input port width')
    parser.add_argument('--width-out', '-wo', type=int, default=8,
                        help='Output port width')
    parser.add_argument('output', type=str, help='Output file (Verilog)')
    args = parser.parse_args(cmd_args)
    filename = args.output if args.output.endswith('.v') else args.output + '.v'
    top = Mean8(width_in=args.width_in, width_out=args.width_out)
    ports = [*top.inputs, top.output]
    with open(filename, "w") as f:
        f.write(verilog.convert(top, ports=ports))


if __name__ == '__main__':
    main()
