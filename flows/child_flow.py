from time import sleep

from prefect import flow, get_run_logger, task


@task
def sleepy() -> None:
    logger = get_run_logger()
    logger.info("Hello child!")
    logger.info("Sleeping.....")
    sleep(60)
    logger.info("Awake!")


@flow
def child() -> None:
    sleepy()


if __name__ == "__main__":
    child()
