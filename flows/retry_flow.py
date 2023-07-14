import prefect.context
from prefect import flow, get_run_logger, task
from prefect.context import get_run_context


@task(retries=2)
def unreliable_task() -> None:
    logger = get_run_logger()
    ctx: prefect.context.TaskRunContext = get_run_context()  # type: ignore
    run_count = ctx.task_run.run_count
    logger.info(f"Starting unreliable task {run_count=}")
    if run_count == 1:
        raise Exception("halt and catch fire")


@task
def the_end() -> None:
    logger = get_run_logger()
    logger.info("We reached the end!")


@flow
def retry() -> None:
    logger = get_run_logger()
    logger.info("Starting failing flow")
    f = unreliable_task.submit()
    the_end.submit(wait_for=[f])  # type: ignore see https://github.com/PrefectHQ/prefect/issues/5762


# TODO: deploy and test on Kubes

if __name__ == "__main__":
    retry()
