import os
import pandas as pd

df_global = None

# Function to check if it has date format
def is_date_format(value):
    date_formats = [
        '%Y-%m-%d',
        '%Y-%m-%d %H:%M:%S'
    ]
    for fmt in date_formats:
        try:
            pd.to_datetime(value, format=fmt)
            return True
        except ValueError:
            continue
    return False

# Function to convert nulls, spaces and quotes
def format_value(value, column):
    value_str = str(value).strip()  # Convert to string and remove leading and trailing spaces

    # If the value is null or the field is empty after removing spaces, represent as 'empty'
    if pd.isna(value) or value_str == '':
        return '' 

    # If the value is of type date, do not place it in quotes
    if pd.api.types.is_datetime64_any_dtype(df_global[column]):
        return value_str  # Devolver el valor de fecha directamente

    # Check if the value has more than one word that does not already have quotes
    if ' ' in value_str and not (value_str.startswith("'") and value_str.endswith("'")):
        return f"'{value_str}'"  # Place in single quotes if not already in quotes

    return value_str   # If no condition is met, the value is added directly

# Main conversion function
def convert_file(file_path, format_selected):
    global df_global

    # Check file extension
    file_extension = os.path.splitext(file_path)[1].lower()
    is_csv = file_extension == '.csv'  # Verificar si el archivo es CSV

    try:
        # Read file based on extension
        if file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)

            # Remove comments in the first row (header)
            if df.columns[0].startswith('#'):
                df = pd.read_excel(file_path, header=None)
                df = df[~df.iloc[:, 0].astype(str).str.startswith('#')]
                df.columns = df.iloc[0]
                df = df[1:]
            else:
                df = df[~df.apply(lambda row: row.astype(str).str.startswith('#')).any(axis=1)]

            df.reset_index(drop=True, inplace=True)

        elif file_extension == '.csv':
            # Try to read the CSV with different encodings
            try:
                df = pd.read_csv(file_path, comment='#', encoding='utf-8')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, comment='#', encoding='latin1')

        else:
            raise Exception("File format not supported. Formats supported: Excel (.xlsx, .xls) or CSV (.csv).")

        df_global = df

        # Get the directory and name of the original file
        file_directory = os.path.dirname(file_path)
        file_name_without_ext = os.path.splitext(os.path.basename(file_path))[0]

        # If ARFF is selected, convert to ARFF
        if format_selected == "ARFF":
            arff_file_path = os.path.join(file_directory, f'{file_name_without_ext}.arff')
            with open(arff_file_path, 'w', encoding='utf-8') as f:
                f.write('@RELATION data\n\n')

                # Write attributes (columns)
                for column in df.columns:
                    # If it is numeric (even if it has nulls), it will be NUMERIC
                    if pd.api.types.is_numeric_dtype(df[column]) or (df[column].apply(lambda x: isinstance(x, (int, float)) or str(x).strip() == '').all()):
                        f.write(f'@ATTRIBUTE {column} NUMERIC\n')
                    elif pd.api.types.is_datetime64_any_dtype(df[column]) or df[column].apply(is_date_format).all():
                        f.write(f'@ATTRIBUTE {column} DATE "yyyy-MM-dd"\n')  
                    else:
                        # Collect unique values ​​for nominal attributes
                        unique_values = df[column].dropna().unique()
                        if is_csv:
                            # If coming from CSV, don't add quotes
                            unique_values = [str(val) for val in unique_values]
                        else:
                            # If not CSV, add quotes as necessary
                            unique_values = [f"'{val}'" if ' ' in str(val) else str(val) for val in unique_values]

                        nominal_values = "{" + ",".join(unique_values) + "}"
                        f.write(f'@ATTRIBUTE {column} {nominal_values}\n')

                f.write('\n@DATA\n')

                # Write data, handling null values ​​and fields with only white spaces
                for index, row in df.iterrows():
                    row_data = []
                    for column in df.columns:
                        value = row[column]  
                        value_str = format_value(value, column) 

                        # If value is null, replace with '?'
                        if pd.isna(value) or value_str == '':
                            row_data.append('?') 
                        else:
                            # Verificar si el tipo de la columna es fecha o coincide con un formato de fecha
                            if is_date_format(value_str):
                            # Si es una fecha y no tiene comillas, agregar comillas simples
                                if not value_str.startswith("'") and not value_str.endswith("'"):
                                    value_str = f"'{value_str}'"
                            row_data.append(value_str) 

                    f.write(','.join(row_data) + '\n')

            return arff_file_path, df_global 

        # If CSV is selected, convert directly and save to disk
        elif format_selected == "CSV":
            csv_file_path = os.path.join(file_directory, f'{file_name_without_ext}.csv')
            
            # Write the CSV manually to format the values
            with open(csv_file_path, 'w', encoding='utf-8') as f:
                # Write header
                f.write(','.join(df.columns) + '\n')
                
                # Write the data
                for index, row in df.iterrows():
                    row_data = [format_value(row[column], column) for column in df.columns]  
                    f.write(','.join(row_data) + '\n')

            return csv_file_path, df_global

    except Exception as e:
        raise Exception(f"Error al convertir el archivo: {e}")
