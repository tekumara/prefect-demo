from typing import List

import dask_kubernetes
from dask_kubernetes import make_pod_spec
from kubernetes.client import V1Pod
from prefect import flow, get_run_logger, task
from prefect_dask.task_runners import DaskTaskRunner


@task
def say_hello(name: str) -> None:
    # logs not currently working see https://github.com/PrefectHQ/prefect/issues/5850
    logger = get_run_logger()
    logger.info(f"hello {name}")


@task
def say_goodbye(name: str) -> None:
    logger = get_run_logger()
    logger.info(f"goodbye {name}")


# see https://kubernetes.dask.org/en/latest/
def dask_pod_spec() -> V1Pod:
    return make_pod_spec(
        image="ghcr.io/dask/dask:latest",
        memory_limit="1G",
        memory_request="1G",
        cpu_limit=1,
        cpu_request=1,
        # this is how to specify a service account for the dask pods
        # if not specified Kube will use the service account called `default`
        extra_pod_config={"serviceAccountName": "default"},
    )


@flow(
    task_runner=DaskTaskRunner(
        cluster_class=dask_kubernetes.KubeCluster,
        cluster_kwargs={"pod_template": dask_pod_spec()},
        adapt_kwargs={"minimum": 1, "maximum": 2},
    )
)
def greetings(names: List[str]) -> None:
    for name in names:
        say_hello.submit(name)
        say_goodbye.submit(name)


if __name__ == "__main__":
    greetings(["arthur", "trillian", "ford", "marvin"])
