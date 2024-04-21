# Prefect Demo

[![ci](https://github.com/tekumara/prefect-demo/actions/workflows/ci.yml/badge.svg)](https://github.com/tekumara/prefect-demo/actions/workflows/ci.yml)

Prefect 2 (aka Orion) examples running self-contained in a local kubernetes cluster. Batteries (mostly) included. 🔋

## Getting started

Prerequisites:

- make
- node (required for pyright)
- python >= 3.10
- docker & docker compose
- [k3d](https://k3d.io/) (for creating a local kubernetes cluster)
- kubectl
- helm

To start:

- Install the [development environment](CONTRIBUTING.md#getting-started): `make install`

## Examples

Flows:

- [Dask flow](flows/dask_flow.py) using a dask local cluster
- [Dask kubes flow](flows/dask_kubes_flow.py) using an ephemeral dask cluster on Kubernetes
- [Parameterized flow](flows/param_flow.py) using a custom Docker image containing additional modules
- [Ray flow](flows/ray_flow.py) that runs on an existing ray cluster (see [tekumara/ray-demo](https://github.com/tekumara/ray-demo))
- [Sub flow](flows/sub_flow.py) that is trigger by a parent flow
- [Submit flow](flows/submit_flow.py) demonstrates the difference of running tasks with/without `.submit()`
- [Retry flow](flows/retry_flow.py) demonstrates retries when a task fails.
- [Failure flow](flows/failure_flow.py) shows how to handle a failing task.
- [Map flow](flows/map_flow.py) uses [Task.map](https://docs.prefect.io/faq/?h=map#does-prefect-2-support-mapping).
- [Flatten flow](flows/flatten_flow.py) demonstrates how to parallelise over a list of lists.
- [Parent flow](flows/parent_flow.py) shows how to [trigger a flow run from a deployment](https://annageller.medium.com/44d65b625627) within a parent flow. The triggered flow is treated as a sub flow.
- [Context flow](flows/context_flow.py) accessing [prefect context at runtime](https://docs.prefect.io/2.18.0/concepts/runtime-context/).

Deployments to Kubernetes created via:

- [Deployment objects in python](flows/deploy.py) - both local and uploaded to remote s3 storage.
- [prefect.yaml](prefect.yaml) - both local and pushed to s3.

## Usage

### Local

1. `make param-flow` or `make dask-flow` or `make ray-flow` or `make sub-flow`
1. `make ui` then navigate to [http://localhost:4200/](http://localhost:4200/)

The orion sqlite database is stored in _~/.prefect/prefect.db_

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

- [Blocks](docs/blocks.md) - an overview and look into the database tables for Blocks.
- [Deployment](docs/deployment.md) - an overview of the deployment process.

## References

- [Tutorials](https://docs.prefect.io/tutorials/first-steps/) from which some of the examples are taken

## Cloud

To run flows with a cloud workspace set:

```
export PREFECT_API_URL=https://api.prefect.cloud/api/accounts/$accountid/workspaces/$workspaceid
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
- [Zombie tasks consume concurrency slots](https://github.com/PrefectHQ/prefect/issues/5995)

Minor

- [Replicate kube events to Prefect that occur before the pod starts](https://github.com/PrefectHQ/prefect-kubernetes/issues/86)
- [Configuring different task runner for dev and prod deployments](https://github.com/PrefectHQ/prefect/issues/5560)
- [Workers only support local storage](https://github.com/PrefectHQ/prefect/discussions/10277)
- [Prefect.Deployment doesn't have a property pull_steps](https://github.com/PrefectHQ/prefect/issues/9220)
- [Support environment variables read from kubernetes secrets](https://github.com/PrefectHQ/prefect-kubernetes/issues/83)
- [Encountered error while running prefect.deployments.steps.set_working_directory - FileNotFoundError](https://github.com/PrefectHQ/prefect/issues/10285)
- [Deployment metadata](https://github.com/PrefectHQ/prefect/issues/5735)
- [Stream logs via CLI](https://github.com/PrefectHQ/prefect/issues/5987)
- [FileNotFoundError errors when running with a remote ray cluster #26](https://github.com/PrefectHQ/prefect-ray/issues/26)
- [Add Flow.submit interface for subflows on external infrastructure](https://github.com/PrefectHQ/prefect/issues/6689)
- [not a known member of module "prefect.runtime"](https://github.com/PrefectHQ/prefect/issues/9027)
- mapped tasks aren't collapsed in the UI like they were in Prefect 1
- pushing to s3 is sequential and slower than using sf3s to parallel upload to an s3 storage block

See all [roadmap tagged issues](https://github.com/PrefectHQ/prefect/labels/status%3Aroadmap) for planned work.

## Troubleshooting

### Flows are late

Check the logs of the agent/worker:

```
make kubes-logs
```
