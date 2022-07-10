from typing import List

from prefect import flow, task
from prefect_dask.task_runners import DaskTaskRunner


@task
def say_hello(name: str) -> None:
    print(f"hello {name}")


@task
def say_goodbye(name: str) -> None:
    print(f"goodbye {name}")


@flow(task_runner=DaskTaskRunner())
def greetings(names: List[str]) -> None:
    for name in names:
        say_hello(name)
        say_goodbye(name)


if __name__ == "__main__":
    greetings(["arthur", "trillian", "ford", "marvin"])
