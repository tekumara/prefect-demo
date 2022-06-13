from prefect import State, flow, get_run_logger
from prefect.flows import Flow


@flow
def add_one(i: int) -> int:
    # logger requires a flow or task run context
    logger = get_run_logger()
    logger.info(f"{i=}")
    return i + 1


if __name__ == "__main__":
    # to demonstrate that this is a Flow object
    f: Flow = add_one

    # execute Flow
    r: State[int] = f(1)
