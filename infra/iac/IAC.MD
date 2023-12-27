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
For the deployment of the application we are using [ArgoCD](https://argo-cd.readthedocs.io/en/stable/) and to control/setting Argo we are using [ArgoCD autopilot](https://argocd-autopilot.readthedocs.io/en/stable/).

For the installation of ArgoCD autopilot we will require to have the binary for [autopilot](https://argocd-autopilot.readthedocs.io/en/stable/Installation-Guide/). As well we will require to have a Github [token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens) to be able to connect to the repository and store all the configuration.

We will need to export the following variables:
```console
export GIT_TOKEN=ghp_PcZ...IP0
```

```console
export GIT_REPO=https://github.com/owner/name.git/some/relative/path
```
Once we have all this set up we can run the following command to install ArgoCD autopilot:
```console
argocd-autopilot repo bootstrap
```

## NexusApiService
Inside the nexusapi folder we will find the files for Kubernetes deployent including the MongoDB, NexusApiService and the Service for the application. As well a secret is required with the following information:
```console
apiVersion: v1
data:
  password: <Base64 Username>
  username: <Base64 Password>
  mongodb_url: <Base64 Mongodd URI including user and password> #mongodb://user:password@mongo-svc:27017/mydatabase
  kind: Secret
metadata:
  creationTimestamp: null
  name: mongo-creds
```



