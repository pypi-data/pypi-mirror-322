from .example import *

def main():
    hiden_folder_name = create_main_hiden_folder()
    output_path = save_model_table_from_cloud(hiden_folder_name)
    with open (output_path, "r") as t:
        table = t.read()
    A1 = table.split(",")[0]
    print(A1)
    
