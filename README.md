# flows

Prefect Orion examples

## Development

### Prerequisites

- make
- node (required for pyright. Install via `brew install node`)
- python >= 3.7

### Getting started

To get started run `make install`. This will:

- install git hooks for formatting & linting on git push
- create the virtualenv in _.venv/_
- install this package in editable mode

Then run `make` to see the options for running checks, tests etc.

`. .venv/bin/activate` activates the virtualenv. When the requirements in `setup.py` change, the virtualenv is updated by the make targets that use the virtualenv.
