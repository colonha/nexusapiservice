# Infrastructure as Code

## Kubernetes
For this project we are deploying a local kubernetes cluster using [K3s](https://k3s.io/).

```console
curl -sfL https://get.k3s.io | sh - 
```
```console
sudo k3s kubectl get node
NAME          STATUS   ROLES                  AGE    VERSION
my-desk   Ready    control-plane,master   154m   v1.28.4+k3s2
```

## ArgoCD using autopilot
For the deployment of the application we are using [ArgoCD](https://argoproj.github.io/argo-cd/) and to control/setting Argo we are using [ArgoCD autopilot](https://argocd-autopilot.readthedocs.io/en/stable/).

```console

```console