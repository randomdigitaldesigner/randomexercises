from nmigen import *


class Suma6(Elaboratable):

    def __init__(self, width):
        self.width = width
        self.inputs = [Signal(width, name='input_' + str(i)) for i in range(6)]
        self.output = Signal(width + 3) # width + int(ceil(log2(6))))

    def elaborate(self, platform):
        m = Module() # creo un module

        # Defino sumas parciales. El resultado de esto es una senial que 
        # tiene la cantidad de bits necesaria para que entre el resultado.
        # Hasta no asignarlo a una senial definida, eso no molesta.
        partial_sum_0 = self.inputs[0] + self.inputs[1]
        partial_sum_1 = self.inputs[2] + self.inputs[3]
        partial_sum_2 = self.inputs[4] + self.inputs[5]

        # De igual manera, defino la suma final.
        resultado = partial_sum_0 + partial_sum_1 + partial_sum_2

        # Ahora si! Voy a asignar esto a la funcion de salida.
        # Si las longitudes de las seniales no coinciden, puedo usar
        # .as_unsigned() o .as_signed() para que extienda con ceros o con el
        # bit de signo.

        # En este caso no me interesa el signo. Solo me aseguro que la senial
        # a asignar tenga el tamanio que le asigne aprovechando un lenguaje
        # bello como es Python
        assert len(resultado) == len(self.output)

        # Ahora si, estamos listos para asignar la salida.
        # m.d.comb es el dominio "combinacional" de mi disenio. Siempre existe
        # y es equivalente a hacer cualquier asignacion combinacional.
        m.d.comb += self.output.eq(resultado)

        # Cosas del lenguaje, tenemos que devolver el "Module" que creamos
        return m


def main(cmd_args=None):
    import argparse
    from nmigen.back import verilog
    parser = argparse.ArgumentParser()
    parser.add_argument('--width', '-w', type=int, default=8,
                        help='Input ports width')
    parser.add_argument('output', type=str, help='Output file (Verilog)')
    args = parser.parse_args(cmd_args)
    filename = args.output if args.output.endswith('.v') else args.output + '.v'
    top = Suma6(width=args.width)
    ports = top.inputs
    ports.append(top.output)
    with open(filename, "w") as f:
        f.write(verilog.convert(top, ports=ports))


# llamando a este script se genera el verilog!
if __name__ == '__main__':
    main()