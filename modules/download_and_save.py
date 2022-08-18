import datetime
import requests
import os
import locale
import logging
from decouple import config

ROOT_CSV_FOLDER = config('ROOT_CSV_FOLDER')


def is_downloadable_csv(request):
    """
    Does the url contain a downloadable resource
    """
    header = request.headers
    content_type = header.get('content-type')
    # Can be expanded to other types
    if 'csv' in content_type.lower():
        print("Is a CSV")
        return True
    return False


def download_and_save(url_data, type):
    """This will download and store the data to fixed folder convention 
        according type parameter, from the provided URL"""
    # Settings for Argentine date hardcoded, should be system set
    locale.setlocale(locale.LC_TIME, 'es_AR.utf8')
    current_time = datetime.datetime.now()

    # Creation of filename
    # file_name_and_extension=url_data.rpartition('/')[-1]#OLD
    file_path_folder = f"{current_time.year}-{current_time.strftime('%B')}"

    # Changed to be more verbose and resilient to changes,upgrade to future, use regexp
    # if type == 'cine': #OLD
    ####
    if (str(type).find('cine')) != -1:
        file_path_type = ROOT_CSV_FOLDER+"Cinemas/"
        file_name = f"cines-{current_time.strftime('%d-%m-%Y')}.csv"
    elif (str(type).find('biblio')) != -1:
        file_path_type = ROOT_CSV_FOLDER+"Libraries/"
        file_name = f"bibliotecas-{current_time.strftime('%d-%m-%Y')}.csv"
    elif (str(type).find('museos')) != -1:
        file_path_type = ROOT_CSV_FOLDER+"Museums/"
        file_name = f"museos-{current_time.strftime('%d-%m-%Y')}.csv"

    # Creation of filepath
    full_file_path = f"{file_path_type}{file_path_folder}"
    # New Request to fetch csv archive
    try:
        req_csv = requests.get(url_data)
        logging.info('Request processed')
    except OSError:
        print("Fetch csv Failed")
        logging.error('Request failed')
        return -1

    if is_downloadable_csv(req_csv):
        if os.path.exists(full_file_path):
            try:
                open(full_file_path+"/"+file_name, "wb").write(req_csv.content)
                logging.info(
                    f'File on {full_file_path}/{file_name} Saved at {current_time}')
            except OSError:
                logging.error(
                    f'File on {full_file_path}/{file_name} Saved failed to save')
        else:
            try:
                os.mkdir(full_file_path)
            except OSError:
                logging.warning(
                    f'Folder on {full_file_path}, not found. Created at {current_time}')
            try:
                open(full_file_path+"/"+file_name, "wb").write(req_csv.content)
                logging.info(
                    f'File on {full_file_path}/{file_name} Saved at {current_time}')
            except OSError:
                logging.error(
                    f'File on {full_file_path}/{file_name} Saved failed to save')
    else:
        logging.error('CSV not Downlodable')
