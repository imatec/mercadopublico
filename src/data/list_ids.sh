#!/bin/bash
# to generate sequential files of 100K rows each do:  $ for j in $(seq 18 19); do ./list_ids.sh "${j}00000" "${j}99999"; done
URL="https://www.mercadopublico.cl/BusquedaLicitacion/api/encriptacion/"
for i in $(seq $1 $2)
do
	#enc=`curl "${URL}" --compressed --data "=${i}"`
	echo "$i;$enc" >> "${1}_to_${2}.csv"
done
