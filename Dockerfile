FROM prefecthq/prefect:2.4.0-python3.9

# s3fs is used by the file-packager deployment to fetch flows
# from the remote file system
# prefect-dask is needed by dask_kubes_flow
# boto3 is pinned to avoid a slow search by the pip resolver
RUN pip install s3fs prefect-dask boto3==1.21.21

# point fsspec at minio inside the cluster
COPY config/fsspec-minio.json config/fsspec.json
ENV FSSPEC_CONFIG_DIR=/opt/prefect/config

# add flows so they can be imported
# by the orion-packager-import deployment
COPY flows flows
