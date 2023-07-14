from prefect import flow, get_run_logger


@flow
def common(config: dict) -> int:
    # show in prefect ui
    logger = get_run_logger()
    logger.info("I am a subgraph that shows up in lots of places!")
    intermediate_result = 42
    return intermediate_result


@flow
def main() -> None:
    # do some things
    # then call another flow function

    data = common(config={})
    logger = get_run_logger()
    logger.info(f"data = {data}")
    # do more things


if __name__ == "__main__":
    main()
