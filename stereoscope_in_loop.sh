#! /bin/bash
function Usage()
{
cat <<EOF
Usage: $0 [-h] [-i nazwa folderu z plikami]
 -i podaj nazwe folderu w, ktorym znajduja sie podfoldery z danymi zestawami danych
 -h pomoc

 Skrypt:
 1. Potrzebuje nazwe folderu z podfolderami zawierajacymi zestawy danych(uwczesnie przetworzone przez preprocess.py)
EOF

} 


set --  $(getopt hi: $*)
while [ "$1" != -- ]
do
    case $1 in
  -h)   Usage; exit 0;;
  -i)   nazwa_folderu=$2; shift;;
    esac
    shift  
done

if [ "$*" = "" ]  
then
    Usage 
    exit 1
fi


cd $nazwa_folderu
for d in *; do
	cd $d
	CUDA_VISIBLE_DEVICES=2 stereoscope run --sc_fit TRUE_lambda.tsv p_g.tsv --st_cnt C_gs.tsv -ste 50000 -stb 256 -lr 0.01 --gpu -o .
	cd ..
done