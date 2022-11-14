TEST_DIR =tests
COV=-

ODIR=obj
LDIR =libraries

.PHONY: clean, experiment, pytest

# default
all: sim
	@echo "Make all"

# Show help
help:
	@awk -f make-help.awk Makefile

# run Simulator
sim:
	@echo "Run"
	@./main.py; read -p "Close:" module;

clean:
	@echo "Clean"

# run pytest
pytest:
	@pytest -cov=$(COV) tests
