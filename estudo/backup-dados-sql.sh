#!/bin/bash

HOME=/home/igor

cd $HOME
if [ ! -d backup ]
then
    mkdir backup
fi

mysqldump -u root $1 > $HOME/backup/$1.sql
if [ $? -eq 0 ]
then
    echo "Backup realizado com sucesso"
else
    echo "Problema ao realizar backup"
fi

