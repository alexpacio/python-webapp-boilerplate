#!/bin/sh

# usage: run_app_cluster.sh <k8s-namespace> <env-file-path>

NAMESPACE=$1
alias ktest="kubectl -n $NAMESPACE"
kubectl create namespace $NAMESPACE
set -e
ktest create configmap app-configs --from-env-file=$2
helm install python-fastapi-boilerplate ./helm/ --namespace $NAMESPACE