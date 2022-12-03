include *.mk

export KUBECONFIG=$(HOME)/.k3d/kubeconfig-orion.yaml

## create cluster and install minio and prefect
kubes: cluster kubes-minio kubes-prefect

## create k3s cluster
cluster:
# enable ephmeral containers for profiling
	k3d cluster create orion --registry-create orion-registry:0.0.0.0:5550 \
		-p 4200:80@loadbalancer -p 9000:9000@loadbalancer -p 9001:9001@loadbalancer \
		-p 10001:10001@loadbalancer -p 8265:8265@loadbalancer \
		--k3s-arg '--kube-apiserver-arg=feature-gates=EphemeralContainers=true@server:*' \
  		--k3s-arg '--kube-scheduler-arg=feature-gates=EphemeralContainers=true@server:*' \
  		--k3s-arg '--kubelet-arg=feature-gates=EphemeralContainers=true@agent:*' \
		--wait
	@echo "Probing until traefik CRDs are created (~60 secs)..." && export KUBECONFIG=$$(k3d kubeconfig write orion) && \
		while ! kubectl get crd ingressroutes.traefik.containo.us 2> /dev/null ; do sleep 10 && echo $$((i=i+10)); done
	@echo -e "\nTo use your cluster set:\n"
	@echo "export KUBECONFIG=$$(k3d kubeconfig write orion)"

## install minio
kubes-minio:
	helm repo add bitnami https://charts.bitnami.com/bitnami
# root user and password is stored in the minio secret
	helm upgrade --install minio bitnami/minio --set auth.rootUser=minioadmin --set auth.rootPassword=minioadmin \
		--wait --debug > /dev/null
	kubectl apply -f infra/lb-minio.yaml
	kubectl exec deploy/minio -- mc mb -p local/minio-flows

## install kuberay operator using quickstart manifests
kubes-ray: KUBERAY_VERSION=v0.3.0
kubes-ray:
	kubectl get customresourcedefinition.apiextensions.k8s.io/rayclusters.ray.io || kubectl create -k "github.com/ray-project/kuberay/manifests/cluster-scope-resources?ref=$(KUBERAY_VERSION)"
	kubectl apply -k "github.com/ray-project/kuberay/manifests/base?ref=$(KUBERAY_VERSION)"
	kubectl apply -f infra/ray-cluster.complete.yaml
	kubectl apply -f infra/lb-ray.yaml
	@echo -e "\nProbing for the ray cluster to be available (~3 mins)..." && \
		while ! $(venv)/bin/python -m flows.ping_ray; do sleep 10; done

## upgrade prefect helm chart repo
prefect-helm-repo:
	helm repo add prefect https://prefecthq.github.io/prefect-helm
	helm repo update prefect

## install prefect api and agent into kubes cluster
kubes-prefect: prefect-helm-repo
	kubectl apply -f infra/ingress-orion.yaml
	kubectl apply -f infra/rbac-dask.yaml
	kubectl apply -f infra/sa-flows.yaml
	helm upgrade --install prefect-orion prefect/prefect-orion --version=2022.11.11 \
		--values infra/values-orion.yaml --wait --debug > /dev/null
	helm upgrade --install prefect-agent prefect/prefect-agent --version=2022.11.11 \
		--values infra/values-agent.yaml --wait --debug > /dev/null
	@echo -e "\nProbing for the prefect API to be available (~30 secs)..." && \
		while ! curl -fsS http://localhost:4200/api/admin/version ; do sleep 5; done && echo

# show the prefect job manifest
prefect-job-manifest:
	prefect kubernetes manifest flow-run-job

## run parameterised flow
param-flow: $(venv)
	$(venv)/bin/python -m flows.param_flow

## run dask flow
dask-flow: export PREFECT_API_URL=http://localhost:4200/api
dask-flow: $(venv)
	$(venv)/bin/python -m flows.dask_flow

## run ray flow
ray-flow: export PREFECT_LOCAL_STORAGE_PATH=/tmp/prefect/storage # see https://github.com/PrefectHQ/prefect-ray/issues/26
# PREFECT_API_URL needs to be accessible from the process running the flow and within the ray cluster
# to make this work locally, add 127.0.0.1 prefect-orion to /etc/hosts TODO: find a better fix
ray-flow: export PREFECT_API_URL=http://prefect-orion:4200/api
ray-flow: $(venv)
	$(venv)/bin/python -m flows.ray_flow

## run sub flow
sub-flow: $(venv)
	$(venv)/bin/python -m flows.sub_flow

## build and push docker image
publish:
	docker compose build app && docker compose push app

## deploy flows to run on kubernetes
deploy: export PREFECT_API_URL=http://localhost:4200/api
deploy: $(venv) publish
# use minio as the s3 remote file system
	set -e && . config/fsspec-env.sh && $(venv)/bin/python -m flows.deploy
	$(venv)/bin/prefect deployment ls
	for deployment in increment/s3 increment/local greetings/dask parent/local; do $(venv)/bin/prefect deployment run $$deployment; done
	$(venv)/bin/prefect flow-run ls
	@echo Visit http://localhost:4200

## start prefect ui
ui: $(venv)
	PATH="$(venv)/bin:$$PATH" prefect orion start

## show kube logs
kubes-logs:
	kubectl logs -l "app.kubernetes.io/name in (prefect-orion, prefect-agent)" -f --tail=-1

## show flow run logs
logs: export PREFECT_API_URL=http://localhost:4200/api
logs: assert-id
	curl -H "Content-Type: application/json" -X POST --data '{"logs":{"flow_run_id":{"any_":["$(id)"]},"level":{"ge_":0}},"sort":"TIMESTAMP_ASC"}' -s "http://localhost:4200/api/logs/filter" | jq -r '.[] | [.timestamp,.level,.message] |@tsv'

## show flow runs
flow-runs: export PREFECT_API_URL=http://localhost:4200/api
flow-runs:
	$(venv)/bin/prefect flow-run ls

## access orion.db in kubes
kubes-db:
	kubectl exec -i -t deploy/prefect-orion-api -- /bin/bash -c 'hash sqlite3 || (apt-get update && apt-get install sqlite3) && sqlite3 ~/.prefect/orion.db'

## upgrade to latest version of orion
upgrade:
	latest=$$(PIP_REQUIRE_VIRTUALENV=false pip index versions prefect | grep 'LATEST' | sed -E 's/[[:space:]]+LATEST:[[:space:]]+([^[:space:]]+).*/\1/') && \
		rg -l 2.7.0 | xargs sed -i '' "s/2.7.0/$$latest/g"
	make install

## inspect block document
api-block-doc: assert-id
	@curl -s "http://localhost:4200/api/block_documents/$(id)" | jq -r 'if .message then .message else {data, block_type:{ name: .block_type.name }} end'

assert-id:
ifndef id
	@echo Missing id variable, eg: make $(MAKECMDGOALS) id=3af1d9d7-d52b-4251-87a0-dfe9c82daa3f
	@exit 42
endif
