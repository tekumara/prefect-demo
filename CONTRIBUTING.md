# Contributing 🌳

## Development environment

`make install` creates the dev environment with:

- git hooks for formatting & linting on git push
- a virtualenv in _.venv/_
- pyright (requires node)

`. .venv/bin/activate` activates the virtualenv.

Run `make` to see the options for running checks, tests etc. make targets that use the virtualenv will it when _setup.py_ changes.
