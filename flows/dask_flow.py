from typing import List

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


# TODO: can the task runner be parameterised so we don't duplicate the flow?
@flow(task_runner=DaskTaskRunner())
def greetings(names: List[str]) -> None:
    for name in names:
        say_hello(name)
        say_goodbye(name)


if __name__ == "__main__":
    greetings(["arthur", "trillian", "ford", "marvin"])
