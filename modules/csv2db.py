import pandas as pd
import logging
from pathlib import Path
from glob import glob
import os
from .get_last_csv_in_folder import get_last_filetype_in_folder
from .log2file import log2file
from sqlalchemy import create_engine
from decouple import config

log2file()

usr = config('DB_USR')
passwd = config('DB_PASS')
SCHEMA_NAME = config('SCHEMA_NAME')
ROOT_CSV_FOLDER = config('ROOT_CSV_FOLDER')
conn_url = f'postgresql://{usr}:{passwd}@localhost:5432/{SCHEMA_NAME}'


def csv2df(path=Path('./csv_files/Cinemas/')):

    csv_uri = get_last_filetype_in_folder(path, 'csv')
    df = pd.read_csv(csv_uri)

    # Sanitize Headers
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.lower()
    # rename_dict={'cod_loc':'cod_localidad','idprovincia':'id_provincia',
    # 'iddepartamento':'id_departamento','categoría':'categoria','direccion':'domicilio',
    # 'dirección':'domicilio','cp':'codigo_postal',
    # 'teléfono':'numero_de_telefono','telefono':'numero_de_telefono'}
    # for key in rename_dict.keys():
    #     if key in df.columns:
    #         print(str(f"{{'{key}':'{rename_dict[key]}'}}"))
    #         df.rename(columns=f"{{'{key}':'{rename_dict[key]}'}}",
    # inplace=True)

    if 'cod_loc' in df.columns:
        df.rename(columns={'cod_loc': 'cod_localidad'},
                  inplace=True)
    if 'idprovincia' in df.columns:
        df.rename(columns={'idprovincia': 'id_provincia'},
                  inplace=True)
    if 'iddepartamento' in df.columns:
        df.rename(columns={'iddepartamento': 'id_departamento'},
                  inplace=True)
    if 'categoría' in df.columns:
        df.rename(columns={'categoría': 'categoria'},
                  inplace=True)
    if 'dirección' in df.columns:
        df.rename(columns={'dirección': 'domicilio'},
                  inplace=True)
    if 'direccion' in df.columns:
        df.rename(columns={'direccion': 'domicilio'},
                  inplace=True)
    if 'cp' in df.columns:
        df.rename(columns={'cp': 'codigo_postal'},
                  inplace=True)
    if 'teléfono' in df.columns:
        df.rename(columns={'teléfono': 'numero_de_telefono'},
                  inplace=True)
        # Upgrade concept merge area code with phone number, comment for rollback
        if 'cod_tel' in df.columns:
            df['numero_de_telefono'] = df['cod_tel'].astype(
                str) + "-" + df['numero_de_telefono']
        if 'cod_area' in df.columns:
            df['numero_de_telefono'] = df['cod_area'].astype(
                str) + "-" + df['numero_de_telefono']
    if 'telefono' in df.columns:
        df.rename(columns={'telefono': 'numero_de_telefono'},
                  inplace=True)
        # Upgrade concept merge area code with phone number, comment for rollback
        if 'cod_tel' in df.columns:
            df['numero_de_telefono'] = df['cod_tel'].astype(
                str) + "-" + df['numero_de_telefono']
        if 'cod_area' in df.columns:
            df['numero_de_telefono'] = df['cod_area'].astype(
                str) + "-" + df['numero_de_telefono']

    try:
        # Handled for index error case
        df_out = df[['cod_localidad', 'id_provincia', 'id_departamento', 'categoria', 'provincia',
                     'localidad', 'nombre', 'domicilio', 'codigo_postal', 'numero_de_telefono', 'mail', 'web']]
    except:
        logging.error('Data frame generation failed')
        # create an Empty DataFrame object for failed return purposes
        df_out = pd.DataFrame()

    return df_out


def generate_cultural_map_table(table_name='cultural_map'):

    engine = create_engine(conn_url)
    conn = engine.connect()

    folder_list = next(os.walk(ROOT_CSV_FOLDER))[1]

    df = pd.DataFrame()
    for folder in folder_list:
        df = df.append(csv2df(ROOT_CSV_FOLDER+folder), ignore_index=True)

    try:
        df.to_sql(table_name, con=conn, if_exists='replace')
        logging.info('Table Generated')
        print(df)
    except:
        logging.warning('Table Generation Failed')