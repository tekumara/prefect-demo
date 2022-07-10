FROM prefecthq/prefect:2.0b8-python3.9

# s3fs is used by the file-packager deployment to fetch flows
# from the remote file system
# prefect-dask is needed by dask_kubes_flow
RUN pip install s3fs prefect-dask

# point fsspec at minio inside the cluster
COPY config/fsspec-minio.json config/fsspec.json
ENV FSSPEC_CONFIG_DIR=/opt/prefect/config

# add flows so they can be imported
# by the orion-packager-import deployment
COPY flows flows
