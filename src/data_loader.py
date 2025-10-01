"""
Data loading module for airline OTP and Load Factor analysis.
Handles loading CSV files from BTS data directories.
"""

import pandas as pd
import glob
import os
from pathlib import Path


class DataLoader:
    """Handles loading of OTP and Load Factor data from CSV files."""
    
    def __init__(self, base_path='data/raw'):
        """
        Initialize DataLoader with base data path.
        
        Parameters:
        -----------
        base_path : str
            Base directory containing OTP_Data and Load_Factor_Data subdirectories
        """
        self.base_path = Path(base_path)
        self.otp_path = self.base_path / 'OTP_Data'
        self.lf_path = self.base_path / 'Load_Factor_Data'
        
    def load_load_factor_data(self):
        """
        Load all Load Factor CSV files and combine into single DataFrame.
        
        Returns:
        --------
        pd.DataFrame
            Combined load factor data from all annual files
        """
        lf_files = glob.glob(str(self.lf_path / '*_Segment.csv'))
        
        if not lf_files:
            raise FileNotFoundError(f"No Load Factor files found in {self.lf_path}")
        
        print(f"Found {len(lf_files)} Load Factor files")
        
        dfs = []
        for file in sorted(lf_files):
            print(f"Loading: {os.path.basename(file)}")
            df = pd.read_csv(file)
            dfs.append(df)
        
        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"Total Load Factor records: {len(combined_df):,}")
        
        return combined_df
    
    def load_otp_data(self):
        """
        Load all OTP (On-Time Performance) CSV files and combine into single DataFrame.
        
        Returns:
        --------
        pd.DataFrame
            Combined OTP data from all monthly files
        """
        otp_files = glob.glob(str(self.otp_path / '*.csv'))
        
        if not otp_files:
            raise FileNotFoundError(f"No OTP files found in {self.otp_path}")
        
        print(f"Found {len(otp_files)} OTP files")
        
        dfs = []
        for file in sorted(otp_files):
            print(f"Loading: {os.path.basename(file)}")
            df = pd.read_csv(file)
            dfs.append(df)
        
        combined_df = pd.concat(dfs, ignore_index=True)
        print(f"Total OTP records: {len(combined_df):,}")
        
        return combined_df
    
    def load_all_data(self):
        """
        Load both Load Factor and OTP data.
        
        Returns:
        --------
        tuple
            (load_factor_df, otp_df)
        """
        print("="*60)
        print("Loading Load Factor Data")
        print("="*60)
        lf_df = self.load_load_factor_data()
        
        print("\n" + "="*60)
        print("Loading OTP Data")
        print("="*60)
        otp_df = self.load_otp_data()
        
        return lf_df, otp_df


def quick_load():
    """
    Convenience function to quickly load all data.
    
    Returns:
    --------
    tuple
        (load_factor_df, otp_df)
    """
    loader = DataLoader()
    return loader.load_all_data()