#!/bin/bash

#bash filtro-resicao.sh POST, GET, PUT, DELETE

cd scripts-logs

#tratativa para letra minusculas
upper=$(echo $1 | awk '{ print toupper($1) }')

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
    echo "Parametro invalido, digite [GET, POST, PUT ou DELETE]"
    ;;
esac

