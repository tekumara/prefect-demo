from typing import List

from prefect import flow, get_run_logger, task
from prefect_ray.task_runners import RayTaskRunner


@task
def say_hello(name: str) -> None:
    logger = get_run_logger()
    logger.info(f"hello {name}")


@task
def say_goodbye(name: str) -> None:
    # logs not currently working see https://github.com/PrefectHQ/prefect/issues/5960
    logger = get_run_logger()
    logger.info(f"goodbye {name}")


# run on an existing ray cluster
@flow(
    task_runner=RayTaskRunner(
        address="ray://127.0.0.1:10001",
        init_kwargs={"runtime_env": {"pip": ["prefect==2.0b9"]}},
    )
)
def greetings(names: List[str]) -> None:
    for name in names:
        # tasks must be submitted to run on ray
        # if called without .submit() they are still tracked but run locally
        say_hello.submit(name)
        say_goodbye.submit(name)


if __name__ == "__main__":
    greetings(["arthur", "trillian", "ford", "marvin"])
