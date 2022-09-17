from prefect.deployments import Deployment
from prefect.infrastructure import KubernetesJob

import flows.dask_flow
import flows.param_flow
import flows.storage

# upload flow to storage and create deployment yaml file
deploy_s3: Deployment = Deployment.build_from_flow(
    name="s3",
    flow=flows.param_flow.increment,
    output="deployment-increment-s3.yaml",
    description="deployment using s3 storage",
    version="snapshot",
    work_queue_name="kubernetes",
    # every deployment will overwrite the files in this location
    storage=flows.storage.minio_flows_increment(),
    # use the default KubernetesJob block and override it,
    # rather than creating a new block
    infrastructure=KubernetesJob(),  # type: ignore
    infra_overrides=dict(
        image="orion-registry:5000/flow:latest",
        # use to read the stored flow from minio when the flow executes
        # TODO: move into kubes environment to avoid storing secrets in Prefect
        env={"AWS_ACCESS_KEY_ID": "minioadmin", "AWS_SECRET_ACCESS_KEY": "minioadmin"},
    ),
    parameters={"i": 1},
)  # type: ignore

deploy_local: Deployment = Deployment.build_from_flow(
    name="local",
    flow=flows.param_flow.increment,
    output="deployment-increment-local.yaml",
    description="deployment using local storage",
    version="snapshot",
    work_queue_name="kubernetes",
    # use the default KubernetesJob block and override it,
    # rather than creating a new block
    infrastructure=KubernetesJob(),  # type: ignore
    infra_overrides=dict(
        image="orion-registry:5000/flow:latest",
        # use to read the stored flow from minio when the flow executes
        # TODO: move into kubes environment to avoid storing secrets in Prefect
        env={"AWS_ACCESS_KEY_ID": "minioadmin", "AWS_SECRET_ACCESS_KEY": "minioadmin"},
    ),
    parameters={"i": 1},
)  # type: ignore


def apply(deployment: Deployment) -> None:
    did = deployment.apply()
    print(f"Created deployment '{deployment.flow_name}/{deployment.name}' ({did})")


if __name__ == "__main__":
    apply(deploy_s3)
    apply(deploy_local)


# Requires a docker image with prefect-dask & dask_kubernetes.
# Deployment(
#     name="orion-packager",
#     flow=flows.dask_flow.greetings,
#     infrastructure=KubernetesJob(
#         image="orion-registry:5000/flow:latest",
#     ),
#     parameters={"names": ["kubes", "deployment!"]},
# )
