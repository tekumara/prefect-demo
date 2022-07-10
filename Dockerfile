FROM prefecthq/prefect:2.0b8-python3.9

# used by the file-packager deployment to fetch flow
# from the remote file system using fsspec
RUN pip install s3fs

# point fsspec at minio inside the cluster
COPY config/fsspec-minio.json config/fsspec.json
ENV FSSPEC_CONFIG_DIR=/opt/prefect/config

# add flows so they can be referenced by import path
# by the orion-packager-import deployment
COPY flows flows
