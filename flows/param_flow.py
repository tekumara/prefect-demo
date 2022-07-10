from prefect import State, flow, get_run_logger, task
from prefect.flows import Flow
from prefect.futures import PrefectFuture
from prefect.utilities.asyncio import Sync


@flow
def increment(i: int) -> PrefectFuture[int, Sync]:
    # logger requires a flow or task run context
    logger = get_run_logger()

    # shown in stdout but not prefect ui
    print("Hello stdout!")

    # show in prefect logs/UI
    logger.info("Hello Prefect logs!")
    logger.info(f"{i=}")

    # result is PrefectFuture[int, Sync]
    result = add_one(i)
    logger.info(f"{result=}")

    # passing the result future will resolve to its int value
    print_result(result)  # type: ignore see https://github.com/PrefectHQ/prefect/issues/5985
    return result


@task
def add_one(i: int) -> int:
    return i + 1


@task
def print_result(i: int) -> None:
    logger = get_run_logger()
    logger.info(f"print_result: {i=}")


if __name__ == "__main__":
    # to demonstrate that this is a Flow object
    f: Flow = increment

    # execute Flow
    r: State[PrefectFuture[int, Sync]] = f(1)
