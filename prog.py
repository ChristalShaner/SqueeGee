import pandas as pd
import numpy as np
from scipy.stats import zscore

def load_data(file_path, chunksize=None):
    """Load the CSV file into a pandas DataFrame."""
    try:
        if chunksize:
            chunks = pd.read_csv(file_path, chunksize=chunksize)
            df = pd.concat(chunks, ignore_index=True)
        else:
            df = pd.read_csv(file_path)
        return df, "Data loaded successfully!"
    except Exception as e:
        return None, f"Error loading data: {e}"

def remove_duplicates(df):
    """Remove duplicate rows from the DataFrame."""
    initial_row_count = len(df)
    df = df.drop_duplicates().reset_index(drop=True)
    return df, f"Removed {initial_row_count - len(df)} duplicate rows."

def handle_missing_values(df, strategy="drop", columns=None):
    """Handle missing values by dropping or imputing them."""
    messages = []
    if strategy == "drop":
        df = df.dropna(subset=columns) if columns else df.dropna()
        messages.append("Dropped rows with missing values.")
    elif strategy in ["mean", "median", "mode"]:
        if not columns:
            columns = df.select_dtypes(include=[np.number]).columns
        fill_values = {
            "mean": {col: df[col].mean() for col in columns},
            "median": {col: df[col].median() for col in columns},
            "mode": {col: df[col].mode()[0] for col in columns}
        }
        df.fillna(value=fill_values[strategy], inplace=True)
        messages.append(f"Missing values imputed using {strategy}.")
    return df, messages

def standardize_text(df):
    """Standardize text columns: remove extra spaces and convert to lowercase."""
    text_columns = df.select_dtypes(include=['object']).columns
    df[text_columns] = df[text_columns].applymap(lambda x: x.strip().lower() if isinstance(x, str) else x)
    return df, "Standardized text columns."

def convert_data_types(df):
    """Convert columns to appropriate data types (numeric, datetime)."""
    messages = []
    for column in df.columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')
        df[column] = pd.to_datetime(df[column], errors='coerce')
    messages.append("Converted data types where applicable.")
    return df, messages

def remove_irrelevant_columns(df, columns_to_drop):
    """Remove irrelevant columns from the DataFrame."""
    df.drop(columns=columns_to_drop, errors='ignore', inplace=True)
    return df, f"Dropped columns: {', '.join(columns_to_drop)}."

def remove_outliers(df, z_threshold=3):
    """Remove outliers using Z-score threshold."""
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    z_scores = np.abs(zscore(df[numeric_columns]))
    mask = (z_scores < z_threshold).all(axis=1)
    df = df.loc[mask]
    return df, f"Outliers removed using Z-Score threshold of {z_threshold}."
