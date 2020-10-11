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
    top = Truncador(width_in=args.width_in,
                    width_out=args.width_out)
    ports = [top.input, top.output]
    with open(filename, "w") as f:
        f.write(verilog.convert(top, ports=ports))


if __name__ == '__main__':
    main()