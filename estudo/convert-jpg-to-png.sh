#!/bin/bash

#usuário digita a imagem
for imagem in $@
do
    convert $imagem.jpg $imagem.png
done


#verifica todos jpg do diretório - converte para png
converte_imagem(){
cd ~/Downloads/images
if [! -d png ]
then
    mkdir imagem-png
fi

for imagem in *.jpg
do
    local imagem_tratada=$(ls $imagem | awk -F. '{ print $1 }')
    convert $imagem_tratada.jpg imagem-png/$imagem_tratada.png
done
}

converte_imagem 2>erros_conversão.txt
if [ $? -eq 0 ]
then    
    echo "Conversão realizada com sucesso!"
else
    echo "Houve uma falha no processo!"
fi


