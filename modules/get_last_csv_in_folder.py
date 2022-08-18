from pathlib import Path


def get_last_filetype_in_folder(dir_path=Path('./csv_files/Cinemas/'), type='csv'):
    if type == 'csv':
        # Lists CSVs only
        result_list = list(Path(dir_path).rglob("*.[cC][sS][vV]"))
    return max(result_list)
