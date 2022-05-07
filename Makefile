## create k3s cluster
cluster:
# enable ephmeral containers for profiling
	k3d cluster create orion --registry-create orion-registry:0.0.0.0:5550 \
		-p 4200:80@loadbalancer -p 9000:9000@loadbalancer -p 9001:9001@loadbalancer \
		--k3s-arg '--kube-apiserver-arg=feature-gates=EphemeralContainers=true@server:*' \
  		--k3s-arg '--kube-scheduler-arg=feature-gates=EphemeralContainers=true@server:*' \
  		--k3s-arg '--kubelet-arg=feature-gates=EphemeralContainers=true@agent:*' \
		--wait
	@echo "Waiting until traefik CRDs are created (~60 secs)..." && export KUBECONFIG=$$(k3d kubeconfig write orion) && \
		while : ; do kubectl get crd ingressroutes.traefik.containo.us > /dev/null && break; sleep 10; done
	@echo -e "\nTo use your cluster set:\n"
	@echo "export KUBECONFIG=$$(k3d kubeconfig write orion)"

## install minio
kubes-minio:
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm install minio bitnami/minio
	kubectl apply -f infra/lb-minio.yaml

## install prefect api and agent into kubes cluster
kubes-prefect: $(venv)
	prefect orion kubernetes-manifest | kubectl apply -f -
	kubectl apply -f infra/ingress-orion.yaml
	PREFECT_API_URL=http://localhost:4200/api prefect work-queue create kubernetes

## minio credentials
minio-creds:
	@set -e && . config/fsspec-env.sh && echo -e "user: $$AWS_ACCESS_KEY_ID\npass: $$AWS_SECRET_ACCESS_KEY"

## show logs
logs:
	kubectl logs -lapp=orion --all-containers

## run basic_flow
basic-flow: $(venv)
	$(venv)/bin/python -m flows.basic_flow

## run ray_flow
ray-flow: $(venv)
	$(venv)/bin/python -m flows.ray_flow

## run k8s_flow as deployment
k8s-flow: export PREFECT_API_URL=http://localhost:4200/api
k8s-flow: $(venv)
	docker compose build app && docker compose push app
	set -e && . config/fsspec-env.sh && cd flows && ../$(venv)/bin/prefect deployment create k8s_flow.py
	$(venv)/bin/prefect deployment inspect test-flow/test-deployment
	$(venv)/bin/prefect deployment run test-flow/test-deployment

## start prefect ui
ui: $(venv)
	PATH="$(venv)/bin:$$PATH" prefect orion start

include *.mk
