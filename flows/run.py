import asyncio

from prefect.client.schemas.objects import FlowRun
from prefect.deployments.deployments import run_deployment
from prefect.server.schemas.states import StateType


async def main() -> None:
    deployments = ["param/yaml", "retry/yaml", "dask-kubes/python", "parent/python"]

    flow_runs: list[FlowRun] = await asyncio.gather(*[run_deployment(name=d) for d in deployments])

    for f in flow_runs:
        assert f.state_type == StateType.COMPLETED


if __name__ == "__main__":
    asyncio.run(main())
