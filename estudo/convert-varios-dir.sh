#!/bin/bash
varre_dir(){
    cd $1
    for arquivo in *
    do
        if [ -d $arquivo ]
        then
            varre_dir $arquivo
        else
            #Converte jpg png
        fi
    done
}