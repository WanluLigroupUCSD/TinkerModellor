#!/bin/bash

echo tkm will be tested
DIR=test/dataset
outpath=test/.pytest_cache
mkdir -p $outpath

#transform
function transform(){
    echo "transforming...$i"
    cp -r data/para/gromacs/amber14sb_parmbsc1.ff -t $file_pre 
    tkm transform --top $top --crd $gro --xyz $outpath/$i"_transformed.xyz" --clean --ff $1
    rm -r $file_pre/amber14sb_parmbsc1.ff 
    }

for i in {'asp','cys','glu','his','lys'} ;do
    if [ -e $DIR/$i/$i.gro ];then
        file_pre=$DIR/$i
        gro=$file_pre/$i.gro
        top=''
        for file in $(ls $file_pre);do
            ext="${file##*.}"
            if [ "$ext" = "top" ];then
                top+=$file_pre/$file' '
            fi
        done
        transform 2
    fi
done  

pytest -n auto

