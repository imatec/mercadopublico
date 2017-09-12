from flask import current_app
import requests
import json
from dateutil import parser
from flask_script import Manager
MPCommand = Manager(usage="Mercado público")


def _try_request_and_save(url, payload, json_filename=None):
    try:
        resp = requests.get(url, params=payload, verify=False)
        print(resp.url)
        print(resp.status_code)
        print(resp.content)
        json_data = resp.json()
        if json_filename:
            with open(json_filename, 'w') as f:
                json.dump(json_data, f, ensure_ascii=False, sort_keys=True, indent=4)
        else:
            print(json_filename)
    except Exception as ex:
        print(ex)


@MPCommand.command
def buscarproveedor(rut="6-k", json_filename=None):
    ticket = current_app.config.get('MP_TICKET', None)
    url = current_app.config.get('MP_ENDPOINT_PROVEEDOR', None)
    payload = {"ticket": ticket}
    if rut:
        payload["rutempresaproveedor"] = rut
    _try_request_and_save(url, payload, json_filename)


@MPCommand.command
def buscarcomprador(json_filename=None):
    ticket = current_app.config.get('MP_TICKET', None)
    url = current_app.config.get('MP_ENDPOINT_COMPRADOR', None)
    payload = {"ticket": ticket}
    _try_request_and_save(url, payload, json_filename)


@MPCommand.command
def ordenesdecompra(estado="todos", codigo=None, organismo=None, proveedor=None, fecha=None, json_filename=None):
    """
    Ordenes de compra
    """
    ticket = current_app.config.get('MP_TICKET', None)
    url = current_app.config.get('MP_ENDPOINT_ORDENESDECOMPRA', None)
    payload = {"ticket": ticket}
    if estado:
        payload["estado"] = estado
    if codigo:
        payload["codigo"] = codigo
    if organismo:
        payload["CodigoOrganismo"] = organismo
    if proveedor:
        payload["CodigoProveedor"] = proveedor
    if fecha:
        fecha = parser.parse(fecha)
        payload["fecha"] = fecha.strftime("%d%m%Y")
    _try_request_and_save(url, payload, json_filename)

@MPCommand.command
def licitaciones(estado="activas", codigo=None, organismo=None, proveedor=None, fecha=None, json_filename=None):
    """
    Licitaciones
    """
    ticket = current_app.config.get('MP_TICKET', None)
    url = current_app.config.get('MP_ENDPOINT_LICITACIONES', None)
    payload = {"ticket": ticket}
    if estado:
        payload["estado"] = estado
    if codigo:
        payload["codigo"] = codigo
    if organismo:
        payload["CodigoOrganismo"] = organismo
    if proveedor:
        payload["CodigoProveedor"] = proveedor
    if fecha:
        fecha = parser.parse(fecha)
        payload["fecha"] = fecha.strftime("%d%m%Y")
    _try_request_and_save(url, payload, json_filename)


@MPCommand.command
def ticket():
    print(current_app.config.get('MP_TICKET', None))