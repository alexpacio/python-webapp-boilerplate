#!/bin/sh

# usage: destroy_app_cluster.sh <k8s-namespace>

NAMESPACE=$1
alias ktest="kubectl -n $NAMESPACE"

printf 'Should I destroy and clean up the k8s cluster (y/n)? '
read answer

if [ "$answer" != "${answer#[Yy]}" ] ;then 
    helm uninstall python-fastapi-boilerplate --namespace $NAMESPACE
    ktest delete configmap app-configs
    ktest delete all --all
    kubectl delete namespace $NAMESPACE
fi