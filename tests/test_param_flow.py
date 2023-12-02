import prefect.testing.utilities
import pytest
from prefect import State
from prefect.server.schemas.states import StateType

from flows.param_flow import add_one, param


@pytest.fixture(scope="session")
def _prefect_test_harness():
    # run flows against a temporary SQLite database rather than ~/.prefect/prefect.db
    # adds an extra second to test time
    # see https://docs.prefect.io/latest/guides/testing/
    with prefect.testing.utilities.prefect_test_harness():
        yield


# works as long as the task does not use anything from the prefect context (eg: loggers)
def test_underlying_fn():
    assert add_one.fn(41) == 42


def test_increment(_prefect_test_harness: None):
    state: State = param(42)  # type: ignore see https://github.com/PrefectHQ/prefect/issues/6049

    assert state.type == StateType.COMPLETED
    assert state.result() == 43
