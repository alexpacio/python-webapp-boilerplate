#!/bin/sh

# usage: run_app_benchmark.sh <k8s-namespace>

NAMESPACE=$1
alias ktest="kubectl -n $NAMESPACE"
set -e
ktest delete job backend-svc-benchmark || true
helm template -s templates/backend-api-benchmark-*.yaml python-fastapi-boilerplate ./helm/ --set enableBenchmark=true --namespace $NAMESPACE | ktest apply -f -
sleep 2
ktest get pods --selector=job-name=backend-svc-benchmark --output=jsonpath='{.items[0].metadata.name}' | xargs -I {} kubectl -n $NAMESPACE wait --for=condition=ready pod/{} --timeout=300s
ktest logs job.batch/backend-svc-benchmark -f
