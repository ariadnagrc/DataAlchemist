import os
import pandas as pd
from CSVconverter import convert_to_csv
from ARFFconverter import convert_to_arff

#df_global = None

def convert_file(file_path, format_selected):
    if format_selected == "ARFF":
        return convert_to_arff(file_path)
    elif format_selected == "CSV":
        return convert_to_csv(file_path)
    else:
        raise Exception("Unsupported format selected.")