from dataclasses import replace
from optparse import Values
import pandas as pd
import logging
from pathlib import Path
from glob import glob
import os
from .get_last_file_in_folder import get_filetype_list_in_folder
from .log2file import log2file_init
from .db import Session, engine
from decouple import config

# Logs to Specific Folder
log2file_init()

SCHEMA_NAME = config('SCHEMA_NAME')
ROOT_CSV_FOLDER = config('ROOT_CSV_FOLDER')
CINEMAS_FOLDER_NAME=config('CINEMAS_FOLDER_NAME')
MUSEUMS_FOLDER_NAME=config('MUSEUMS_FOLDER_NAME')
LIBRARIES_FOLDER_NAME=config('LIBRARIES_FOLDER_NAME')

def csv2df(path=Path('./csv_files/Cinemas/'),custom_act_for_table='default'):
    """
    Converts csvfile into a panda dataframe, optionally with custom
    normalization and sanitization
    """
    #Get the last file downloaded
    csv_uri = max(get_filetype_list_in_folder(path, 'csv'))
    #Read file
    df = pd.read_csv(csv_uri)
    #df = pd.read_csv(csv_uri,index_col=False)

    # Sanitize Headers
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.lower()

    #Headers Normalization for each table
    if custom_act_for_table == 'cultural_map':
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
    elif custom_act_for_table=='registry_totals':      
        if 'idprovincia' in df.columns:
            df.rename(columns={'idprovincia': 'id_provincia'},
                    inplace=True)
        if 'categoría' in df.columns:
            df.rename(columns={'categoría': 'categoria'},
                    inplace=True)
        df_out=df
    elif custom_act_for_table=='cinemas_capacity':
        #No need for extra rules yet
        df_out=df   
    elif custom_act_for_table=='default':
        #Default course of action
        df_out=df
    return df_out


def generate_table(table_name='cultural_map'):
    """
    Generates and populates the provided table
    """

    folder_list = next(os.walk(ROOT_CSV_FOLDER))[1]
    #Dataframe init
    df = pd.DataFrame()
    
    if table_name=='registry_totals':
        #Gets data from all the sources
        for folder in folder_list:
            df = pd.concat([df, csv2df(ROOT_CSV_FOLDER+folder,custom_act_for_table=table_name)])
        #Get series from dataframe
        sf_cat_count=df['categoria'].value_counts()
        #Convert to Dataframe
        df_cat_count = sf_cat_count.to_frame().reset_index()
        df_cat_count = df_cat_count.rename(columns= {'categoria': 'cant_totals'})
        df_cat_count = df_cat_count.rename(columns= {'index': 'categoria'})
        
        #Get series from dataframe
        sf_source_count=df['fuente'].value_counts()
        #Convert to Dataframe
        df_source_count=sf_source_count.to_frame().reset_index()
        df_source_count = df_source_count.rename(columns= {'fuente': 'cant_totals'})
        df_source_count = df_source_count.rename(columns= {'index': 'fuente'})
        
        #Merge 1st two dataframes
        df_registry_aux=pd.merge(df_source_count, df_cat_count,  how='outer', left_on=['fuente','cant_totals'], right_on = ['categoria','cant_totals'])
        
        #Get series from dataframe
        sf_prov_n_cat=df.value_counts(["provincia", "categoria"])
        #Convert to Dataframe
        df_prov_n_cat=sf_prov_n_cat.to_frame().reset_index()
        df_prov_n_cat = df_prov_n_cat.rename(columns= {0: 'cant_totals'})
        
        #Merge remaining two dataframes
        df_registry_aux=pd.merge(df_registry_aux, df_prov_n_cat,  how='outer', left_on=['categoria','cant_totals'], right_on = ['categoria','cant_totals'])
        df=df_registry_aux

    elif table_name=='cinemas_capacity':
        #Gets data from cinema sources only
        for folder in folder_list:
            if 'Cinemas' in folder:
                df = pd.concat([df, csv2df(ROOT_CSV_FOLDER+folder,custom_act_for_table=table_name)])
        #Get series from dataframe
        sf_cinemas=df.value_counts(["provincia", "pantallas", "butacas", "espacio_incaa"])
        #Convert to Dataframe
        df_cinemas=sf_cinemas.to_frame().reset_index()
        #Generate DataFrame
        df_cinemas = df_cinemas.rename(columns= {0: 'cant_totals'})
        df_cinemas = df_cinemas.groupby('provincia').agg({'espacio_incaa':'count',
                         'pantallas':'sum',
                         'butacas':'sum'}).reset_index()
        df=df_cinemas
    else:
        #Gets data from all the sources
        for folder in folder_list:
            df = pd.concat([df, csv2df(ROOT_CSV_FOLDER+folder,custom_act_for_table=table_name)])
    try:
        with engine.begin() as connection:
            #Read Previous data, set index:
            #Verificar si existe primero
            df_old = pd.read_sql(table_name, con=connection)
            df_old = df_old.set_index('index', drop=True)
            #Save to new dataframe to compare more visually
            df_new=df
            df_new = df.set_index('index', drop=True)
            #Combine with old comes first
            df = pd.concat([df_old, df_new ], copy=False)
            #Drop duplicates, keep last which is from df_new
            df = df [~df .index.duplicated(keep='last')]
            print(df)
            df.to_sql(table_name, con=connection,if_exists='replace')
            logging.info(f'Table {table_name} Generated/Updated Succesfully')
    except Exception as e:
        logging.warning(f'Table {table_name} Generation Failed:{e}')