from prefect import State, flow
from prefect.flows import Flow


@flow
def add_one(i: int) -> int:
    return i + 1


if __name__ == "__main__":
    # to demonstrate that this is a Flow object
    f: Flow = add_one

    # execute Flow
    r: State[int] = f(1)
