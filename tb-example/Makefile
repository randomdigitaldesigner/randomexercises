# ghdl is the VHDL simulator.
SIM=ghdl
# Here add all VHDL the project sources
VHDL_SOURCES = $(PWD)/up_counter.vhd
# TOPLEVEL is the name of the toplevel module in your Verilog or VHDL file:
TOPLEVEL=up_counter
# MODULE is the name of the Python test file:
MODULE=tb_counter
# Necessary to have synopsys ieee lib available
COMPILE_ARGS=--ieee=synopsys

SIM_ARGS=--vcd=waveform.vcd

include $(shell cocotb-config --makefiles)/Makefile.sim