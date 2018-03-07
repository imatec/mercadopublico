#!/usr/bin/env bash

if [ -z "$1" ]; then
    TODAY=$(date -u +%Y%m%d)
else
    TODAY=$1
fi

PATH_PUBLICACIONES="data/publicaciones"
PATH_LICITACIONES="data/licitaciones"
mkdir -p ${PATH_PUBLICACIONES}
mkdir -p ${PATH_LICITACIONES}
PUBLICACION="${PATH_PUBLICACIONES}/${TODAY}.json"
python manage.py mp licitaciones --estado=publicada --fecha=${TODAY} --file=${PUBLICACION}
for i in $(python manage.py mp read_list_codes --file=${PUBLICACION});
do
    sleep 2
    echo ""
    CODIGO=$i
    echo $CODIGO
    LICITACION="${PATH_LICITACIONES}/${CODIGO}.json"
    python manage.py mp licitaciones --codigo=${CODIGO} --file=${LICITACION}
    python manage.py mp read_licitacion_fields --licitacion=${LICITACION}
done