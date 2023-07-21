#!/bin/bash

export KUBECONFIG=$RD_OPTION_KUBECONFIG

unsel_vault() {

    local try=0

    while [ $try -lt 4 ]; do 

        local pod_status=$(kubectl get pods vault-0 -n vault --no-headers -o custom-columns=":status.phase")

        if [ "$pod_status" = "Running" ]; then
            kubectl exec vault-0 -n vault -- vault operator unseal $RD_OPTION_UNSEAL_VAULT_KEY
            break
        else
            try=$((try + 1))
            sleep 20
        fi
    done

    if [ $try -eq 3]; then
        echo "Erro. verificar o status do POD."
    else
        echo "Vault unseal."
    fi       
}

unseal_vault 
