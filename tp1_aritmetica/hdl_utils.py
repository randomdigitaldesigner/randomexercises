def twos_comp_from_int(val, bits):
    """compute the 2's complement of int value val"""
    assert val >= -2**(bits-1), f'{val} < -2**({bits}-1)'
    assert val < 2**(bits-1), f'{val} > 2**({bits}-1)'
    if (val & (1 << (bits - 1))) != 0: # if sign bit is set e.g., 8bit: 128-255
        val = val - (1 << bits)        # compute negative value
    return val & (2**bits-1)           # return positive value as is


def int_from_twos_comp(binary, bits):
    assert binary & (2**bits - 1) == binary, f'0b{binary:0b} & (2**{bits} - 1) == 0b{binary:0b}'
    val = binary & ~(2**(bits - 1)) 
    if binary & 2**(bits - 1): 
        val -= 2**(bits - 1) 
    return val


def shape_limits(shape):
    """
    shape contains elements signed and width
    """
    if shape.signed:
        _min = -2**(shape.width - 1)
        _max = 2**(shape.width - 1) - 1
    else:
        _min = 0
        _max = 2**shape.width - 1
    return (_min, _max)


def add_debug_signal(signal, name):
    from nmigen import Signal
    x = Signal.like(signal, name=name)
    return x.eq(signal)