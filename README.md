# Install the Helm package and all its dependencies

```
./scripts/build_docker_image.sh
kubectl create namespace python-api
alias k='kubectl -n python-api '
k create configmap app-configs --from-env-file=.env
helm install python-fastapi-boilerplate ./helm/ --namespace python-api
k get all
k port-forward service/backend-svc 8000:8000 &
```
# Redeploy backend

```
k rollout restart deploy backend-svc
```

# Uninstall the Helm package

```
helm uninstall python-fastapi-boilerplate --namespace python-api
```