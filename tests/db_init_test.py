from modules.log2file import log2file_tests
from modules.models import CulturalMap
from modules.db_orm_settings import Base, Session, engine
from sqlalchemy.sql import exists
import logging

log2file_tests()


def engine_session_test():
    # Generate database schema
    Base.metadata.create_all(engine)
    # Create a new session
    session = Session()
    test_entry = CulturalMap(1, 2, 3, 'test_Categ', 'test_provincia', 'test_localidad',
                             'test_nombre', 'test_domicilio', 5500, 2616968879, 'ganasiff@gmail.com', 'www.test.com')

    if (session.query(exists().where(CulturalMap.nombre == 'test_nombre')).scalar()):
        print("Test ya corrido")
        session.close()
        logging.info('Query previously done')
    else:
        session.add(test_entry)
        session.commit()
        session.close()
        logging.info('Query test finished')
