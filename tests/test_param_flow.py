from prefect import State
from prefect.futures import PrefectFuture
from prefect.orion.schemas.states import StateType
from prefect.utilities.asyncio import Sync

from flows.param_flow import add_one, increment


# works as long as the task does not use anything from the prefect context (eg: loggers)
def test_underlying_fn():
    assert add_one.fn(41) == 42


def test_flow():
    state: State[PrefectFuture[int, Sync]] = increment(41)
    assert state.type == StateType.COMPLETED

    assert state.result().result() == 42
