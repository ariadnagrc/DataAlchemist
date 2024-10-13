import os
import pandas as pd

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