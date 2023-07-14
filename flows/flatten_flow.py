from typing import List, Tuple

from prefect import flow, get_run_logger, task


@task
def setup() -> str:
    logger = get_run_logger()
    logger.info("setup")
    return "done"


@task
def fetch_batches() -> List[str]:
    return [f"batch {i}" for i in range(10)]


@task
def repartition_batches(batch: str) -> List[List[str]]:
    logger = get_run_logger()
    batch_size = 4
    materialised = [f"{batch}-{i}" for i in range(8)]
    repartitioned = [materialised[i : i + batch_size] for i in range(0, len(materialised), batch_size)]
    logger.info(f"Breaking result batch of size {len(materialised)} into {len(repartitioned)} batches")
    return repartitioned


@task
def count_rows(batch: List[str]) -> int:
    logger = get_run_logger()
    logger.info(batch)
    return len(batch)


@task
def summary(count: List[int]) -> Tuple[int, int]:
    logger = get_run_logger()
    logger.info(f"{count} Num batches: {len(count)} Num rows: {sum(count)}")
    return len(count), sum(count)


@flow
def flatten() -> None:
    logger = get_run_logger()
    # 10 batches
    batches = fetch_batches.submit()

    # split each batch into 2 sub batches each, with 4 row in each sub batch
    balanced_batches = repartition_batches.map(batches)  # type: ignore see https://github.com/PrefectHQ/prefect/issues/6922
    # extract setup.submit() from the list expression so it only gets called once for all batches
    setup_future = setup.submit()
    count = [count_rows.map(batch, wait_for=[setup_future]) for batch in balanced_batches]  # type: ignore
    flatten_count = [batch for group in count for batch in group]
    # summary: [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4] Num batches: 20 Num rows: 80
    b, r = summary.submit(flatten_count).result()
    logger.info(f"{b},{r}")


if __name__ == "__main__":
    flatten()
