import pandas as pd
from typing import Union
from pathlib import Path

class DataLoader:
    @staticmethod
    def load_data(source: Union[str, Path]) -> pd.DataFrame:
        """
        Load data from either CSV or Google Sheets.
        
        Args:
            source: Path to CSV file or Google Sheets URL
            
        Returns:
            pd.DataFrame: Loaded data
        """
        if isinstance(source, (str, Path)):
            if str(source).endswith('.csv'):
                return pd.read_csv(source)
            elif 'docs.google.com' in str(source):
                return pd.read_csv(source)
            else:
                raise ValueError("Unsupported file format. Please provide a CSV file or Google Sheets URL.")
        else:
            raise TypeError("Source must be a string path or URL")

    @staticmethod
    def validate_columns(df: pd.DataFrame, required_columns: list) -> bool:
        """
        Validate that the DataFrame contains required columns.
        
        Args:
            df: Input DataFrame
            required_columns: List of required column names
            
        Returns:
            bool: True if all required columns are present
        """
        missing_columns = set(required_columns) - set(df.columns)
        if missing_columns:
            raise ValueError(f"Missing required columns: {missing_columns}")
        return True