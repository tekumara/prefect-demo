from prefect import State
from prefect.orion.schemas.states import StateType

from flows.basic_flow import add_one


def test_underlying_fn():
    assert add_one.fn(41) == 42


def test_with_state():
    state: State[int] = add_one(41)
    assert state.type == StateType.COMPLETED

    assert state.result() == 42
