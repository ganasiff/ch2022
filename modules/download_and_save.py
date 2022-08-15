import datetime
import requests
import os
from modules import log2file
import locale
import logging

# log2file.log2file()


def is_downloadable_csv(request):
    """
    Does the url contain a downloadable resource
    """
    header = request.headers
    content_type = header.get('content-type')
    if 'csv' in content_type.lower():
        print("Is a CSV")
        return True
    return False


def download_and_save(url_data, type):
    """This will download and store the data to fixed folder convention, from the provided URL"""
    # Settings for Argentine date hardcoded, should be system set
    locale.setlocale(locale.LC_TIME, 'es_AR.utf8')
    current_time = datetime.datetime.now()

    # Creation of filename
    # file_name_and_extension=url_data.rpartition('/')[-1]
    file_path_folder = f"{current_time.year}-{current_time.strftime('%B')}"
    if type == 'cine':
        file_path_type = "./Cinemas/"
        file_name = f"cines-{current_time.strftime('%d-%m-%Y')}.csv"
    elif type == 'biblio':
        file_path_type = "./Libraries/"
        file_name = f"bibliotecas-{current_time.strftime('%d-%m-%Y')}.csv"
    elif type == 'museos':
        file_path_type = "./Museums/"
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
            os.mkdir(full_file_path)
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
