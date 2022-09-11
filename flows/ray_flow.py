import sys
from typing import List

from prefect import flow, get_run_logger, task
from prefect_ray.task_runners import RayTaskRunner


@task
def say_hello(name: str) -> None:
    print(f"print say_hello {name}", file=sys.stderr)
    logger = get_run_logger()
    logger.info(f"hello {name}")


@task
def say_goodbye(name: str) -> None:
    print(f"print say_goodbye {name}", file=sys.stderr)
    logger = get_run_logger()
    logger.info(f"goodbye {name}")


# run on an existing ray cluster
# errors with FileNotFoundError see https://github.com/PrefectHQ/prefect-ray/issues/26
@flow(
    task_runner=RayTaskRunner(
        # 127.0.0.1:10001 is port-forwarded to the remote ray cluster
        address="ray://127.0.0.1:10001",
        init_kwargs={
            "runtime_env": {
                "pip": ["prefect==2.3.2"],
                # the PREFECT_API_* env vars in the current environment will be passed through by prefect
                # make sure PREFECT_API_URL and PREFECT_API_KEY are set to a host that can be reached
                # from the client running the flow and the ray worker node
            }
        },
    )
)
def greetings(names: List[str]) -> None:
    for name in names:
        # tasks must be submitted to run on ray
        # if called without .submit() they are still tracked but
        # run immediately and locally rather than async on ray
        say_hello.submit(name)
        say_goodbye.submit(name)


if __name__ == "__main__":
    greetings(["arthur", "trillian", "ford", "marvin"])
