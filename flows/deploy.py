from prefect.deployments import Deployment
from prefect.infrastructure import KubernetesJob

import flows.dask_kubes_flow
import flows.param_flow
import flows.storage

# upload flow to storage and create deployment yaml file
increment_s3: Deployment = Deployment.build_from_flow(
    name="s3",
    flow=flows.param_flow.increment,
    # output to disk is optional, but we save the yaml representation so we can compare across versions
    output="deployment-increment-s3.yaml",
    description="deployment using s3 storage",
    version="snapshot",
    work_queue_name="kubernetes",
    # every deployment will overwrite the files in this location
    storage=flows.storage.minio_flows(),
    path="increment",
    # use the default KubernetesJob block and override it,
    # rather than creating a new block
    infrastructure=KubernetesJob(),  # type: ignore
    infra_overrides=dict(
        image="orion-registry:5000/flow:latest",
        # use to read the stored flow from minio when the flow executes
        # TODO: move into kubes environment to avoid storing secrets in Prefect
        env={"AWS_ACCESS_KEY_ID": "minioadmin", "AWS_SECRET_ACCESS_KEY": "minioadmin"},
        service_account_name="prefect-flows",
        # deleted completed jobs see https://kubernetes.io/docs/concepts/workloads/controllers/job/#ttl-mechanism-for-finished-jobs
        finished_job_ttl=300,
    ),
    parameters={"i": 1},
)

increment_local: Deployment = Deployment.build_from_flow(
    name="local",
    flow=flows.param_flow.increment,
    output="deployment-increment-local.yaml",
    description="deployment using local storage",
    version="snapshot",
    work_queue_name="kubernetes",
    infrastructure=KubernetesJob(),  # type: ignore
    infra_overrides=dict(
        image="orion-registry:5000/flow:latest",
        env={"AWS_ACCESS_KEY_ID": "minioadmin", "AWS_SECRET_ACCESS_KEY": "minioadmin"},
        service_account_name="prefect-flows",
        finished_job_ttl=300,
    ),
    parameters={"i": 1},
)

greetings_dask: Deployment = Deployment.build_from_flow(
    name="dask",
    flow=flows.dask_kubes_flow.greetings,
    output="deployment-dask-greetings.yaml",
    description="dask kubes",
    version="snapshot",
    work_queue_name="kubernetes",
    infrastructure=KubernetesJob(),  # type: ignore
    infra_overrides=dict(
        image="orion-registry:5000/flow:latest",
        env={"AWS_ACCESS_KEY_ID": "minioadmin", "AWS_SECRET_ACCESS_KEY": "minioadmin"},
        service_account_name="prefect-flows",
        finished_job_ttl=300,
    ),
    parameters={"names": ["arthur", "trillian", "ford", "marvin"]},
)


def apply(deployment: Deployment) -> None:
    did = deployment.apply()
    print(f"Created deployment '{deployment.flow_name}/{deployment.name}' ({did})")


if __name__ == "__main__":
    apply(increment_s3)
    apply(increment_local)
    apply(greetings_dask)
