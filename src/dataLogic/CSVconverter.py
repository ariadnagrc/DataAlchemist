import os
import pandas as pd
from nullsFormatter import format_value

def convert_to_csv(file_path):
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
    csv_file_path = os.path.join(file_directory, f'{file_name_without_ext}.csv')

    # Escribir el archivo CSV
    try:
        with open(csv_file_path, 'w', encoding='utf-8') as f:
            # Escribir el encabezado
            f.write(','.join(df.columns) + '\n')

            # Escribir los datos
            for index, row in df.iterrows():
                row_data = [format_value(row[column], column) for column in df.columns]
                f.write(','.join(row_data) + '\n')

        return csv_file_path

    except Exception as e:
        raise Exception(f"Error writing CSV file: {str(e)}")
