## create k3s cluster
cluster:
	k3d cluster create orion --registry-create orion-registry:0.0.0.0:5555 -p "4200:80@loadbalancer" --wait
	@echo "Waiting until traefik CRDs are created (~60 secs)..." && export KUBECONFIG=$$(k3d kubeconfig write orion) && \
		while : ; do kubectl get crd ingressroutes.traefik.containo.us > /dev/null && break; sleep 10; done
	@echo -e "\nTo use your cluster set:\n"
	@echo "export KUBECONFIG=$$(k3d kubeconfig write orion)"

## install prefect api and agent into kubes cluster
install-kubes: $(venv)
	prefect orion kubernetes-manifest | kubectl apply -f -
	kubectl apply -f infra/ingress.yaml

## show logs
logs:
	kubectl logs -lapp=orion --all-containers

## run basic_flow
basic-flow: $(venv)
	$(venv)/bin/python -m flows.basic_flow

## start prefect ui
ui: $(venv)
	PATH="$(venv)/bin:$$PATH" prefect orion start

include *.mk
