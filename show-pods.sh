#!/usr/bin/env bash

NAMESPACE="--all-namespaces"
if [[ -n $1 ]];then
    NAMESPACE="-n $1"
fi

CUSTOM_COLUMNS='-o=custom-columns=namespace:.metadata.namespace,name:.metadata.name,node:.spec.nodeName'
GET_PODS_ARGS=(get pods $NAMESPACE --no-headers "$CUSTOM_COLUMNS")

# disable default space as the output from
IFS=$'\n'
NODES=($(kubectl get nodes --no-headers -o=custom-columns=name:.metadata.labels."kubernetes\.io\/hostname",fd:.metadata.labels."failure-domain\.beta\.kubernetes\.io/zone"))
if [[ $? -ne 0 ]];then
    echo "Error getting nodes:$NODES"
    exit 1
fi
function getFaultDomainForNode() {
    if [[ -z $1 ]];then
        echo "Error no node passed as parameter"
        exit 1
    fi
    RESULT="No FD found for node $1"
    for node in "${NODES[@]}";do
        IFS=' ' read NODE FD <<< "$node"
        if [[ $1 == ${NODE} ]];then
            RESULT=${FD}
            break
        fi
    done
    echo -n $RESULT
}

echo "namespace,pod,node,fd"
IFS=$'\n'
PODS=($(kubectl "${GET_PODS_ARGS[@]}"))
for pod in "${PODS[@]}";do
    IFS=' ' read NS POD POD_NODE <<< "$pod"
    POD_FD=$(getFaultDomainForNode $POD_NODE)
    echo "$NS,$POD,$POD_NODE,$POD_FD"
done
