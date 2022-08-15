import email
import mailbox
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy_utils import EmailType, PhoneNumber
from .db_orm_settings import Base


class CulturalMap(Base):
    __tablename__ = 'cultural_map'

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

    def __init__(self, cod_localidad, id_provincia, id_departamento, categoria, provincia ,
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
