from nmigen import *


def add_debug_signal(signal, name):
    x = Signal.like(signal, name=name)
    return x.eq(signal)


def shift_left(signal, shift):
    return Cat(Repl(0, shift), signal)

def get_req_bits_for_sum(*args):
    min_values = [-2**(w-1) for w in args]
    max_values = [2**(w-1)-1 for w in args]
    lowest = sum(min_values)
    highest = sum(max_values)
    dummy_signal = Signal(range(lowest, highest + 1))
    return dummy_signal.shape().width


class SumaPonderada(Elaboratable):

    def __init__(self):
        M = 8
        N = 4
        _s0 = 4 + 3
        _s1 = 0 + 2
        _s2 = 5 + 1
        self.PiX0 = Signal(signed(M))
        self.PiX1 = Signal(signed(M))
        self.PiX2 = Signal(signed(M))
        self.PiW0 = Signal(signed(N))
        self.PiW1 = Signal(signed(N))
        self.PiW2 = Signal(signed(N))

        # productos intermedios
        self.y0 = self.PiX0 * self.PiW0
        self.y1 = self.PiX1 * self.PiW1
        self.y2 = self.PiX2 * self.PiW2

        # antes de la suma tengo que alinearlos asi que calculo los shifteos
        max_shift = max(_s0, _s1, _s2)
        min_shift = min(_s0, _s1, _s2)
        s0 = max_shift - _s0
        s1 = max_shift - _s1
        s2 = max_shift - _s2

        self.y0_shifted = shift_left(self.y0, s0)
        self.y1_shifted = shift_left(self.y1, s1)
        self.y2_shifted = shift_left(self.y2, s2)

        self.suma_a = self.y0_shifted.as_signed() + \
                      self.y1_shifted.as_signed()
        self.suma_b = self.suma_a + self.y2_shifted.as_signed()

        # bits requeridos para la suma
        bits = get_req_bits_for_sum(len(self.y0_shifted),
                                    len(self.y1_shifted),
                                    len(self.y2_shifted))
        self.suma = self.suma_b[:bits]

        self.PoZ = Signal.like(self.suma)

    def elaborate(self, platform):
        m = Module()

        m.d.comb += self.PoZ.eq(self.suma)

        # seniales para debuguear waveforms
        m.d.comb += add_debug_signal(self.y0, 'y0_dbg')
        m.d.comb += add_debug_signal(self.y1, 'y1_dbg')
        m.d.comb += add_debug_signal(self.y2, 'y2_dbg')
        m.d.comb += add_debug_signal(self.y0_shifted, 'y0_shifted_dbg')
        m.d.comb += add_debug_signal(self.y1_shifted, 'y1_shifted_dbg')
        m.d.comb += add_debug_signal(self.y2_shifted, 'y2_shifted_dbg')
        m.d.comb += add_debug_signal(self.suma_a, 'suma_a_dbg')
        m.d.comb += add_debug_signal(self.suma_b, 'suma_b_dbg')
        m.d.comb += add_debug_signal(self.suma, 'suma_dbg')

        return m


def main(cmd_args=None):
    import argparse
    from nmigen.back import verilog
    parser = argparse.ArgumentParser()
    parser.add_argument('output', type=str, help='Output file (Verilog)')
    args = parser.parse_args(cmd_args)
    filename = args.output if args.output.endswith('.v') else args.output + '.v'
    top = SumaPonderada()
    ports = [top.PiX0, top.PiX1, top.PiX2,
             top.PiW0, top.PiW1, top.PiW2,
             top.PoZ]
    with open(filename, "w") as f:
        f.write(verilog.convert(top, ports=ports))


if __name__ == '__main__':
    main()