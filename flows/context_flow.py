import prefect
from prefect import task, flow, get_run_logger
from prefect.context import get_run_context
import prefect.context

@task
def log_context() -> None:
    logger = get_run_logger()

    ctx: prefect.context.TaskRunContext = get_run_context()  # type: ignore
    logger.info(f"{ctx.task_run.start_time=}")
    logger.info(f"{ctx.task_run.flow_run_id=}")

    # no guarantees that this will be available inside a task and not recreated
    # when task runs are executed remotely
    flow_ctx = prefect.context.FlowRunContext.get()

    logger.info(f"{flow_ctx.flow.name=}")   # pyright: ignore[reportOptionalMemberAccess]


@flow
def hello() -> None:
    logger = get_run_logger()
    logger.info("Starting hello flow")
    log_context()

if __name__ == "__main__":
    hello()
