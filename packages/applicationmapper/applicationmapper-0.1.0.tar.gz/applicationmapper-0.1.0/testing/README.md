# testing

This direectory contains resources to help you set up a testing environment.

## 1. Prerequisites

- A Kubernetes cluster for testing (e.g. Kind)
- Nyl 0.8.0+

## 2. Getting started

### 2.1. Install ArgoCD and Metacontroller

Simply run

    nyl template --apply base/

### 2.2. Install applicationmapper

    kubectl apply -f ../crds/applicationmapper.yaml

Now, for local development, create a Cloudflare Tunnel and update the `compositecontroller.yaml` to point to your
tunnel.

    kubectl apply -f ../manifests/compositecontroller.yaml

Then also apply the example after making suitable modifications for your tests:

    kubectl apply -f ../manifests/example.yaml
