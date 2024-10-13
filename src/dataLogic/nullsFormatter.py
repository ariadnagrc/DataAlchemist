import pandas as pd

# Function to convert nulls, spaces, and quotes
def format_value(value, column_data):
    value_str = str(value).strip()  # Convert to string and remove leading and trailing spaces

    # If the value is null or the field is empty after removing spaces, represent as 'empty'
    if pd.isna(value) or value_str == '':
        return ''

    # If the value is of type date, do not place it in quotes
    if pd.api.types.is_datetime64_any_dtype(column_data):
        return value_str  # Return the date value directly

    # Check if the value has more than one word that does not already have quotes
    if ' ' in value_str and not (value_str.startswith("'") and value_str.endswith("'")):
        return f"'{value_str}'"  # Place in single quotes if not already in quotes

    return value_str  # If no condition is met, return the value directly
