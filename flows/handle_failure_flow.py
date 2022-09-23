from time import sleep
from typing import List

from prefect import flow, get_run_logger, task


@task
def fail() -> int:
    logger = get_run_logger()
    logger.info("Starting fail task")
    # sleep to demonstrate this runs concurrently
    sleep(3)
    raise Exception("halt and catch fire")


@task
def success() -> int:
    logger = get_run_logger()
    logger.info("Success!")
    return 42


@task
def the_end(scores: List[int]) -> None:
    logger = get_run_logger()
    logger.info(f"Final score is {sum(scores)} 🏆")


@flow
def handle_failure() -> None:
    logger = get_run_logger()
    logger.info("Starting handle failure flow")

    # start tasks asynchronously
    f = fail.submit()
    s = success.submit()

    # wait() will block and return the task state
    # we then filter to completed (ie: successful) states
    completed_states = [s for s in [f.wait(), s.wait()] if s.is_completed()]

    # NB: unlike @task(trigger=any_successful) in Prefect 1 the dag is dynamically
    # constructed at runtime and so the_end will not have an upstream edge to the failed task
    the_end.submit(completed_states)  # type: ignore


if __name__ == "__main__":
    handle_failure()
