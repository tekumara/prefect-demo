from typing import List

import dask_kubernetes
from dask_kubernetes import make_pod_spec
from kubernetes.client import V1Pod
from prefect import flow, get_run_logger, task
from prefect_dask.task_runners import DaskTaskRunner


@task
def say_hello(name: str) -> None:
    # logs are sometimes dropped see https://github.com/PrefectHQ/prefect/issues/6872
    logger = get_run_logger()
    logger.info(f"hello {name}")


@task
def say_goodbye(name: str) -> None:
    logger = get_run_logger()
    logger.info(f"goodbye {name}")


# see https://kubernetes.dask.org/en/latest/
def dask_pod_spec() -> V1Pod:
    return make_pod_spec(
        # we need a image containing dask + prefect
        image="prefect-registry:5550/flow:latest",
        # image="ghcr.io/dask/dask:latest",
        # env={"EXTRA_PIP_PACKAGES": "prefect==2.10.21"},
        memory_limit="1G",
        memory_request="1G",
        cpu_limit=1,
        cpu_request=1,
        # this is how to specify a service account for the dask pods
        # if not specified Kube will use the service account called `default`
        extra_pod_config={"serviceAccountName": "prefect-flows"},
    )


@flow(
    task_runner=DaskTaskRunner(
        cluster_class=dask_kubernetes.KubeCluster,
        cluster_kwargs={"pod_template": dask_pod_spec()},
        adapt_kwargs={"minimum": 1, "maximum": 2},
    )
)
def dask_kubes(names: List[str]) -> None:
    for name in names:
        # tasks must be submitted to run on dask
        # if called without .submit() they are still tracked but
        # run immediately and locally rather than async on dask
        say_hello.submit(name)
        say_goodbye.submit(name)


if __name__ == "__main__":
    dask_kubes(["arthur", "trillian", "ford", "marvin"])
