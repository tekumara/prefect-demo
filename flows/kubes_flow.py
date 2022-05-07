from prefect import flow, get_run_logger
from prefect.blocks.storage import FileStorageBlock
from prefect.deployments import DeploymentSpec
from prefect.flow_runners import KubernetesFlowRunner


@flow
def kubes_flow() -> None:
    # shown in kubectl logs but not prefect ui
    print("Hello from Kubernetes!")
    # show in prefect ui
    logger = get_run_logger()
    logger.info("Hello Prefect UI from Kubernetes!")


DeploymentSpec(
    name="kubes-deployment",
    flow=kubes_flow,
    flow_runner=KubernetesFlowRunner(
        image="orion-registry:5000/flow:latest",
        stream_output=True,
        env={"AWS_ACCESS_KEY_ID": "minioadmin", "AWS_SECRET_ACCESS_KEY": "minioadmin"},
    ),
    flow_storage=FileStorageBlock(base_path="s3://minio-flows/", key_type="hash"),
)
