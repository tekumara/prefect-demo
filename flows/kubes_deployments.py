from prefect.deployments import Deployment
from prefect.filesystems import RemoteFileSystem
from prefect.infrastructure.kubernetes import KubernetesJob
from prefect.packaging.file import FilePackager
from prefect.packaging.orion import OrionPackager
from prefect.packaging.serializers import ImportSerializer

import flows.dask_flow
import flows.param_flow

# use the default packager (OrionPackager) to store the flow's source file
# as an anonymous JSON block in the Orion database. Uses the built docker
# image because it contains flows.another_module which isn't serialised
# and stored by the OrionPackager.
Deployment(
    name="orion-packager",
    flow=flows.param_flow.increment,
    infrastructure=KubernetesJob(
        image="orion-registry:5000/flow:latest",
    ),
    parameters={"i": 1},
)

# use the OrionPackager with the ImportSerializer to store the flow's import path
# as a JSON block in the database, for import at runtime. Requires the flow be
# baked into the the docker image.
Deployment(
    name="orion-packager-import",
    flow=flows.param_flow.increment,
    infrastructure=KubernetesJob(
        image="orion-registry:5000/flow:latest",
    ),
    packager=OrionPackager(serializer=ImportSerializer()),
    parameters={"i": 2},
)

# use the FilePackager to store the flow's source file in S3.
# Requires a docker image with s3fs.
Deployment(
    name="file-packager",
    flow=flows.param_flow.increment,
    infrastructure=KubernetesJob(
        image="orion-registry:5000/flow:latest",
        # use to read the stored flow from minio when the flow executes
        env={"AWS_ACCESS_KEY_ID": "minioadmin", "AWS_SECRET_ACCESS_KEY": "minioadmin"},
    ),
    packager=FilePackager(filesystem=RemoteFileSystem(basepath="s3://minio-flows/")),
    parameters={"i": 3},
)

# Requires a docker image with prefect-dask & dask_kubernetes.
Deployment(
    name="orion-packager",
    flow=flows.dask_flow.greetings,
    infrastructure=KubernetesJob(
        image="orion-registry:5000/flow:latest",
    ),
    parameters={"names": ["kubes", "deployment!"]},
)
