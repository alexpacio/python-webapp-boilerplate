#!/bin/sh

# usage: run_e2e_tests_app_cluster.sh <k8s-namespace> <env-file-path>

NAMESPACE=$1
alias ktest="kubectl -n $NAMESPACE"
set -e
helm template -s templates/backend-api-e2etest-job.yaml python-fastapi-boilerplate ./helm/ --set enableE2eTest=true --namespace $NAMESPACE | ktest apply -f -
sleep 2
ktest logs job.batch/backend-api-e2e-test -f