from prefect import State, flow, get_run_logger, task
from prefect.flows import Flow
from prefect.futures import PrefectFuture
from prefect.utilities.asyncio import Sync


@flow
def add_one_with_logging(i: int) -> PrefectFuture[int, Sync]:
    # logger requires a flow or task run context
    logger = get_run_logger()
    logger.info(f"{i=}")
    return add_one(i)


@task
def add_one(i: int) -> int:
    return i + 1


if __name__ == "__main__":
    # to demonstrate that this is a Flow object
    f: Flow = add_one_with_logging

    # execute Flow
    r: State[PrefectFuture[int, Sync]] = f(1)
