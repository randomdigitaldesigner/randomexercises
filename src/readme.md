# TP aritmética

Fuentes: https://github.com/randomdigitaldesigner/randomexercises/tree/master/src

Lista de archivos:

```bash
src/
├── ej1.py # HDL ej1
├── ej2.py # HDL ej2
├── ej3.py # HDL ej3
├── ej4.py # HDL ej4
├── ej5.py # HDL ej5
├── ej6.py # HDL ej6
├── ej7.py # HDL ej7
├── hdl_utils.py
├── tb_ej1.py # Testbech ej1
├── tb_ej2.py # Testbech ej2
├── tb_ej3.py # Testbech ej3
├── tb_ej4.py # Testbech ej4
├── tb_ej5.py # Testbech ej5
├── tb_ej6.py # Testbech ej6
├── tb_ej7.py # Testbech ej7
├── test_ejs.py
└── test_verilog.py
```

## Requerimientos

* Simulador de Verilog: iverilog
* Visualizador de waveforms: gtkwave
* Framework de testbench en Python: cocotb
* Para generar Verilog: nmigen
* Para integrar nmigen y cocotb: nmigen-cocotb

## Uso

Clonar el repositorio e ir a la carpeta con el ejemplo:
```bash
git clone https://github.com/randomdigitaldesigner/randomexercises
cd randomexercises/src
```

Instalar requerimientos:
```bash
sudo apt-get install iverilog gtkwave
python3 -m pip install -r requirements.txt
```

Correr tests:
```bash
python3 -m pytest -vs . --log-cli-level info
# verilogs en carpeta verilog/
# waveforms en carpeta wafeform/
```

Visualización de waveforms:
```bash
gtkwave <waveform.vcd>
```

Generar verilog individualmente (los tests los generan igual para simular):
```bash
# ejemplo: generacion de ej1
python3 ej1.py --width 8 ej1.v
```