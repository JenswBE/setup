# K8S setup with k0s, Cilium and ArgoCD

## Important notes

- k0s is bound to your server's IP. Therefore, ensure your IP is static. See https://github.com/k0sproject/k0s/issues/3450 for more info.

## Base setup on cluster node

```bash
# Ensure system is up-to-date
sudo apt-get update
sudo apt-get dist-upgrade -y
sudo reboot

# Install requirements
sudo apt install -y curl yq

# Install kubectl (optional, "k0s kubectl" also works)
sudo curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"

# Install k0s CLI
curl -sSLf https://get.k0s.sh | sudo sh

# Generate k0s config
k0s config create \
  | yq '.spec.network.provider = "custom"' \
  | yq '.spec.network.kubeProxy.disabled = true' \
  > k0s.yaml

# Install k0s
sudo k0s install controller --single --start --config k0s.yaml

# Generate kubeconfig
mkdir -p ~/.kube
sudo k0s kubeconfig admin > ~/.kube/config

# Install Cilium CLI
CILIUM_CLI_VERSION=$(curl -s https://raw.githubusercontent.com/cilium/cilium-cli/main/stable.txt)
CLI_ARCH=amd64
if [ "$(uname -m)" = "aarch64" ]; then CLI_ARCH=arm64; fi
curl -L --fail --remote-name-all https://github.com/cilium/cilium-cli/releases/download/${CILIUM_CLI_VERSION}/cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}
sha256sum --check cilium-linux-${CLI_ARCH}.tar.gz.sha256sum
sudo tar xzvfC cilium-linux-${CLI_ARCH}.tar.gz /usr/local/bin
rm cilium-linux-${CLI_ARCH}.tar.gz{,.sha256sum}

# Install Cilium on k0s
cilium install

# Wait for the install to finish
cilium status --wait

# Enable Hubble
cilium hubble enable

# Test connectivity
cilium connectivity test
cilium connectivity test --cleanup
```

## Finish setup on local machine

These instructions assume:

- These tools are installed locally: kubectl, helm
- You have a kubeconfig file for above cluster

```bash
# Install ArgoCD
helm repo add argo https://argoproj.github.io/argo-helm
helm install argocd argo/argo-cd -f values/argocd-public.yml --create-namespace -n argo
kubectl -n argo get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d

# Configure public app-of-apps
kubectl config set-context --current --namespace=argo
argocd app create root-public \
    --core \
    --dest-namespace argo \
    --dest-server https://kubernetes.default.svc \
    --repo https://github.com/JenswBE/setup.git \
    --path server/k8s/gitops/root-public \
    --revision main
argocd app sync root-public --core
```

## Based on

- https://docs.k0sproject.io/v0.11.0/install/
- https://docs.cilium.io/en/latest/installation/k0s/
