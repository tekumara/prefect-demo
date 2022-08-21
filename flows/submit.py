import asyncio

from prefect import flow, get_run_logger, task
from prefect.task_runners import SequentialTaskRunner

"""
shout.submit runs concurrently via the default task runner (ConcurrentTaskRunner)

11:07:00.225 | INFO    | prefect.engine - Created flow run 'slick-rhino' for flow 'count-to'
11:07:00.227 | INFO    | Flow run 'slick-rhino' - Starting 'ConcurrentTaskRunner'; submitted tasks will be run concurrently...
11:07:00.349 | INFO    | Flow run 'slick-rhino' - Created task run 'shout-58a68b34-0' for task 'shout'
11:07:00.349 | INFO    | Flow run 'slick-rhino' - Submitted task run 'shout-58a68b34-0' for execution.
11:07:00.377 | INFO    | Flow run 'slick-rhino' - Created task run 'shout-58a68b34-1' for task 'shout'
11:07:00.377 | INFO    | Flow run 'slick-rhino' - Submitted task run 'shout-58a68b34-1' for execution.
11:07:00.391 | INFO    | Task run 'shout-58a68b34-0' - shout begin number=0
11:07:00.410 | INFO    | Flow run 'slick-rhino' - Created task run 'shout-58a68b34-2' for task 'shout'
11:07:00.410 | INFO    | Flow run 'slick-rhino' - Submitted task run 'shout-58a68b34-2' for execution.
11:07:00.419 | INFO    | Task run 'shout-58a68b34-1' - shout begin number=1
11:07:00.434 | INFO    | Task run 'shout-58a68b34-2' - shout begin number=2
11:07:02.391 | INFO    | Task run 'shout-58a68b34-0' - shout done  number=0
11:07:02.419 | INFO    | Task run 'shout-58a68b34-1' - shout done  number=1
11:07:02.425 | INFO    | Task run 'shout-58a68b34-0' - Finished in state Completed()
11:07:02.435 | INFO    | Task run 'shout-58a68b34-2' - shout done  number=2
11:07:02.454 | INFO    | Task run 'shout-58a68b34-1' - Finished in state Completed()
11:07:02.475 | INFO    | Task run 'shout-58a68b34-2' - Finished in state Completed()
11:07:02.524 | INFO    | Flow run 'slick-rhino' - Finished in state Completed('All states completed.')

shout - ignores the task runner and runs immediately and locally to the flow runner/infrastructure

11:09:21.698 | INFO    | prefect.engine - Created flow run 'elegant-hound' for flow 'count-to'
11:09:21.699 | INFO    | Flow run 'elegant-hound' - Starting 'ConcurrentTaskRunner'; submitted tasks will be run concurrently...
11:09:21.800 | INFO    | Flow run 'elegant-hound' - Created task run 'shout-58a68b34-0' for task 'shout'
11:09:21.800 | INFO    | Flow run 'elegant-hound' - Executing 'shout-58a68b34-0' immediately...
11:09:21.820 | INFO    | Task run 'shout-58a68b34-0' - shout begin number=0
11:09:23.821 | INFO    | Task run 'shout-58a68b34-0' - shout done  number=0
11:09:23.851 | INFO    | Task run 'shout-58a68b34-0' - Finished in state Completed()
11:09:23.869 | INFO    | Flow run 'elegant-hound' - Created task run 'shout-58a68b34-1' for task 'shout'
11:09:23.869 | INFO    | Flow run 'elegant-hound' - Executing 'shout-58a68b34-1' immediately...
11:09:23.888 | INFO    | Task run 'shout-58a68b34-1' - shout begin number=1
11:09:25.889 | INFO    | Task run 'shout-58a68b34-1' - shout done  number=1
11:09:25.917 | INFO    | Task run 'shout-58a68b34-1' - Finished in state Completed()
11:09:25.932 | INFO    | Flow run 'elegant-hound' - Created task run 'shout-58a68b34-2' for task 'shout'
11:09:25.932 | INFO    | Flow run 'elegant-hound' - Executing 'shout-58a68b34-2' immediately...
11:09:25.948 | INFO    | Task run 'shout-58a68b34-2' - shout begin number=2
11:09:27.949 | INFO    | Task run 'shout-58a68b34-2' - shout done  number=2
11:09:27.979 | INFO    | Task run 'shout-58a68b34-2' - Finished in state Completed()
11:09:28.004 | INFO    | Flow run 'elegant-hound' - Finished in state Completed('All states completed.')

shout.submit with SequentialTaskRunner - runs immediately using the SequentialTaskRunner
(useful when you want a PrefectFuture to get at the state from a task)

11:11:52.124 | INFO    | prefect.engine - Created flow run 'steadfast-earwig' for flow 'count-to'
11:11:52.125 | INFO    | Flow run 'steadfast-earwig' - Starting 'SequentialTaskRunner'; submitted tasks will be run sequentially...
11:11:52.221 | INFO    | Flow run 'steadfast-earwig' - Created task run 'shout-58a68b34-0' for task 'shout'
11:11:52.221 | INFO    | Flow run 'steadfast-earwig' - Executing 'shout-58a68b34-0' immediately...
11:11:52.242 | INFO    | Task run 'shout-58a68b34-0' - shout begin number=0
11:11:54.242 | INFO    | Task run 'shout-58a68b34-0' - shout done  number=0
11:11:54.280 | INFO    | Task run 'shout-58a68b34-0' - Finished in state Completed()
11:11:54.297 | INFO    | Flow run 'steadfast-earwig' - Created task run 'shout-58a68b34-1' for task 'shout'
11:11:54.297 | INFO    | Flow run 'steadfast-earwig' - Executing 'shout-58a68b34-1' immediately...
11:11:54.312 | INFO    | Task run 'shout-58a68b34-1' - shout begin number=1
11:11:56.312 | INFO    | Task run 'shout-58a68b34-1' - shout done  number=1
11:11:56.339 | INFO    | Task run 'shout-58a68b34-1' - Finished in state Completed()
11:11:56.355 | INFO    | Flow run 'steadfast-earwig' - Created task run 'shout-58a68b34-2' for task 'shout'
11:11:56.356 | INFO    | Flow run 'steadfast-earwig' - Executing 'shout-58a68b34-2' immediately...
11:11:56.373 | INFO    | Task run 'shout-58a68b34-2' - shout begin number=2
11:11:58.374 | INFO    | Task run 'shout-58a68b34-2' - shout done  number=2
11:11:58.414 | INFO    | Task run 'shout-58a68b34-2' - Finished in state Completed()
11:11:58.499 | INFO    | Flow run 'steadfast-earwig' - Finished in state Completed('All states completed.')

You can also mix within a flow ie: have some tasks without submit() to execute immediately and locally, and
others that run via the task runner.
"""


@task
async def shout(number: int) -> None:
    logger = get_run_logger()
    logger.info(f"shout begin {number=}")
    await asyncio.sleep(2)
    logger.info(f"shout done  {number=}")


@flow(task_runner=SequentialTaskRunner())
async def count_to(highest_number: int) -> None:
    for number in range(highest_number):
        await shout.submit(number)


asyncio.run(count_to(3))  # type: ignore see https://github.com/PrefectHQ/prefect/issues/6054
