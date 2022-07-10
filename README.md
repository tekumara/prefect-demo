# Orion Demo

Prefect Orion examples running self-contained in a local kubernetes cluster. Batteries included. 🔋

## Getting started

Prerequisites:

- make
- node (required for pyright)
- python >= 3.9
- docker & docker compose
- [k3d](https://k3d.io/) (for creating a local kubernetes cluster)
- kubectl

To start:

- Install the [development environment](CONTRIBUTING.md#Development-environment): `make install`

## Usage

### Local

1. `make param-flow` or `make dask-flow` or `make ray-flow`
1. `make ui` then navigate to [http://localhost:4200/](http://localhost:4200/)

The orion sqlite database is stored in _~/.prefect/orion.db_

### Kubernetes

Create k3d cluster with an image registry, minio (for remote storage), the prefect agent and api

```
make kubes
```

Create kubes deployments and run them

```
make kubes-deploy
```

### UI

Prefect UI: [http://localhost:4200/](http://localhost:4200/)

Minio UI: [http://localhost:9001](http://localhost:9001). User: `minioadmin` pass: `minioadmin`.

### API

Prefect API: [http://localhost:4200/api/](http://localhost:4200/api/)

## References

- [Blocks](blocks.md)
- [Orion tutorials](https://orion-docs.prefect.io/tutorials/first-steps/)
