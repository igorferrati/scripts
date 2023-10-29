#!/bin/bash

WORKDIR_RESTORE=/home/igor/restore-aws

aws s3 sync s3://bucket-name/$(date +%F) $WORKDIR_RESTORE

cd $WORKDIR_RESTORE

if [ -f $1.sql ]
then
    mysql -u root table-name < $1.sql
    if [ $? -eq 0 ]
    then
        echo "O restore foi realizado com sucesso"
else
    echo "Arquivo indicado não encontrado"
fi
