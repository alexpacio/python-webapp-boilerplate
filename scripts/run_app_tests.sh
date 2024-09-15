#!/bin/sh
NAMESPACE=python-api-test
alias ktest="kubectl -n $NAMESPACE"
kubectl create namespace $NAMESPACE
ktest create configmap app-configs --from-env-file=.env
helm install python-fastapi-boilerplate ./helm/ --namespace $NAMESPACE
helm template -s templates/backend-api-e2etest-job.yaml python-fastapi-boilerplate ./helm/ --namespace $NAMESPACE | ktest apply -f -
ktest logs job.batch/backend-api-e2e-test -f
printf 'Should I clean up the test k8s cluster (y/n)? '
read answer

if [ "$answer" != "${answer#[Yy]}" ] ;then 
    helm uninstall python-fastapi-boilerplate --namespace $NAMESPACE
    kubectl delete namespace $NAMESPACE
fi