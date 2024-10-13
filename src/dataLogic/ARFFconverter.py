import os
import pandas as pd
from dataFormatter import is_date_format
from nullsFormatter import format_value

def convert_to_arff(file_path):
    # Cargar el archivo según la extensión
    file_extension = os.path.splitext(file_path)[1].lower()
    if file_extension in ['.xlsx', '.xls']:
        df = pd.read_excel(file_path)
    elif file_extension == '.csv':
        df = pd.read_csv(file_path, comment='#', encoding='utf-8')
    else:
        raise Exception("File format not supported.")

    # Obtener el directorio y nombre del archivo original
    file_directory = os.path.dirname(file_path)
    file_name_without_ext = os.path.splitext(os.path.basename(file_path))[0]
    arff_file_path = os.path.join(file_directory, f'{file_name_without_ext}.arff')

    # Escribir el archivo ARFF
    try:
        with open(arff_file_path, 'w', encoding='utf-8') as f:
            f.write('@RELATION data\n\n')
            
            # Escribir los atributos
            for column in df.columns:
                if pd.api.types.is_numeric_dtype(df[column]):
                    f.write(f'@ATTRIBUTE {column} NUMERIC\n')
                elif pd.api.types.is_datetime64_any_dtype(df[column]) or df[column].apply(is_date_format).all():
                    f.write(f'@ATTRIBUTE {column} DATE "yyyy-MM-dd"\n')
                else:
                    unique_values = df[column].dropna().unique()
                    nominal_values = "{" + ",".join([str(val) for val in unique_values]) + "}"
                    f.write(f'@ATTRIBUTE {column} {nominal_values}\n')

            f.write('\n@DATA\n')

            # Escribir los datos
            for index, row in df.iterrows():
                row_data = [format_value(row[column], column) for column in df.columns]
                f.write(','.join(row_data) + '\n')

        return arff_file_path

    except Exception as e:
        raise Exception(f"Error writing ARFF file: {str(e)}")
