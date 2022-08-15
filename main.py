import logging
from modules import log2file
from decouple import config
from modules.getdata import get_data_from_gob
from modules.download_and_save import download_and_save

M_URL = config('MUSEUMS_URL')
C_URL = config('CINEMAS_URL')
L_URL = config('LIBRARIES_URL')

# Logs to Specific Folder
log2file.log2file()


def main():

    urls_gob_c = get_data_from_gob(C_URL)
    if urls_gob_c != -1:
        for url_data in urls_gob_c:
            if url_data.find('cine') != -1:
                download_and_save(url_data, 'cine')

    urls_gob_m = get_data_from_gob(M_URL)
    if urls_gob_m != -1:
        for url_data in urls_gob_m:
            if url_data.find('museos') != -1:
                download_and_save(url_data, 'museos')

    urls_gob_L = get_data_from_gob(L_URL)
    if urls_gob_L != -1:
        for url_data in urls_gob_L:
            if url_data.find('biblioteca') != -1:
                download_and_save(url_data, 'biblio')

    return 0


main()
