from sqlalchemy import Column, String, Integer
from sqlalchemy_utils import EmailType
from modules.db import Base
from decouple import config

TABLE_NAME = config('TABLE_NAME')


class CulturalMap(Base):
    __tablename__ = TABLE_NAME

    id = Column(Integer, primary_key=True)
    cod_localidad = Column(Integer)
    id_provincia = Column(Integer)
    id_departamento = Column(Integer)
    categoria = Column(String)
    provincia = Column(String)
    localidad = Column(String)
    nombre = Column(String)
    domicilio = Column(String)
    codigo_postal = Column(Integer)
    numero_de_telefono = Column(String)
    mail = Column(EmailType)
    web = Column(String)

    def __init__(self, cod_localidad, id_provincia, id_departamento, categoria, provincia,
                 localidad, nombre, domicilio, codigo_postal, numero_de_telefono, mail, web):
        self.cod_localidad = cod_localidad
        self.id_provincia = id_provincia
        self.id_departamento = id_departamento
        self.categoria = categoria
        self.provincia = provincia
        self.localidad = localidad
        self.nombre = nombre
        self.domicilio = domicilio
        self.codigo_postal,  = codigo_postal,
        self.numero_de_telefono = numero_de_telefono
        self.mail = mail
        self.web = web
