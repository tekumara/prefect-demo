# flows

Prefect Orion examples

## Getting started

Prerequisites:

- make
- node (required for pyright)
- python >= 3.7
- sqlite 3

To start:

- Install the [development environment](CONTRIBUTING.md#Development-environment): `make install`

## Usage

1. `make basic-flow`
1. `make ui` then navigate to [http://localhost:4200/](http://localhost:4200/)

The orion sqlite database is stored in _~/.prefect/orion.db_

### Kubernetes

Create k3d cluster

```
make cluster
```

Deploy agent and api

```
make install-kubes
```

Navigate to [http://localhost:4200/](http://localhost:4200/)

## References

- [Orion tutorials](https://orion-docs.prefect.io/tutorials/first-steps/)
