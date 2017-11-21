PYTHON := python3
VENV := .venv
PROJECT := example
OPTIONS := -shell-escape

build: clean $(PROJECT).pdf tidy

$(PROJECT).pdf: $(VENV)
	vex --path $(VENV) latexmk -pdf $(PROJECT) -latexoption="$(OPTIONS)"

preview: clean $(VENV)
	vex --path $(VENV) latexmk -pvc -pdf $(PROJECT)\
		-latexoption="$(OPTIONS) -quiet"

$(VENV):
	$(PYTHON) -m venv .venv
	vex --path $(VENV) pip install -r requirements.pip

tidy:
	latexmk -c

clean:
	latexmk -C

.PHONY: build preview tidy clean
