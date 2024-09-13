```kubectl create namespace python-api```

```alias k='kubectl -n python-api '```

```k create configmap app-configs --from-env-file=.env```

```helm install python-fastapi-boilerplate ./helm/ --namespace python-api```

```k get all```

```k port-forward service/backend-api 8000:8000```





```helm uninstall python-fastapi-boilerplate --namespace python-api```