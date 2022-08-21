# Orion Demo

Prefect Orion examples running self-contained in a local kubernetes cluster. Batteries (mostly) included. 🔋

## Getting started

Prerequisites:

- make
- node (required for pyright)
- python >= 3.9
- docker & docker compose
- [k3d](https://k3d.io/) (for creating a local kubernetes cluster)
- kubectl
- helm

To start:

- Install the [development environment](CONTRIBUTING.md#Development-environment): `make install`

## Examples

Flows

- [Dask flow](flows/dask_flow.py) using a dask local cluster
- [Dask kubes flow](flows/dask_kubes_flow.py) using an ephemeral dask cluster on Kubernetes
- [Parameterized flow](flows/param_flow.py) using a custom Docker image containing additional modules
- [Ray flow](flows/ray_flow.py) that runs on an existing ray cluster (see [tekumara/ray-demo](https://github.com/tekumara/ray-demo))
- [Sub flow](flows/sub_flow.py) that is trigger by a parent flow
- [Submit flow](flows/submit.py) demonstrates the difference of running tasks with/without `.submit()`

[Deployment](flows/deploy.py) to Kubernetes using an S3 block to store the flow in minio.

## Usage

### Local

1. `make param-flow` or `make dask-flow` or `make ray-flow` or `make sub-flow`
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

## Docs

- [Blocks](blocks.md) - an overview and look into the database tables for Blocks.
- [Deployment](deployment.md) - an overview of the deployment process.

## References

- [Orion tutorials](https://orion-docs.prefect.io/tutorials/first-steps/) from which some of the examples are taken

## Cloud

To run flows with a cloud workspace set:

```
export PREFECT_API_URL=https://api-beta.prefect.io/api/accounts/$accountid/workspaces/$workspaceid
export PREFECT_API_KEY=<your api key>
```

`$accountid` and `$workspaceid` are visible in the URL when you login to Prefect Cloud. The api key can be created from your user profile (bottom left).

Setting the environment variables is recommended. An alternative method is to login using:

```
prefect cloud login --key <your api key>
```

However be aware that this stores your api url and key as plain text _~/.prefect/profiles.toml_.

## Known issues

- [Support flat mapping #6462](https://github.com/PrefectHQ/prefect/issues/6462)
- [Logs configured in tasks with get_run_logger using DaskTaskRunner don't make it to the Prefect 2.0 backend #5850](https://github.com/PrefectHQ/prefect/issues/5850)
- [Ray task runner logs missing #25](https://github.com/PrefectHQ/prefect-ray/issues/25)
- [FileNotFoundError errors when running with a remote ray cluster #26](https://github.com/PrefectHQ/prefect-ray/issues/26)
- [There is no visibility of agents in the UI #6256](https://github.com/PrefectHQ/prefect/issues/6256)
- Deployments with a remote file system will upload the entire contents of the current directory (excluding .prefectignore and hidden files/directories) to storage (eg: S3). The destination will be overwritten and isn't prefixed per deployment. See [#6320](https://github.com/PrefectHQ/prefect/issues/6320)
- `prefect deployment build` does not provide a mechanism for supplying parameters. See [#6304](https://github.com/PrefectHQ/prefect/issues/6304).
- [Module import fails when deploying using Deployment.build_from_flow and remote storage #6469](https://github.com/PrefectHQ/prefect/issues/6469)

## Troubleshooting

### Flows are late

Check the logs of the agent:

```
make kubes-logs
```

## Todo

- Use service account in Kubes
- [task.map example](https://github.com/PrefectHQ/prefect/pull/6112/files)
