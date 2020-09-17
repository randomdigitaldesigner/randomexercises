# Ej 1

## Install requirements

```bash
python3 -m pip install -r requirements.txt
```

## Run testbench

```bash
python3 -m pytest -vs src/
```

## Generate Verilog

```bash
python3 src/ej1.py
```

## Files hierarchy

```bash
$ tree src/
src/
├── ej1.py
├── tb_ej1.py
└── test_ejs.py

0 directories, 5 files
```

* `ej1.py`: hdl
* `tb_ej1.py`: testbench
* `test_ejs.py`: pytest wrapper to run testbenches