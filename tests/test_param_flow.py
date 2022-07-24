import prefect.testing.utilities
import pytest
from prefect import State
from prefect.orion.schemas.states import StateType

from flows.param_flow import add_one, increment


@pytest.fixture(scope="session")
def prefect_test_harness():
    # run flows against a temporary SQLite database rather than  ~/.prefect/orion.db
    # adds an extra second to test time
    # see https://orion-docs.prefect.io/tutorials/testing/
    with prefect.testing.utilities.prefect_test_harness():
        yield


# works as long as the task does not use anything from the prefect context (eg: loggers)
def test_underlying_fn():
    assert add_one.fn(41) == 42


@pytest.mark.skip(reason="https://github.com/PrefectHQ/prefect/issues/6049")
def test_increment(prefect_test_harness):
    meaning_of_life_future = increment(41)

    assert meaning_of_life_future.get_state().type == StateType.COMPLETED
    assert meaning_of_life_future.get_state().result() == 42


def test_increment_run(prefect_test_harness):
    state = increment._run(42)
    assert state.type == StateType.COMPLETED

    # not sure why the result is itself a state object with the actual result?
    assert type(state.result()) == State
    assert state.result().result() == 43
