#!/bin/bash

resp_http=$(curl --write-out %{http_code} --silent --output /dev/null http://localhost:8080)

if [ $resp_http -eq 200 ]
then
    echo "Tudo ok com o servidor"
else
#mail -s "Problema no servidor" adm.exemplo@g ail.com<<del
#Servidor não respondeu 200
#del
    echo "Houve um problema no servidor. Tentando reinicializar"
    docker start apache2-container
fi

