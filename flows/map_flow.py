from time import sleep
from typing import List

from prefect import flow, get_run_logger, task


@task
def setup() -> str:
    logger = get_run_logger()
    logger.info("setup start")
    sleep(3)
    logger.info("setup end")
    return "setup"


@task
def fetch_batches() -> List[str]:
    return [f"batch {i}" for i in range(10)]


@task
def count_rows(batch: str) -> int:
    logger = get_run_logger()
    logger.info(f"{batch}")
    return 1


@task
def summary(count: List[int]) -> None:
    logger = get_run_logger()
    total = sum(count)
    logger.info(f"Num batches: {len(count)} Num rows: {total}")
    return None


# map is a bit more performant than a for loop as it gathers all upstream dependencies concurrently
# but if you’re calling map without any upstream tasks as inputs, it’s probably going to be the same as a for loop
@flow
def map_flow() -> None:
    batches = fetch_batches.submit()
    counts = count_rows.map(batches, wait_for=[setup.submit()])  # type: ignore see https://github.com/PrefectHQ/prefect/issues/6922
    summary(counts)


if __name__ == "__main__":
    map_flow()
