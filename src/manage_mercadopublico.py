from flask import current_app
import requests
import json
from dateutil import parser
from flask_script import Manager
import re
from app.utils import JIRATool

MPCommand = Manager(usage="Mercado público")


def _try_request_and_save(url, payload, json_filename=None):
    try:
        resp = requests.get(url, params=payload, verify=False)
        print(resp.url)
        print(resp.status_code)
        # print(resp.content)
        json_data = resp.json()
        if json_filename:
            with open(json_filename, 'w', encoding='utf-8') as f:
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


@MPCommand.command
def update_compradores():
    from app.mercadopublico import Empresa

    ticket = current_app.config.get('MP_TICKET', None)
    url = current_app.config.get('MP_ENDPOINT_COMPRADOR', None)
    payload = {"ticket": ticket}
    resp = requests.get(url, params=payload, verify=False)
    if resp.status_code == 200:
        json_data = resp.json()
        cantidad = json_data.get('Cantidad', None)
        lista_empresas = json_data.get('listaEmpresas', None)
        print("check {0} items".format(cantidad))
        for empresa in lista_empresas:
            empresa = Empresa.create_from_json(empresa)
            print(empresa.CodigoEmpresa)


@MPCommand.command
def iterate_rainbow(file):
    import mmap
    import contextlib
    import csv
    from io import StringIO

    encoding = 'utf-8'
    csv_opts = {'delimiter': ';', 'quoting': csv.QUOTE_MINIMAL, 'quotechar': '"'}
    with open(file, 'r+b') as fd:
        with contextlib.closing(mmap.mmap(fd.fileno(), 0, access=mmap.ACCESS_WRITE)) as mm:
            start = 0
            n_line = 0
            for line in iter(mm.readline, b''):
                n_line += 1
                print("n_line {0}".format(n_line))
                end = mm.tell()
                line = line.decode(encoding).rstrip()
                # print("{0}-{1}: {2}".format(start, end, line))

                row = next(csv.reader([line], **csv_opts))

                encrypt_row(row, encoding)

                new_line_buff = StringIO()
                csv.writer(new_line_buff, **csv_opts).writerow(row)
                new_line = new_line_buff.getvalue().encode(encoding)
                new_end = start + len(new_line)

                # mm.seek(start)
                fd.seek(0)
                size_before = mm.size()
                fd.write(mm[0:start] + new_line + mm[end:])
                fd.flush()
                size_after = mm.size()

                if size_after > size_before:
                    mm.resize(size_after)
                mm.seek(new_end)

                start = new_end


def encrypt_row(row, content_encoding='utf-8'):
    if not row[1]:
        url = "https://www.mercadopublico.cl/BusquedaLicitacion/api/encriptacion/"
        data = [("", "{0}".format(row[0]))]
        resp = requests.post(url, data=data)
        if resp.status_code == 200:
            new_hash = resp.content.decode(content_encoding)[1:-1]
            if new_hash:
                row[1] = new_hash
    else:
        pass


@MPCommand.command
def jira_test():
    host = current_app.config.get('JIRA_HOST', None)
    user = current_app.config.get('JIRA_USER', None)
    _pass = current_app.config.get('JIRA_PASS', None)
    jiratool = JIRATool()
    jiratool.auth(host, user, _pass)
    jql = u'project = SALES AND statusCategory = Done AND status not in (Failed, IceBox)'
    issues = jiratool.query_issues(jql)
    for issue in issues:
        print(issue)


@MPCommand.option('-f', '--file', dest='filename', help='nombre de archivo JSON a leer')
def read_list_codes(filename):
    if filename is None:
        print("no filename")
        exit(1)
    try:
        data = json.load(open(filename))
        if data is not None:
            listado = data.get('Listado', [])
        if listado is not None and len(listado) > 0:
            for licitacion in listado:
                codigo = licitacion.get('CodigoExterno', None)
                if codigo is not None:
                    print(codigo)
        exit(0)
    except Exception as e:
        print(str(e))
        exit(1)


@MPCommand.option('-l', '--licitacion', dest='licitacion', help='nombre de archivo JSON de licitacion')
def read_licitacion_fields(licitacion=None):
    if licitacion:
        host = current_app.config.get('JIRA_HOST', None)
        user = current_app.config.get('JIRA_USER', None)
        _pass = current_app.config.get('JIRA_PASS', None)
        jiratool = JIRATool()
        jiratool.auth(host, user, _pass)

        patterns = ["software", "web", "documental", "computacional", "informatico"]

        try:
            data = json.load(open(licitacion))
            if data is not None:
                listado = data.get('Listado', [])
                if listado is not None and len(listado) > 0:
                    licitacion = listado[0]
                    codigo_externo = licitacion.get('CodigoExterno', None)
                    nombre = licitacion.get('Nombre', None)
                    descripcion = licitacion.get('Descripcion', None)
                    print("Nombre: {0}".format(nombre))
                    print("Descripcion: {0}".format(descripcion))

                    full = "{0} {1}".format(nombre, descripcion)
                    for pattern in patterns:
                        if re.search(pattern, full, re.IGNORECASE):
                            print("MATCH!")
                            new_issue = jiratool.create_ticket(
                                "SALES",
                                "MP - ({0}) {1}".format(codigo_externo, nombre),
                                "Opportunity",
                                descripcion
                            )
                            break

        except Exception as e:
            print(str(e))

