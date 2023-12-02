import asyncio
import logging

import pendulum
from prefect import get_client
from prefect.client.schemas.filters import LogFilter
from prefect.deployments.deployments import run_deployment
from prefect.server.schemas.states import StateType


async def main() -> None:
    async with get_client() as client:
        deployments = ["param/yaml", "retry/yaml", "dask-kubes/python", "parent/python"]

        failure = False
        for fut in asyncio.as_completed([run_deployment(name=d, client=client) for d in deployments], timeout=120):
            run = await fut
            flow = await client.read_flow(run.flow_id)
            print(f"---- {flow.name}/{run.name} {run.state_type} {run.estimated_run_time.seconds}s ----")

            if run.state_type != StateType.COMPLETED:
                first_page = await client.read_logs(
                    log_filter=LogFilter(flow_run_id={"any_": [run.id]}),
                )
                print()
                for log in first_page:  # type: ignore see https://github.com/PrefectHQ/prefect/issues/11302
                    print(
                        # Print following the flow run format (declared in logging.yml)
                        f"{pendulum.instance(log.timestamp).to_datetime_string()}.{log.timestamp.microsecond // 1000:03d} |"  # noqa: E501
                        f" {logging.getLevelName(log.level):7s} | Flow run"
                        f" {run.name!r} - {log.message}"
                    )
                print()
                failure = True
        if failure:
            raise SystemExit("\nFlow failure")


if __name__ == "__main__":
    asyncio.run(main())
