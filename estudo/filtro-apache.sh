#!/bin/bash

#bash filtro-apache.sh ip 

cd scripts-logs

#passando ip 
regex="\b([0-9]{1,3}\.){3}[0-9]{1,3}\b"

if [[ $1 =~ $regex ]]
then
    cat apache.log | grep $1
    if [ $? -ne 0 ]
    then
        echo "Não foi encontrado o ip indicado"
    fi
else
    echo "Formato invalido"
fi