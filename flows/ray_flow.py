from typing import List

from prefect import flow, task
from prefect_ray.task_runners import RayTaskRunner


@task
def say_hello(name: str) -> None:
    print(f"hello {name}")


@task
def say_goodbye(name: str) -> None:
    print(f"goodbye {name}")


# run on an existing ray cluster
@flow(
    task_runner=RayTaskRunner(
        address="ray://127.0.0.1:10001",
        init_kwargs={"runtime_env": {"pip": ["prefect==2.0b8"]}},
    )
)
def greetings(names: List[str]) -> None:
    for name in names:
        say_hello(name)
        say_goodbye(name)


if __name__ == "__main__":
    greetings(["arthur", "trillian", "ford", "marvin"])
