# Summary

This project is intended to be used as a boilerplate to deploy backend applications that rely on AWS services.

The project features:

- Helm Charts to install, deploy and configure the entire service stack
- A backend API application written in Python using FastAPI
- Horizontal autoscaling via HPA
- Localstack to mimic the AWS infrastructure locally
- Pulumi IaC to automate the infrastructure management
- K6 to run load tests against the backend API
- E2E tests via pytest

All these features are offered as part of the Helm manifests and all running within the k8s namespace context of this project.

The backend API server is listening on port 8000 and exposes the following resources:


- GET /users: returns the list of users
- POST /users: allows to create an user
- You can find Swagger documentation for the above endpoints at /docs


# Requirements

This project has been tested against microk8s and Ubuntu 24.04 as host OS but it is intended to work with any Kubernetes distribution.

You need to install the following dependencies:

- docker
- microk8s
- HPA CRD, if not included in your K8S distro
- container registry and dns k8s services
- kubectl
- helm

As an optional, in order to develop the backend API server locally, you might want to install also:

- python3 (>3.12)
- poetry
- pip

## Create your environment files

Starting from the .env-example file, create two .env files, called:

- .env-prod - This is meant for the production cluster
- .env-e2etest - This is meant for the E2E tests cluster

## Install the Helm package and all its dependencies

First of all, you need to expose a registry in your k8s cluster. For simplicity we assume that it is reachable via localhost:32000 in your local host.

Using the below script you can build and push the needed Docker images on your registry.

```
sh ./scripts/build_docker_image.sh <image-registry-socket-addr>
```
(socket address is -> "hostname:port")

Then, run your cluster using this script:

```
sh ./scripts/run_app_cluster.sh <k8s-namespace> <env-file-path>
```

The above process should init all the infrastructure needed in k8s. Make sure that everything is up and running with:

```
k get all
```

Now, expose the port needed to access to the API server:

```
kubectl -n <k8s-namespace> port-forward service/backend-svc 8000:8000 &
```

# Scripts

## Tests

### Run e2e tests

This runs e2e tests using Pytest and Poetry, leveraging on a k8s transient job. Also, the script attaches to the k8s log automatically.

```
sh ./scripts/run_e2e_tests_app_cluster.sh <k8s-namespace>
```


## Development lifecycle: pushing changes to the cluster and update it


### Redeploy backend-svc

This builds and deploys the backend API image. Use this script to push your changes in your k8s cluster.

```
sh ./scripts/rebuild_backend_api.sh <k8s-namespace> <image-registry-socket-addr>
```


### Redeploy pulumi

This builds and deploys the pulumi image. Use this script to push your changes in your k8s cluster.

```
sh ./scripts/rebuild_pulumi.sh <k8s-namespace> <image-registry-socket-addr>
```

## Uninstall the Helm package

When you are done, use this command to uninstall your Helm package.

```
sh ./scripts/destroy_app_cluster.sh <k8s-namespace>
```