import logging
from flask import Blueprint, jsonify, current_app
from app import db
from sqlalchemy.orm.attributes import InstrumentedAttribute


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True)

    @classmethod
    def from_json(cls, json_dict):
        obj = cls()
        [setattr(obj, atr, json_dict.get(atr, None)) for atr in dir(cls) if isinstance(getattr(cls, atr), InstrumentedAttribute)]
        return obj

    @classmethod
    def create(cls, obj):
        try:
            db.session.add(obj)
            db.session.commit()
            return obj
        except Exception as e:
            logging.exception(e)

    @classmethod
    def create_from_json(cls, json_dict):
        return cls.create(cls.from_json(json_dict))


class Empresa(BaseModel):
    CodigoEmpresa = db.Column(db.String(20), nullable=False)
    NombreEmpresa = db.Column(db.String(255), nullable=False)


class Licitacion(BaseModel):
    CodigoExterno =         db.Column(db.String(100), nullable=False)
    Nombre =                db.Column(db.String(255), nullable=False)
    CodigoEstado =          db.Column(db.Integer, nullable=False)
    FechaCierre =           db.Column(db.DateTime(), nullable=False)
    Descripcion =           db.Column(db.Text, nullable=True)
    Estado =                db.Column(db.String(510), nullable=False)
    Comprador_id =          db.Column(db.Integer, db.ForeignKey('Comprador.id', name='fk_Licitacion_Comprador_id'), index=True)
    Comprador =             db.relationship('Comprador', backref=db.backref('licitaciones', lazy='dynamic'))
    DiasCierreLicitacion =  db.Column(db.Integer, nullable=False)
    Informada =             db.Column(db.Boolean, nullable=False)
    CodigoTipo =            db.Column(db.Integer, nullable=False)
    Tipo =                  db.Column(db.String(20), nullable=False)
    TipoConvocatoria =      db.Column(db.Integer, nullable=False)
    Moneda =                db.Column(db.String(100), nullable=False)
    Etapas =                db.Column(db.Integer, nullable=False)
    EstadoEtapas =          db.Column(db.Integer, nullable=False)
    TomaRazon =             db.Column(db.Integer, nullable=False)
    EstadoPublicidadOfertas = db.Column(db.Integer, nullable=False)
    JustificacionPublicidad = db.Column(db.Text, nullable=True)
    Contrato =              db.Column(db.Integer, nullable=False)
    Obras =                 db.Column(db.Integer, nullable=False)
    CantidadReclamos =      db.Column(db.Integer, nullable=False)
    Fechas_id =             db.Column(db.Integer, db.ForeignKey('Fechas.id', name='fk_Licitacion_Fechas_id'), index=True)
    Fechas =                db.relationship('Fechas', backref=db.backref('licitacion', lazy='dynamic'))
    UnidadTiempoEvaluacion = db.Column(db.Integer, nullable=False)
    DireccionVisita =       db.Column(db.String(500), nullable=False)
    DireccionEntrega =      db.Column(db.String(500), nullable=False)
    Estimacion =            db.Column(db.Text, nullable=True)
    FuenteFinanciamiento =  db.Column(db.Integer, nullable=False)
    VisibilidadMonto =      db.Column(db.Boolean, nullable=False)
    # MontoEstimado
    # UnidadTiempo
    # Modalidad
    # TipoPago
    # NombreResponsablePago
    # EmailResponsablePago






class Comprador(BaseModel):
    CodigoOrganismo = db.Column(db.String(100), nullable=False)
    NombreOrganismo = db.Column(db.String(510), nullable=False)
    RutUnidad = db.Column(db.String(100), nullable=False)
    CodigoUnidad = db.Column(db.String(100), nullable=False)
    NombreUnidad = db.Column(db.String(510), nullable=False)
    DireccionUnidad = db.Column(db.String(510), nullable=False)
    ComunaUnidad = db.Column(db.String(510), nullable=False)
    RegionUnidad = db.Column(db.String(510), nullable=False)
    RutUsuario = db.Column(db.String(100), nullable=False)
    CodigoUsuario = db.Column(db.String(100), nullable=False)
    NombreUsuario = db.Column(db.Text, nullable=True)
    CargoUsuario = db.Column(db.String(100), nullable=False)


class Fechas(BaseModel):
    FechaCreacion = db.Column(db.DateTime(), nullable=False)
    FechaCierre = db.Column(db.DateTime(), nullable=False)
    FechaInicio = db.Column(db.DateTime(), nullable=False)
    FechaFinal = db.Column(db.DateTime(), nullable=False)
    FechaPubRespuestas = db.Column(db.DateTime(), nullable=False)
    FechaActoAperturaTecnica = db.Column(db.DateTime(), nullable=False)
    FechaActoAperturaEconomica = db.Column(db.DateTime(), nullable=False)
    FechaPublicacion = db.Column(db.DateTime(), nullable=False)
    FechaAdjudicacion = db.Column(db.DateTime(), nullable=False)
    FechaEstimadaAdjudicacion = db.Column(db.DateTime(), nullable=False)
    FechaSoporteFisico = db.Column(db.DateTime(), nullable=False)
    FechaTiempoEvaluacion = db.Column(db.DateTime(), nullable=False)
    FechaEstimadaFirma = db.Column(db.DateTime(), nullable=False)
    FechasUsuario = db.Column(db.DateTime(), nullable=False)
    FechaVisitaTerreno = db.Column(db.DateTime(), nullable=False)
    FechaEntregaAntecedentes = db.Column(db.DateTime(), nullable=False)


mp = Blueprint(
    'mp',
    __name__,
    template_folder='templates',
    static_folder='static',
    static_url_path='/static/mp')


@mp.route('/')
def index():
    n_empresas = len(Empresa.query.all())
    print(Empresa)
    return jsonify({'response': 'OK'})