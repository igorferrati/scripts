#!/bin/bash

#bash filtro-resicao.sh POST, GET, PUT, DELETE

cd scripts-logs

if [ -z $1 ]
then
    read -p "Passe um parametro [GET, PUT, POST ou DELETE]: " requisicao
    upper=$(echo $requisicao | awk '{ print toupper($1) }')
else
    #tratativa para letra minusculas
    upper=$(echo $1 | awk '{ print toupper($1) }')
fi

case $upper in
    GET)
    cat apache.log | grep GET
    ;;

    POST)
    cat apache.log | grep POST
    ;;

    PUT)
    cat apache.log | grep PUT
    ;;

    DELETE)
    cat apache.log | grep DELETE
    ;;

    *)
    echo "Parametro invalido"
    ;;
esac

