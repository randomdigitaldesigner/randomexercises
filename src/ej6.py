from nmigen import *
from ej2 import Truncador
from ej3 import RoundNearest
from ej4 import RoundConvergent
from hdl_utils import shape_limits, add_debug_signal
from math import ceil, log2


def saturate(signal, lowest, highest):
    _lowest = Const(lowest, signal.shape())
    _highest = Const(highest, signal.shape())
    return Mux(signal > _highest, _highest,
           Mux(signal < _lowest, _lowest,
               signal))


def saturate_high(signal, highest):
    _highest = Const(highest, signal.shape())
    return Mux(signal > _highest, _highest,
               signal)


class Gain(Elaboratable):

    def __init__(self, width_in, width_out, width_gain,
                 rounding='convergent'):
        assert rounding in ('nearest', 'convergent', 'truncate')
        self.rounding = rounding
        self.input = Signal(signed(width_in))
        self.gain = Signal(unsigned(width_gain))
        self.output = Signal(signed(width_out))

    def elaborate(self, platform):
        m = Module()

        wi = len(self.input)
        wg = len(self.gain)
        wo = len(self.output)

        # quiero que ganancia max sea max_gain (10):
        # si tengo wg bits, y para 10 necesito solo int(ceil(log2(10+1)))
        # el resto son "decimales". Esto significa que voy a tener el
        # resultado shifteado a la izquierda una cantidad "decimal_bits"
        max_gain = 10
        required_bits = int(ceil(log2(max_gain + 1)))
        decimal_bits = wg - required_bits
        shift = decimal_bits

        # saturo a maxima ganancia 10 el puerto de ganancia
        max_gain_signal = 10 * 2**decimal_bits
        gain_sat = saturate_high(self.gain.as_unsigned(),
                             highest=max_gain_signal)

        # esta multiplicacion tiene todos los bits necesarios para representar
        # el resultado
        product = self.input.as_signed() * gain_sat.as_unsigned()

        # saturo el resultado considerando el shifteo implicito en los
        # decimales
        _min, _max = shape_limits(signed(wo + shift))
        product_sat = saturate(product.as_signed(), _min, _max)
        assert len(product_sat) == len(product), (
            f'{len(product_sat)} == {len(product)}')

        # la saturacion de arriba la hago efectiva eliminando los MSB
        # sobrantes
        product_resized = product_sat[0:wo + shift].as_signed()
        w_prod = len(product_resized)

        # redondeo
        if self.rounding == 'nearest':
            m.submodules.round_nearest = rounding = RoundNearest(w_prod, wo)
        elif self.rounding == 'convergent':
            m.submodules.round_conv = rounding = RoundConvergent(w_prod, wo)
        elif self.rounding == 'truncate':
            m.submodules.truncator = rounding = Truncador(w_prod, wo)

        m.d.comb += rounding.input.eq(product_resized)
        m.d.comb += self.output.eq(rounding.output)

        # seniales para debuguear waveforms
        m.d.comb += add_debug_signal(gain_sat, 'gain_sat_dbg')
        m.d.comb += add_debug_signal(product, 'product_dbg')
        m.d.comb += add_debug_signal(product_sat, 'product_sat_dbg')
        m.d.comb += add_debug_signal(product_resized, 'product_resized_dbg')
        m.d.comb += add_debug_signal(rounding.output, 'rounded_dbg')

        return m


def main(cmd_args=None):
    import argparse
    from nmigen.back import verilog
    parser = argparse.ArgumentParser()
    parser.add_argument('--width-in', '-wi', type=int, default=12,
                        help='Input port width')
    parser.add_argument('--width-gain', '-wg', type=int, default=10,
                        help='Gain port width')
    parser.add_argument('--width-out', '-wo', type=int, default=14,
                        help='Output port width')
    parser.add_argument('output', type=str, help='Output file (Verilog)')
    args = parser.parse_args(cmd_args)
    filename = args.output if args.output.endswith('.v') else args.output + '.v'
    top = Gain(width_in=args.width_in, width_gain=args.width_gain,
               width_out=args.width_out)
    ports = [top.input, top.gain, top.output]
    with open(filename, "w") as f:
        f.write(verilog.convert(top, ports=ports))


if __name__ == '__main__':
    main()