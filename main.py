from modules.log2file import log2file_init
from decouple import config
from modules.get_data import get_data_from_url
from modules.download_and_save import download_and_save
from modules.csv2db import generate_table

#From .env
M_URL = config('MUSEUMS_URL')
C_URL = config('CINEMAS_URL')
L_URL = config('LIBRARIES_URL')
ROOT_CSV_FOLDER = config('ROOT_CSV_FOLDER')

# Logs to Specific Folder
log2file_init()


def main():

    urls_gob_c = get_data_from_url(C_URL)
    if urls_gob_c != -1:
        for url_data in urls_gob_c:
            if url_data.find('cine') != -1:
                download_and_save(url_data, 'cine')

    urls_gob_m = get_data_from_url(M_URL)
    if urls_gob_m != -1:
        for url_data in urls_gob_m:
            if url_data.find('museos') != -1:
                download_and_save(url_data, 'museos')

    urls_gob_L = get_data_from_url(L_URL)
    if urls_gob_L != -1:
        for url_data in urls_gob_L:
            if url_data.find('biblioteca') != -1:
                download_and_save(url_data, 'biblioteca')

    generate_table('cultural_map')
    
    

    return 0


main()
