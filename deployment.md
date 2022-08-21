# Deployment

## Deployment build

[`prefect deployment build`](https://github.com/PrefectHQ/prefect/blob/30ca715/src/prefect/cli/deployment.py#L336) will

1. import the flow module
1. set infrastructure:
   1. if `--infra-block` is provided, load the block from the Orion API
   1. otherwise use defaults from the type specified by `--infra` (defaulting to the process type if none specified)
1. create a `Deployment` object and load existing deployment by name from the Orion API, if any. This populates server-side settings if any (eg: description, version, tags). If no description, use the flow docstring.
1. generate the flow parameter openapi schema
1. update the `Deployment` object with runtime settings
1. write a default _.prefectignore_ file if one doesn't already exist
1. upload the flow to storage:
   1. if `--storage-block` is provided, load the block from the Orion API, and use it to upload the current directory to the storage location
   1. otherwise, use the default storage ie: `LocalFileSystem` with a `basepath` set to the current directory (eg: _/Users/tekumara/code/orion-demo_) and no upload.
1. and write _$flowname-deployment.yaml_ file consisting of:
   1. editable fields, ie: deployment name, description, tags, parameters, schedule, infrastructure
   1. system-generated fields, everything else, eg: flow name, storage, parameter schema

eg:

```
$ prefect deployment build flows/param_flow.py:increment -n my-deployment -i kubernetes-job
Found flow 'increment'
Default '.prefectignore' file written to /Users/tekumara/code/orion-demo/.prefectignore
Deployment YAML created at '/Users/tekumara/code/orion-demo/increment-deployment.yaml'.
```

It's not obvious from these log lines but `build` is saving the flow to storage. In this case storage is a `LocalFileSystem` object with basepath = `/Users/tekumara/code/orion-demo/`

## Deployment apply

[`prefect deployment apply`](https://github.com/PrefectHQ/prefect/blob/30ca715/src/prefect/cli/deployment.py#L241) will

1. load _$flowname-deployment.yaml_ file into a `DeploymentYAML` object.
1. create a flow with the deployment's flow name
1. create and save an anonymous infrastructure block from the infrastructure section of the deployment
1. create a deployment from the deployment metadata (name, parameters, description, tags, parameter schema), and the storage block (previously specified and saved during `deployment build`)

## Loading a flow from a deployment

To [load a flow from a deployment](https://github.com/PrefectHQ/prefect/blob/30ca715/src/prefect/deployments.py#L32), the prefect engine will:

1. retrieve the storage block from the Orion API, or use LocalFileSystem storage if none specified.
1. call `storage_block.get_directory(from_path=None, local_path=".")`:
   - LocalFileSystem copies basepath into the current directory
   - RemoteFileSystem downloads basepath into the current directory
1. load the flow specified in `$path/$entrypoint`

## Building a deployment in python

`Deployment.build_from_flow` is the equivalent of `prefect deployment build` in python.

Differences from the CLI:

1. the `infra` field specifies a new anonymous infra block. To avoid creating a block on apply, use `infra_overrides` instead (recommended).
1. you can supply parameters

For example:

```python
deployment = Deployment.build_from_flow(
   flow=flows.param_flow.increment,
   name="s3-deployment",

   # Deployment class args
   work_queue_name="kubernetes",

   # Create a new anonymous infra block with these params on apply
   infrastructure=KubernetesJob(
      image="orion-registry:5000/flow:latest",
      # use to read the stored flow from minio when the flow executes
      env={"AWS_ACCESS_KEY_ID": "minioadmin", "AWS_SECRET_ACCESS_KEY": "minioadmin"},
   ),
   parameters={"i": 1},
)
```

## Caveats

- Doesn't really support a workflow where the flow code is stored in a docker image because the file systems want to download/copy the contents.
- The LocalFileSystem storage basepath is only valid on the same machine that built the deployment.
