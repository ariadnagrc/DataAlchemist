import os
import pandas as pd

df_global = None

def convert_file(file_path, format_selected):
    global df_global  # Indicar que vamos a usar la variable global

    try:
        # Leer el archivo de Excel
        df = pd.read_excel(file_path)
        df_global = df  # Almacenar el DataFrame en la variable global

        # Obtener el directorio del archivo original
        file_directory = os.path.dirname(file_path)
        file_name_without_ext = os.path.splitext(os.path.basename(file_path))[0]

        # Si se selecciona ARFF, primero se guarda como CSV y luego se convierte a ARFF
        if format_selected == "ARFF":
            # Guardar primero como CSV (en memoria)
            csv_file_path = os.path.join(file_directory, f'{file_name_without_ext}.csv')
            df.to_csv(csv_file_path, index=False)  # Guardar el CSV

            # Luego convertir a ARFF
            arff_file_path = os.path.join(file_directory, f'{file_name_without_ext}.arff')
            with open(arff_file_path, 'w') as f:
                f.write('@RELATION data\n\n')

                # Escribir atributos (columnas)
                for column in df.columns:
                    if pd.api.types.is_numeric_dtype(df[column]):
                        f.write(f'@ATTRIBUTE {column} NUMERIC\n')
                    else:
                        unique_values = df[column].dropna().unique()
                        unique_values = [f"'{val}'" if ' ' in str(val) else str(val) for val in unique_values]
                        nominal_values = "{" + ",".join(unique_values) + "}"
                        f.write(f'@ATTRIBUTE {column} {nominal_values}\n')

                f.write('\n@DATA\n')

                # Escribir datos
                for index, row in df.iterrows():
                    row_data = []
                    for value in row.values:
                        if isinstance(value, str) and ' ' in value:
                            row_data.append(f"'{value}'")
                        else:
                            row_data.append(str(value))
                    f.write(','.join(row_data) + '\n')

            return arff_file_path, df_global  # Devolver la ruta del ARFF y el DataFrame CSV

        # Si se selecciona CSV, convertir directamente y guardar en disco
        elif format_selected == "CSV":
            csv_file_path = os.path.join(file_directory, f'{file_name_without_ext}.csv')
            df.to_csv(csv_file_path, index=False)  # Guardar el CSV
            return csv_file_path

    except Exception as e:
        raise Exception(f"Error al convertir el archivo: {e}")
