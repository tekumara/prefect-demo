from prefect.deployments.deployments import Deployment
from prefect.infrastructure import KubernetesJob

import flows.child_flow
import flows.dask_kubes_flow
import flows.param_flow
import flows.parent_flow
import flows.storage

# read aws creds from the minio secret
aws_creds_customizations = [
    {
        "op": "add",
        "path": "/spec/template/spec/containers/0/env/-",
        "value": {
            "name": "AWS_ACCESS_KEY_ID",
            "valueFrom": {
                "secretKeyRef": {
                    "name": "minio",
                    "key": "root-user",
                }
            },
        },
    },
    {
        "op": "add",
        "path": "/spec/template/spec/containers/0/env/-",
        "value": {
            "name": "AWS_SECRET_ACCESS_KEY",
            "valueFrom": {
                "secretKeyRef": {
                    "name": "minio",
                    "key": "root-password",
                }
            },
        },
    },
]


# upload flow to storage and create deployment yaml file
increment_s3: Deployment = Deployment.build_from_flow(
    name="s3",
    flow=flows.param_flow.increment,
    # output to disk is optional, but we save the yaml representation so we can compare across versions
    output="deployment-increment-s3.yaml",
    description="deployment using s3 storage",
    version="snapshot",
    work_pool_name="default-agent-pool",
    # every deployment will overwrite the files in this location
    storage=flows.storage.minio_flows(),
    path="increment",
    # use the default KubernetesJob block and override it,
    # rather than creating a new block
    infrastructure=KubernetesJob(),  # type: ignore
    infra_overrides=dict(
        image="prefect-registry:5000/flow:latest",
        # used to download the stored flow from minio when the job starts
        customizations=aws_creds_customizations,
        service_account_name="prefect-flows",
        # deletes completed jobs see https://kubernetes.io/docs/concepts/workloads/controllers/job/#ttl-mechanism-for-finished-jobs
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
    work_pool_name="default-agent-pool",
    infrastructure=KubernetesJob(),  # type: ignore
    infra_overrides=dict(
        image="prefect-registry:5000/flow:latest",
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
    work_pool_name="default-agent-pool",
    infrastructure=KubernetesJob(),  # type: ignore
    infra_overrides=dict(
        image="prefect-registry:5000/flow:latest",
        service_account_name="prefect-flows",
        finished_job_ttl=300,
    ),
    parameters={"names": ["arthur", "trillian", "ford", "marvin"]},
)


parent_local: Deployment = Deployment.build_from_flow(
    name="local",
    flow=flows.parent_flow.parent,
    output="deployment-parent-local.yaml",
    description="deployment using local storage",
    version="snapshot",
    work_pool_name="default-agent-pool",
    infrastructure=KubernetesJob(),  # type: ignore
    infra_overrides=dict(
        image="prefect-registry:5000/flow:latest",
        service_account_name="prefect-flows",
        finished_job_ttl=300,
    ),
)

child_local: Deployment = Deployment.build_from_flow(
    name="local",
    flow=flows.child_flow.child,
    output="deployment-child-local.yaml",
    description="deployment using local storage",
    version="snapshot",
    work_pool_name="default-agent-pool",
    infrastructure=KubernetesJob(),  # type: ignore
    infra_overrides=dict(
        image="prefect-registry:5000/flow:latest",
        service_account_name="prefect-flows",
        finished_job_ttl=300,
    ),
)


def apply(deployment: Deployment) -> None:
    did = deployment.apply()
    print(f"Created deployment '{deployment.flow_name}/{deployment.name}' ({did})")


if __name__ == "__main__":
    apply(increment_s3)
    apply(increment_local)
    apply(greetings_dask)
    apply(parent_local)
    apply(child_local)
