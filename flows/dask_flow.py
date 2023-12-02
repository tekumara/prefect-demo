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


# TODO: can the task runner be parameterised so we don't duplicate the flow with dask_kubes_flow?
# see https://github.com/PrefectHQ/prefect/issues/5560
@flow(task_runner=DaskTaskRunner())
def dask(names: list[str]) -> None:
    for name in names:
        # tasks must be submitted to run on dask
        # if called without .submit() they are still tracked but
        # run immediately and locally rather than async on dask
        say_hello.submit(name)
        say_goodbye.submit(name)


if __name__ == "__main__":
    dask(["arthur", "trillian", "ford", "marvin"])
