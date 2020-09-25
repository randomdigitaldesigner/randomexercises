# Testbench con cocotb

Ejemplo de un testbench de un contador descrito en VHDL usando cocotb.

## Requerimientos

Requimientos:
* Simulador de VHDL: ghdl
* Framework de testbench en Python: cocotb
* Visualizador de waveforms: gtkwave

Instalar requerimientos:
```bash
# debian users:
sudo apt-get install ghdl gtkwave
# arch users:
# yay -Syu ghdl-gcc gtkwave
python3 -m pip install cocotb
```

## Uso

Archivos de entrada:
* `up_counter.vhd`: contador en VHDL
* `tb_counter.py`: testbench en Python
* `Makefile`: archivo de configuración de la simulación

Correr test:
```bash
make
```

Visualización de waveforms:
```bash
gtkwave waveform.vcd
```