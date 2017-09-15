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


@MPCommand.option('-f', '--file', dest='filename', help='nombre de archivo para guardar salida en JSON')
@MPCommand.option('-r', '--rit', dest='rut', help='rut de proveedor')
def buscarproveedor(rut="6-k", filename=None):
    """
    Buscar proveedores por rut
    """
    ticket = current_app.config.get('MP_TICKET', None)
    url = current_app.config.get('MP_ENDPOINT_PROVEEDOR', None)
    payload = {"ticket": ticket}
    if rut:
        payload["rutempresaproveedor"] = rut
    _try_request_and_save(url, payload, filename)


@MPCommand.option('-f', '--file', dest='filename', help='nombre de archivo para guardar salida en JSON')
def buscarcomprador(filename=None):
    """
    Listar organismos compradores
    """
    ticket = current_app.config.get('MP_TICKET', None)
    url = current_app.config.get('MP_ENDPOINT_COMPRADOR', None)
    payload = {"ticket": ticket}
    _try_request_and_save(url, payload, filename)


@MPCommand.option('-d', '--fecha', dest='fecha', help='fecha de la orden de compra')
@MPCommand.option('-p', '--proveedor', dest='proveedor', help='código del proveedor')
@MPCommand.option('-o', '--organismo', dest='organismo', help='código del organismo comprador')
@MPCommand.option('-c', '--codigo', dest='codigo', help='código de la orden de compra')
@MPCommand.option('-s', '--estado', dest='estado', help='estado de la orden de compra (default: todos)')
@MPCommand.option('-f', '--file', dest='filename', help='nombre de archivo para guardar salida en JSON')
def ordenesdecompra(estado="todos", codigo=None, organismo=None, proveedor=None, fecha=None, filename=None):
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
    _try_request_and_save(url, payload, filename)


@MPCommand.option('-d', '--fecha', dest='fecha', help='fecha de la licitación')
@MPCommand.option('-p', '--proveedor', dest='proveedor', help='código del proveedor')
@MPCommand.option('-o', '--organismo', dest='organismo', help='código del organismo comprador')
@MPCommand.option('-c', '--codigo', dest='codigo', help='código de la orden de compra')
@MPCommand.option('-s', '--estado', dest='estado', help='estado de la licitación (default: activas)')
@MPCommand.option('-f', '--file', dest='filename', help='nombre de archivo para guardar salida en JSON')
def licitaciones(estado="activas", codigo=None, organismo=None, proveedor=None, fecha=None, filename=None):
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
    _try_request_and_save(url, payload, filename)


@MPCommand.command
def showticket():
    """
    Mostrar ticket actual
    """
    print("""
ticket={0}

Solicitar tickets en: {1}
""".format(
            current_app.config.get('MP_TICKET', None),
            "http://api.mercadopublico.cl/modules/Participa.aspx"))
