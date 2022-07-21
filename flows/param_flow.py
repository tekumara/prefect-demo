from prefect import flow, get_run_logger, task
from prefect.flows import Flow

import flows.another_module


@flow
def increment(i: int) -> int:
    """A parameterised flow that references other modules"""

    # logger requires a flow or task run context
    logger = get_run_logger()

    # shown in stdout but not prefect ui
    print("Hello stdout!")

    # show in prefect logs/UI
    logger.info("Hello Prefect logs!")
    logger.info(flows.another_module.msg)
    logger.info(f"{i=}")

    # result is int
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

    # execute Flow, returns int
    r = f(1)
