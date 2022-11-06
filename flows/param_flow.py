from prefect import flow, get_run_logger, task
from prefect.flows import Flow
from prefect.futures import PrefectFuture
from prefect.states import State  # pyright: ignore[reportPrivateImportUsage]
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

    number = add_one.submit(i)

    # print number which is a unresolved PrefectFuture
    logger.info(f"unresolved {number=}")

    # passing the number future will resolve to its int value when the task runs
    print_number.submit(number)  # type: ignore see https://github.com/PrefectHQ/prefect/issues/5985

    # despite this failing task, this flow's final state will be "completed" (ie: success),
    # because we return a future from the flow
    fail.submit()

    # return the number future, which determines the final state of the flow
    # see https://docs.prefect.io/concepts/states/#final-state-determination
    return number


@task
def add_one(i: int) -> int:
    return i + 1


@task
def fail() -> int:
    logger = get_run_logger()
    logger.info("Starting fail task")
    raise Exception("halt and catch fire")


@task
def print_number(i: int) -> None:
    logger = get_run_logger()
    logger.info(f"{i=}")


if __name__ == "__main__":
    # to demonstrate that this is a Flow object
    f: Flow = increment

    # execute Flow, the number future returned from the flow is resolved to a State
    r: State = f(1)  # type: ignore see https://github.com/PrefectHQ/prefect/issues/6049
    print(repr(r))
