import os
import gdown




def create_main_hiden_folder():
    """
    This function get the path to a ghiden folder in the home dir and create it in case it is absent
    output: path to the hiden folder
    """
    hiden_folder_name = f"{os.path.expanduser('~')}/.FusionX"
    os.makedirs(hiden_folder_name, exist_ok=True)
    return hiden_folder_name



def save_model_table_from_cloud( hiden_folder_name, url = 'https://docs.google.com/spreadsheets/d/1lWNAD8Ebj0RpsseNpjmmU6vr9ngbuhnO_A1Le7zHKkQ/export?format=csv'
, output = 'model.csv', id = False):
    """
    this function saves csv file from cloud and put it into hiden file .FusionX in home derectory
    and outputs the file path. Another ID of document can be inputed into the function or another link
    """
    if id:
        url = f"https://docs.google.com/spreadsheets/d/{id}/export?format=csv"

    output_path = f"{hiden_folder_name}/{output}"
    gdown.download(url, output_path, quiet=False)
    return output_path

    

def hello():
    print("hello")