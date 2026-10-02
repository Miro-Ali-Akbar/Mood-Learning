PYTHON = .venv/bin/python
FIGURES = forecast lagged_correlation long_term correlation_matrix

all: $(FIGURES)

.venv: requirements.txt
	python3 -m venv .venv
	$(PYTHON) -m pip install -r requirements.txt
	@touch .venv

data/data.csv: export.emoodsw code/preprocess.py | .venv
	@echo "Unpacking and cleaning data"
	@rm -rf data
	@mkdir -p data/raw
	@unzip -q export.emoodsw -d data/raw
	@$(PYTHON) code/preprocess.py
	@rm -r data/raw

finished/%.png: code/%.py code/style.py data/data.csv | .venv
	@echo "Making $@"
	@mkdir -p finished
	@$(PYTHON) code/$*.py

preprocess: data/data.csv

$(FIGURES): %: finished/%.png

clean:
	rm -rf data finished

.PHONY: all preprocess clean $(FIGURES)
