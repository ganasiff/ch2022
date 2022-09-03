from pathlib import Path


def get_filetype_list_in_folder(dir_path=Path('./csv_files/Cinemas/'), type='csv'):
    """
    Retrieves the last item added of the provided type in folder
    """
    if type == 'csv':
        # Lists CSVs only
        result_list = list(Path(dir_path).rglob("*.[cC][sS][vV]"))
    return result_list