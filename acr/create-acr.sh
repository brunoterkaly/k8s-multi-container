# Create a resource group $rg on a specific location $location (for example eastus) for an acr registry called,
export location="westus2"
export rg="rg-kubernetes"
export acr="azureregistrykubernetes"
az group create -l $location -n $rg
# Create an ACR registry $acr
az acr create -n $acr -g $rg -l $location --sku Basic
