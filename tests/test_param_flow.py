from prefect.orion.schemas.states import StateType

from flows.param_flow import add_one, increment


# works as long as the task does not use anything from the prefect context (eg: loggers)
def test_underlying_fn():
    assert add_one.fn(41) == 42


def test_flow():
    meaning_of_life = increment(41)
    assert meaning_of_life == 42

    state = increment._run(42)
    assert state.type == StateType.COMPLETED

    assert state.result() == 43
