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
	$(venv)/bin/prefect kubernetes manifest orion | kubectl apply -f -
	kubectl apply -f infra/ingress-orion.yaml
	kubectl wait pod --for=condition=ready --timeout=120s -lapp=orion
	@echo "Probing for the prefect API to be available (~5 secs)..." && \
		while : ; do curl -fsS http://localhost:4200/ > /dev/null && break; sleep 1; done
	$(venv)/bin/prefect work-queue create kubernetes

## show logs
logs:
	kubectl logs -lapp=orion --all-containers

## run basic_flow
basic-flow: $(venv)
	$(venv)/bin/python -m flows.basic_flow

## run ray_flow
ray-flow: $(venv)
	$(venv)/bin/python -m flows.ray_flow

## deploy and run kubes_flow
kubes-flow: export PREFECT_API_URL=http://localhost:4200/api
kubes-flow: $(venv)
	docker compose build app && docker compose push app
	set -e && . config/fsspec-env.sh && cd flows && ../$(venv)/bin/prefect deployment create kubes_flow.py
	$(venv)/bin/prefect deployment inspect kubes-flow/kubes-deployment
	$(venv)/bin/prefect deployment run kubes-flow/kubes-deployment
	$(venv)/bin/prefect flow-run ls
	@echo Visit http://localhost:4200

## start prefect ui
ui: $(venv)
	PATH="$(venv)/bin:$$PATH" prefect orion start

## upgrade to latest vesion of orion
upgrade: $(venv)
	latest=$$($(venv)/bin/pip index versions prefect --pre | grep 'LATEST' | sed -E 's/[[:space:]]+LATEST:[[:space:]]+([^[:space:]]+).*/\1/') && \
		rg -l -g "!orion*.yaml" 2.0b7 | xargs sed -i '' "s/2.0b7/$$latest/g"

include *.mk
