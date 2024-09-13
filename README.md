```kubectl create namespace python-api```

```alias k='kubectl -n python-api '```

```k create configmap app-configs --from-env-file=.env```

```helm install python-fastapi-boilerplate ./helm/ --namespace python-api```

```k get all```





```helm uninstall python-fastapi-boilerplate --namespace python-api```