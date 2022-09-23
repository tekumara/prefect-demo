from prefect import State, flow, get_run_logger, task
from prefect.flows import Flow
from prefect.futures import PrefectFuture
from prefect.utilities.asyncutils import Sync

import flows.another_module


@flow
def increment(i: int) -> PrefectFuture[int, Sync]:
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
    result = add_one.submit(i)
    logger.info(f"{result=}")

    # passing the result future will resolve to its int value
    print_result.submit(result)  # type: ignore see https://github.com/PrefectHQ/prefect/issues/5985

    # despite this failing task, this flow's final state will be "completed" (ie: success),
    # because we return result from the flow
    fail.submit()

    # return the result future, which determines the final state of the flow
    # see https://docs.prefect.io/concepts/states/#final-state-determination
    return result


@task
def add_one(i: int) -> int:
    return i + 1


@task
def fail() -> int:
    logger = get_run_logger()
    logger.info("Starting fail task")
    raise Exception("halt and catch fire")


@task
def print_result(i: int) -> None:
    logger = get_run_logger()
    logger.info(f"print_result: {i=}")


if __name__ == "__main__":
    # to demonstrate that this is a Flow object
    f: Flow = increment

    # execute Flow, the result future returned from the flow is resolved to a State
    r: State = f(1)  # type: ignore see https://github.com/PrefectHQ/prefect/issues/6049
    print(repr(r))
