from prefect import flow, get_run_logger
from prefect.deployments.deployments import run_deployment


@flow
def parent() -> None:
    logger = get_run_logger()
    logger.info("Start parent")
    _ = run_deployment(name="child/python")


if __name__ == "__main__":
    parent()
