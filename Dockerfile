FROM prefecthq/prefect:2.4.2-python3.9

# s3fs is used by the file-packager deployment to fetch flows
# from the remote file system
# dask dependences are needed by dask_kubes_flow
# boto3 is pinned to avoid a slow search by the pip resolver
RUN pip install --no-cache-dir s3fs==2022.7.1 prefect-dask==0.2.0.post1 dask_kubernetes==2022.7.0 boto3==1.21.21

# explictly specific workdir used in the base image and expected by the deployment
WORKDIR /opt/prefect

# point fsspec at minio inside the cluster
COPY config/fsspec-minio.json config/fsspec.json
ENV FSSPEC_CONFIG_DIR=/opt/prefect/config

# add flows so they can be used by deployments with no storage
COPY flows flows
