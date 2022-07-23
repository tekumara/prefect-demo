import pytest
from prefect import State
from prefect.orion.schemas.states import StateType

from flows.param_flow import add_one, increment


# works as long as the task does not use anything from the prefect context (eg: loggers)
def test_underlying_fn():
    assert add_one.fn(41) == 42


@pytest.mark.skip(reason="https://github.com/PrefectHQ/prefect/issues/6049")
def test_increment():
    meaning_of_life_future = increment(41)

    assert meaning_of_life_future.get_state().type == StateType.COMPLETED
    assert meaning_of_life_future.get_state().result() == 42


def test_increment_run():
    state = increment._run(42)
    assert state.type == StateType.COMPLETED

    # not sure why the result is itself a state object with the actual result?
    assert type(state.result()) == State
    assert state.result().result() == 43
