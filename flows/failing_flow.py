import prefect.context
from prefect import flow, get_run_logger, task
from prefect.deployments import Deployment
from prefect.flow_runners import KubernetesFlowRunner


@task(retries=1)
def unreliable_task() -> None:
    logger = get_run_logger()
    task_run_context = prefect.context.TaskRunContext.get()
    if not task_run_context:
        raise TypeError("No task run context")
    run_count = task_run_context.task_run.run_count
    logger.info(f"Starting unreliable task {run_count=}")
    # TODO: find some other way to succeed on the retry,
    # as run_count is always 0, see https://github.com/PrefectHQ/prefect/issues/5763
    if run_count == 0:
        raise Exception("halt and catch fire")


@task
def the_end() -> None:
    logger = get_run_logger()
    logger.info("We reached the end!")


@flow
def failing_flow() -> None:
    logger = get_run_logger()
    logger.info("Starting failing flow")
    f = unreliable_task()
    the_end(wait_for=[f])  # type: ignore see https://github.com/PrefectHQ/prefect/issues/5762


Deployment(
    name="orion-packager",
    flow=failing_flow,
    flow_runner=KubernetesFlowRunner(),
)

if __name__ == "__main__":
    failing_flow()
