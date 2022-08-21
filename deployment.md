# Deployment

## Deployment build

[`prefect deployment build`](https://github.com/PrefectHQ/prefect/blob/5bb20fc/src/prefect/cli/deployment.py#L402) will

1. load/execute the flow module
1. write a _$flowname-manifest.json_ file from the flow with name, import path, and parameter schema
1. store the flow:
   1. if `--storage-block` is provided, load the block from the Orion API, and use it to upload the current directory to the storage location
   1. otherwise, use the default storage ie: `LocalFileSystem` with a `basepath` set to the current directory (eg: _/Users/tekumara/code/orion-demo_) and no upload.
1. set infrastructure:
   1. if `--infra-block` is provided, load the block from the Orion API
   1. otherwise use defaults from the type specified by `--infra` (defaulting to the process type if none specified)
1. set description + schedule from existing deployment via Orion API, if any
1. create a `DeploymentYAML` object and write _$flowname-deployment.yaml_ file consisting of:
   1. editable fields, ie: deployment name, description, tags, parameters, schedule, infrastructure
   1. system-generated fields, everything else, eg: flow name, manifest path, storage, parameter schema

eg:

```
$ prefect deployment build flows/param_flow.py:increment -n my-deployment -i kubernetes-job
Found flow 'increment'
Manifest created at '/Users/tekumara/code/orion-demo/increment-manifest.json'.
Deployment YAML created at '/Users/tekumara/code/orion-demo/increment-deployment.yaml'.
```

It's not obvious from these log lines but `build` is saving the flow to storage. In this case storage is a `LocalFileSystem` object with basepath = `/Users/tekumara/code/orion-demo/`

## Deployment apply

[`prefect deployment apply`](https://github.com/PrefectHQ/prefect/blob/5bb20fc/src/prefect/cli/deployment.py#L241) will

1. load _$flowname-deployment.yaml_ file into a `DeploymentYAML` object.
1. create a flow with the deployment's flow name
1. create and save an anonymous infrastructure block from the infrastructure section of the deployment
1. create a deployment from the deployment metadata (name, parameters, description, tags, parameter schema), flow manifest file, and the storage block (previously specified and saved during `deployment build`)

## Loading a flow from a deployment

To [load a flow from a deployment](https://github.com/PrefectHQ/prefect/blob/5bb20fc/src/prefect/deployments.py#L314), the prefect engine will:

1. retrieve the storage block from the Orion API
1. call `storage_block.get_directory(from_path=None, local_path=".")`:
   - LocalFileSystem copies basepath into the current directory
   - RemoteFileSystem downloads basepath into the current directory
1. load the _$flowname-manifest.json_ file
1. load/execute the flow specified in the `import_path` of the manifest

## Caveats

- Developments now require a yaml file and can't be created via a Deployment object.
- Doesn't really support a workflow where the flow code is stored in a docker image because the file systems want to download/copy the contents including the manifest json file.
- For workflows that specify a unique docker image per deployment the _deployment.yaml_ file needs to be edited after `deployment build` or a KubernetesJob block needs to be saved to Orion each time.
- The LocalFileSystem storage basepath is only valid on the same machine that built the deployment.
- `prefect deployment build` with a remote file system will upload the entire contents of the current directory (excluding hidden files/directories) to storage (eg: S3):
  - this may include non-code files and folders (eg: _node_modules/_)
  - the destination will be overwritten and isn't prefixed per deployment
