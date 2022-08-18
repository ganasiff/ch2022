from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from decouple import config

TABLE_NAME = config('TABLE_NAME')
SCHEMA_NAME = config('SCHEMA_NAME')

usr = config('DB_USR')
passwd = config('DB_PASS')
conn_url = f'postgresql://{usr}:{passwd}@localhost:5432/{SCHEMA_NAME}'
engine = create_engine(conn_url)
Session = sessionmaker(bind=engine)
Base = declarative_base()
