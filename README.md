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
- [Retry flow](flows/retry_flow.py) demonstrates retries when a task fails.
- [Handle failure](flows/handle_failure_flow.py) shows how to handle a failing task.
- [Map flow](flows/map_flow.py) uses [Task.map](https://docs.prefect.io/faq/?h=map#does-prefect-2-support-mapping).
- [Flatten flow](flows/flatten_flow.py) demonstrates how to parallelise over a list of lists.
- [Parent flow](flows/parent_flow.py) shows how to [trigger a flow run from a deployment](https://annageller.medium.com/44d65b625627) within a parent flow. The triggered flow is treated as a sub flow.

[Deployment](flows/deploy.py) to Kubernetes:

- using an S3 block to store the flow in minio.
- using no storage and instead loading the flow from within the docker image.

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

Create deployments that run on kubernetes

```
make deploy
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

## Ray

Create a kubernetes ray cluster

```
make kubes-ray
```

Ray dashboard: [http://localhost:8265](http://localhost:8265)

## Known issues

Major

- [Support flat mapping #6462](https://github.com/PrefectHQ/prefect/issues/6462)
- [There is no visibility of agents in the UI #6256](https://github.com/PrefectHQ/prefect/issues/6256)
- [Notification for runs that do not complete after duration](https://github.com/PrefectHQ/prefect/issues/6939)
- [Zombie tasks consume concurrency slots](https://github.com/PrefectHQ/prefect/issues/5995)
- [Handle flow run restarts caused by infrastructure events](https://github.com/PrefectHQ/prefect/issues/7116)

Minor

- [Deployment metadata](https://github.com/PrefectHQ/prefect/issues/5735)
- [Stream logs via CLI](https://github.com/PrefectHQ/prefect/issues/5987)
- [report ErrImagePull in Prefect UI to improve observability](https://github.com/PrefectHQ/prefect/issues/5688)
- [FileNotFoundError errors when running with a remote ray cluster #26](https://github.com/PrefectHQ/prefect-ray/issues/26)
- [Automatically delete Kubernetes jobs after a flow run](https://github.com/PrefectHQ/prefect/issues/5755)
- [Add Flow.submit interface for subflows on external infrastructure](https://github.com/PrefectHQ/prefect/issues/6689)
- mapped tasks aren't collapsed in the UI like they were in Prefect 1

See all [roadmap tagged issues](https://github.com/PrefectHQ/prefect/labels/status%3Aroadmap) for planned work.

## Troubleshooting

### Flows are late

Check the logs of the agent:

```
make kubes-logs
```
