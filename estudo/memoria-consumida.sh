#!/bin/bash

memoria_total=$(free | grep -i mem | awk '{ print $2 }')
memoria_consumida=$(free | grep -i mem | awk '{ print $3 }')

consumo=$(bc <<< "scale=2;$memoria_consumida/$memoria_total * 100" | awk -F. '{ print $1 }')

echo $consumo

#consumo > 50%
if [ $consumo -gt 50 ]
then
mail -s "Consumo acima do limite" adm.exemplo@gmail.com<<<del
Consumo de memória chegou acima de 50%, ultrapassando os limites epserado. Consumo: $(free -h | grep -i mem | awk '{ print $3 }')
del

fi
