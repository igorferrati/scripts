#!/bin/bash

home=/home/igor/backups-amazon
cd $home

date=$(date +%F)

if [ ! -d $date ]
then
    mkdir $date
fi

tabelas=$(sudo mysql -u root table-name -e "show tables;" | grep -v Tables)
for tabela in $tabelas
do
    mysqldump -u root table-name $tabela > $home/$date/tabela.sql
done

#s3
aws s3 sync $home s3://bucket-name
