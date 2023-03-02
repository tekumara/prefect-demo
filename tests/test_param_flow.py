import prefect.testing.utilities
import pytest
from prefect import State  # pyright: ignore[reportPrivateImportUsage]
from prefect.server.schemas.states import StateType

from flows.param_flow import add_one, increment


@pytest.fixture(scope="session")
def prefect_test_harness():
    # run flows against a temporary SQLite database rather than ~/.prefect/prefect.db
    # adds an extra second to test time
    # see https://docs.prefect.io/tutorials/testing/
    with prefect.testing.utilities.prefect_test_harness():
        yield


# works as long as the task does not use anything from the prefect context (eg: loggers)
def test_underlying_fn():
    assert add_one.fn(41) == 42


def test_increment(prefect_test_harness):
    state: State = increment(42)  # type: ignore see https://github.com/PrefectHQ/prefect/issues/6049

    assert state.type == StateType.COMPLETED
    assert state.result() == 43
