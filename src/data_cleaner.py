"""
Data cleaning module for airline OTP and Load Factor analysis.
Handles filtering, standardization, and preparation of data.
"""

import pandas as pd
import numpy as np


class DataCleaner:
    """Handles cleaning and preparation of airline data."""
    
    def __init__(self, carrier_code='WN'):
        """
        Initialize DataCleaner.
        
        Parameters:
        -----------
        carrier_code : str
            IATA carrier code to filter (default 'WN' for Southwest)
        """
        self.carrier_code = carrier_code
        
    def clean_load_factor_data(self, df):
        """
        Clean and prepare load factor data.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Raw load factor data
            
        Returns:
        --------
        pd.DataFrame
            Cleaned load factor data
        """
        print(f"Cleaning Load Factor data... Initial records: {len(df):,}")
        
        # Create a copy
        df_clean = df.copy()
        
        # Filter for Southwest Airlines
        df_clean = df_clean[df_clean['CARRIER'] == self.carrier_code].copy()
        print(f"After filtering for {self.carrier_code}: {len(df_clean):,} records")
        
        # Remove rows with missing critical values
        critical_cols = ['DEPARTURES_PERFORMED', 'SEATS', 'PASSENGERS']
        initial_len = len(df_clean)
        df_clean = df_clean.dropna(subset=critical_cols)
        print(f"Removed {initial_len - len(df_clean):,} rows with missing critical values")
        
        # Remove records where performed departures is 0
        df_clean = df_clean[df_clean['DEPARTURES_PERFORMED'] > 0].copy()
        
        # Create route identifier (bidirectional)
        df_clean['ROUTE'] = df_clean.apply(
            lambda x: '-'.join(sorted([x['ORIGIN'], x['DEST']])), 
            axis=1
        )
        
        # Create directional route
        df_clean['ROUTE_DIRECTED'] = df_clean['ORIGIN'] + '-' + df_clean['DEST']
        
        # Create date column
        df_clean['DATE'] = pd.to_datetime(
            df_clean['YEAR'].astype(str) + '-' + df_clean['MONTH'].astype(str) + '-01'
        )
        
        # Ensure numeric types
        numeric_cols = ['DEPARTURES_SCHEDULED', 'DEPARTURES_PERFORMED', 'SEATS', 'PASSENGERS']
        for col in numeric_cols:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
        
        print(f"Final Load Factor records: {len(df_clean):,}")
        
        return df_clean
    
    def clean_otp_data(self, df):
        """
        Clean and prepare OTP data.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Raw OTP data
            
        Returns:
        --------
        pd.DataFrame
            Cleaned OTP data
        """
        print(f"Cleaning OTP data... Initial records: {len(df):,}")
        
        # Create a copy
        df_clean = df.copy()
        
        # Filter for Southwest Airlines
        df_clean = df_clean[df_clean['OP_UNIQUE_CARRIER'] == self.carrier_code].copy()
        print(f"After filtering for {self.carrier_code}: {len(df_clean):,} records")
        
        # Create route identifier (bidirectional)
        df_clean['ROUTE'] = df_clean.apply(
            lambda x: '-'.join(sorted([x['ORIGIN'], x['DEST']])), 
            axis=1
        )
        
        # Create directional route
        df_clean['ROUTE_DIRECTED'] = df_clean['ORIGIN'] + '-' + df_clean['DEST']
        
        # Create date column
        df_clean['DATE'] = pd.to_datetime(
            df_clean['YEAR'].astype(str) + '-' + df_clean['MONTH'].astype(str) + '-01'
        )
        
        # Fill NaN delay values with 0 (assuming no delay if not reported)
        delay_cols = ['DEP_DEL15', 'ARR_DEL15', 'CANCELLED', 'DIVERTED',
                      'CARRIER_DELAY', 'WEATHER_DELAY', 'NAS_DELAY', 
                      'SECURITY_DELAY', 'LATE_AIRCRAFT_DELAY']
        
        for col in delay_cols:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].fillna(0)
        
        # Ensure numeric types
        for col in delay_cols:
            if col in df_clean.columns:
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0)
        
        print(f"Final OTP records: {len(df_clean):,}")
        
        return df_clean
    
    def filter_date_range(self, df, start_date='2020-01-01', end_date='2025-06-30'):
        """
        Filter dataframe to specific date range.
        
        Parameters:
        -----------
        df : pd.DataFrame
            DataFrame with DATE column
        start_date : str
            Start date (YYYY-MM-DD)
        end_date : str
            End date (YYYY-MM-DD)
            
        Returns:
        --------
        pd.DataFrame
            Filtered dataframe
        """
        mask = (df['DATE'] >= start_date) & (df['DATE'] <= end_date)
        filtered_df = df[mask].copy()
        print(f"Filtered to {start_date} to {end_date}: {len(filtered_df):,} records")
        return filtered_df
    
    def get_top_routes(self, df, n=5, metric='PASSENGERS'):
        """
        Identify top N routes by specified metric.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Load factor data
        n : int
            Number of top routes to return
        metric : str
            Metric to use for ranking ('PASSENGERS', 'DEPARTURES_PERFORMED', 'SEATS')
            
        Returns:
        --------
        list
            List of top N route identifiers
        """
        route_totals = df.groupby('ROUTE')[metric].sum().sort_values(ascending=False)
        top_routes = route_totals.head(n).index.tolist()
        
        print(f"\nTop {n} routes by {metric}:")
        for i, route in enumerate(top_routes, 1):
            print(f"{i}. {route}: {route_totals[route]:,.0f} {metric.lower()}")
        
        return top_routes


def clean_all_data(lf_df, otp_df, carrier_code='WN'):
    """
    Convenience function to clean both datasets.
    
    Parameters:
    -----------
    lf_df : pd.DataFrame
        Raw load factor data
    otp_df : pd.DataFrame
        Raw OTP data
    carrier_code : str
        Carrier code to filter
        
    Returns:
    --------
    tuple
        (cleaned_lf_df, cleaned_otp_df)
    """
    cleaner = DataCleaner(carrier_code=carrier_code)
    
    print("="*60)
    print("CLEANING LOAD FACTOR DATA")
    print("="*60)
    lf_clean = cleaner.clean_load_factor_data(lf_df)
    
    print("\n" + "="*60)
    print("CLEANING OTP DATA")
    print("="*60)
    otp_clean = cleaner.clean_otp_data(otp_df)
    
    return lf_clean, otp_clean