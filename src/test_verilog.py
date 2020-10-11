import pytest
import os
import shutil
import shlex
from ej1 import main as ej1_main
from ej2 import main as ej2_main
from ej3 import main as ej3_main
from ej4 import main as ej4_main
from ej5 import main as ej5_main
from ej6 import main as ej6_main
from ej7 import main as ej7_main

verilog_dir = 'verilogs'

def setup_function(function):
    if not os.path.exists(verilog_dir):
        os.makedirs(verilog_dir)


def teardown_function(function):
    pass


@pytest.mark.parametrize("main, name", [(ej1_main, 'ej1'),
                                        (ej2_main, 'ej2'),
                                        (ej3_main, 'ej3'),
                                        (ej4_main, 'ej4'),
                                        (ej5_main, 'ej5'),
                                        (ej6_main, 'ej6'),
                                        (ej7_main, 'ej7'),
                                        ])
def test_generate_ej(main, name):
    filename = verilog_dir + '/' + name + '.v'
    shutil.rmtree(filename, ignore_errors=True)
    main(shlex.split(filename))
    assert os.path.exists(filename), f'Failed to generate {filename}'

