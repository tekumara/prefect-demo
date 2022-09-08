export KUBECONFIG=$(HOME)/.k3d/kubeconfig-orion.yaml

## create cluster and install minio and prefect
kubes: cluster kubes-minio kubes-prefect

## create k3s cluster
cluster:
# enable ephmeral containers for profiling
	k3d cluster create orion --registry-create orion-registry:0.0.0.0:5550 \
		-p 4200:80@loadbalancer -p 9000:9000@loadbalancer -p 9001:9001@loadbalancer \
		--k3s-arg '--kube-apiserver-arg=feature-gates=EphemeralContainers=true@server:*' \
  		--k3s-arg '--kube-scheduler-arg=feature-gates=EphemeralContainers=true@server:*' \
  		--k3s-arg '--kubelet-arg=feature-gates=EphemeralContainers=true@agent:*' \
		--wait
	@echo "Probing until traefik CRDs are created (~60 secs)..." && export KUBECONFIG=$$(k3d kubeconfig write orion) && \
		while : ; do kubectl get crd ingressroutes.traefik.containo.us > /dev/null && break; sleep 10; done
	@echo -e "\nTo use your cluster set:\n"
	@echo "export KUBECONFIG=$$(k3d kubeconfig write orion)"

## install minio
kubes-minio:
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm upgrade --install minio bitnami/minio --set auth.rootUser=minioadmin --set auth.rootPassword=minioadmin
	kubectl apply -f infra/lb-minio.yaml

## install prefect api and agent into kubes cluster
kubes-prefect: export PREFECT_API_URL=http://localhost:4200/api
kubes-prefect: $(venv)
	kubectl apply -f infra/ingress-orion.yaml
	$(venv)/bin/prefect kubernetes manifest orion | kubectl apply -f -
	@echo "Waiting for deployment to settle to single replica (~2 secs)..." && \
		while : ; do \
			replicas=$$(kubectl get deployment orion -o jsonpath="{.status.replicas}") && echo $$replicas && [[ $$replicas == 1 ]] && break; \
			sleep 1; \
		done && echo
	@echo "Probing for the prefect API to be available (~30 secs)..." && \
		while : ; do curl -fsS $$PREFECT_API_URL/admin/version && break; sleep 5; done && echo

## run parameterised flow
param-flow: $(venv)
	$(venv)/bin/python -m flows.param_flow

## run dask flow
dask-flow: $(venv)
	$(venv)/bin/python -m flows.dask_flow

## run ray flow
ray-flow: $(venv)
	$(venv)/bin/python -m flows.ray_flow

## run sub flow
sub-flow: $(venv)
	$(venv)/bin/python -m flows.sub_flow

## deploy basic_flow to kubernetes
kubes-deploy: export PREFECT_API_URL=http://localhost:4200/api
kubes-deploy: $(venv)
	docker compose build app && docker compose push app
# use minio as the s3 remote file system
	set -e && . config/fsspec-env.sh && $(venv)/bin/python -m flows.deploy
	$(venv)/bin/prefect deployment ls
	for deployment in increment/s3; do $(venv)/bin/prefect deployment run $$deployment; done
	$(venv)/bin/prefect flow-run ls
	@echo Visit http://localhost:4200

## start prefect ui
ui: $(venv)
	PATH="$(venv)/bin:$$PATH" prefect orion start

## show kube logs
kubes-logs:
	kubectl logs -lapp=orion --all-containers -f

## show flow run logs
run-logs:
	curl -H "Content-Type: application/json" -X POST --data '{"logs":{"flow_run_id":{"any_":["$(id)"]},"level":{"ge_":0}},"sort":"TIMESTAMP_ASC"}' -s "http://localhost:4200/api/logs/filter" | jq '.[].message | fromjson'

## access orion.db in kubes
kubes-db:
	kubectl exec -i -t svc/orion -c=api -- /bin/bash -c 'hash sqlite3 || (apt-get update && apt-get install sqlite3) && sqlite3 ~/.prefect/orion.db'

## upgrade to latest vesion of orion
upgrade: $(venv)
	latest=$$($(venv)/bin/pip index versions prefect | grep 'LATEST' | sed -E 's/[[:space:]]+LATEST:[[:space:]]+([^[:space:]]+).*/\1/') && \
		rg -l -g '!orion*.yaml' 2.3.2 | xargs sed -i '' "s/2.3.2/$$latest/g"

## inspect block document
api-block-doc: assert-id
	@curl -s "http://localhost:4200/api/block_documents/$(id)" | jq -r 'if .message then .message else {data, block_type:{ name: .block_type.name }} end'

assert-id:
ifndef id
	@echo Missing id variable, eg: make $(MAKECMDGOALS) id=3af1d9d7-d52b-4251-87a0-dfe9c82daa3f
	@exit 42
endif

include *.mk
