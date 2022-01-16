# add additional targets here

## run basic_flow
basic-flow: $(venv)
	$(venv)/bin/python -m flows.basic_flow

## start prefect ui
ui: $(venv)
	prefect orion start

include *.mk
