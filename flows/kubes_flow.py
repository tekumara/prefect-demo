from prefect import flow, get_run_logger
from prefect.deployments import Deployment
from prefect.flow_runners import KubernetesFlowRunner


@flow
def kubes_flow() -> None:
    # shown in kubectl logs but not prefect ui
    print("Hello from Kubernetes!")
    # show in prefect ui
    logger = get_run_logger()
    logger.info("Hello Prefect UI from Kubernetes!")


# the default packager is an OrionPackager which creates a OrionPackageManifest pointing to the flow's source file
# stored as an anonymous JSON block in the Orion database. The block is encrypted.
Deployment(
    name="kubes-deployment",
    flow=kubes_flow,
    flow_runner=KubernetesFlowRunner(
        image="orion-registry:5000/flow:latest",
        stream_output=True,
    ),
)
