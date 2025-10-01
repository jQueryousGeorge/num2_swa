"""
Metrics calculation module for airline performance analysis.
Calculates load factors, OTP metrics, and correlations.
"""

import pandas as pd
import numpy as np
from scipy import stats


class MetricsCalculator:
    """Calculates airline performance metrics."""
    
    @staticmethod
    def calculate_load_factor(df, group_by=None):
        """
        Calculate load factor (passengers/seats ratio).
        
        Parameters:
        -----------
        df : pd.DataFrame
            Load factor data with PASSENGERS and SEATS columns
        group_by : list or None
            Columns to group by before calculating
            
        Returns:
        --------
        pd.DataFrame or pd.Series
            Load factor percentages
        """
        if group_by:
            grouped = df.groupby(group_by).agg({
                'PASSENGERS': 'sum',
                'SEATS': 'sum'
            })
            grouped['LOAD_FACTOR'] = (grouped['PASSENGERS'] / grouped['SEATS'] * 100)
            return grouped
        else:
            load_factor = (df['PASSENGERS'].sum() / df['SEATS'].sum() * 100)
            return load_factor
    
    @staticmethod
    def calculate_otp_metrics(df, group_by=None):
        """
        Calculate OTP (On-Time Performance) metrics.
        
        Parameters:
        -----------
        df : pd.DataFrame
            OTP data
        group_by : list or None
            Columns to group by before calculating
            
        Returns:
        --------
        pd.DataFrame
            OTP metrics including on-time %, cancellation %, delay breakdowns
        """
        if group_by:
            result = df.groupby(group_by).agg({
                'DEP_DEL15': ['sum', 'count'],
                'ARR_DEL15': 'sum',
                'CANCELLED': 'sum',
                'DIVERTED': 'sum',
                'CARRIER_DELAY': 'sum',
                'WEATHER_DELAY': 'sum',
                'NAS_DELAY': 'sum',
                'SECURITY_DELAY': 'sum',
                'LATE_AIRCRAFT_DELAY': 'sum'
            })
            
            # Flatten column names
            result.columns = ['_'.join(col).strip('_') for col in result.columns.values]
            result = result.rename(columns={
                'DEP_DEL15_sum': 'TOTAL_DEP_DELAYED',
                'DEP_DEL15_count': 'TOTAL_FLIGHTS',
                'ARR_DEL15_sum': 'TOTAL_ARR_DELAYED',
                'CANCELLED_sum': 'TOTAL_CANCELLED',
                'DIVERTED_sum': 'TOTAL_DIVERTED',
                'CARRIER_DELAY_sum': 'TOTAL_CARRIER_DELAY',
                'WEATHER_DELAY_sum': 'TOTAL_WEATHER_DELAY',
                'NAS_DELAY_sum': 'TOTAL_NAS_DELAY',
                'SECURITY_DELAY_sum': 'TOTAL_SECURITY_DELAY',
                'LATE_AIRCRAFT_DELAY_sum': 'TOTAL_LATE_AIRCRAFT_DELAY'
            })
            
            # Calculate percentages
            result['DEP_ONTIME_PCT'] = (1 - result['TOTAL_DEP_DELAYED'] / result['TOTAL_FLIGHTS']) * 100
            result['ARR_ONTIME_PCT'] = (1 - result['TOTAL_ARR_DELAYED'] / result['TOTAL_FLIGHTS']) * 100
            result['CANCELLATION_PCT'] = (result['TOTAL_CANCELLED'] / result['TOTAL_FLIGHTS']) * 100
            result['DIVERSION_PCT'] = (result['TOTAL_DIVERTED'] / result['TOTAL_FLIGHTS']) * 100
            
            return result
        else:
            total_flights = len(df)
            metrics = {
                'TOTAL_FLIGHTS': total_flights,
                'TOTAL_DEP_DELAYED': df['DEP_DEL15'].sum(),
                'TOTAL_ARR_DELAYED': df['ARR_DEL15'].sum(),
                'TOTAL_CANCELLED': df['CANCELLED'].sum(),
                'TOTAL_DIVERTED': df['DIVERTED'].sum(),
                'DEP_ONTIME_PCT': (1 - df['DEP_DEL15'].sum() / total_flights) * 100,
                'ARR_ONTIME_PCT': (1 - df['ARR_DEL15'].sum() / total_flights) * 100,
                'CANCELLATION_PCT': (df['CANCELLED'].sum() / total_flights) * 100,
                'DIVERSION_PCT': (df['DIVERTED'].sum() / total_flights) * 100
            }
            return pd.Series(metrics)
    
    @staticmethod
    def merge_lf_otp_by_route_month(lf_df, otp_df):
        """
        Merge load factor and OTP data by route and month.
        
        Parameters:
        -----------
        lf_df : pd.DataFrame
            Load factor data
        otp_df : pd.DataFrame
            OTP data
            
        Returns:
        --------
        pd.DataFrame
            Merged dataset with both load factor and OTP metrics
        """
        # Calculate monthly load factors by route
        lf_monthly = MetricsCalculator.calculate_load_factor(
            lf_df, 
            group_by=['ROUTE', 'YEAR', 'MONTH']
        ).reset_index()
        
        # Calculate monthly OTP by route
        otp_monthly = MetricsCalculator.calculate_otp_metrics(
            otp_df,
            group_by=['ROUTE', 'YEAR', 'MONTH']
        ).reset_index()
        
        # Merge on route, year, and month
        merged = pd.merge(
            lf_monthly,
            otp_monthly,
            on=['ROUTE', 'YEAR', 'MONTH'],
            how='inner'
        )
        
        # Create date column
        merged['DATE'] = pd.to_datetime(
            merged['YEAR'].astype(str) + '-' + merged['MONTH'].astype(str) + '-01'
        )
        
        return merged
    
    @staticmethod
    def calculate_correlation(df, x_col, y_col, method='pearson'):
        """
        Calculate correlation between two variables.
        
        Parameters:
        -----------
        df : pd.DataFrame
            Data containing both variables
        x_col : str
            First variable column name
        y_col : str
            Second variable column name
        method : str
            Correlation method ('pearson', 'spearman', 'kendall')
            
        Returns:
        --------
        dict
            Dictionary with correlation coefficient and p-value
        """
        # Remove any rows with NaN in either column
        clean_df = df[[x_col, y_col]].dropna()
        
        if len(clean_df) < 2:
            return {'correlation': np.nan, 'p_value': np.nan, 'n': 0}
        
        if method == 'pearson':
            corr, p_value = stats.pearsonr(clean_df[x_col], clean_df[y_col])
        elif method == 'spearman':
            corr, p_value = stats.spearmanr(clean_df[x_col], clean_df[y_col])
        elif method == 'kendall':
            corr, p_value = stats.kendalltau(clean_df[x_col], clean_df[y_col])
        else:
            raise ValueError(f"Unknown method: {method}")
        
        return {
            'correlation': corr,
            'p_value': p_value,
            'n': len(clean_df),
            'method': method
        }
    
    @staticmethod
    def route_summary_stats(merged_df, route):
        """
        Calculate summary statistics for a specific route.
        
        Parameters:
        -----------
        merged_df : pd.DataFrame
            Merged load factor and OTP data
        route : str
            Route identifier
            
        Returns:
        --------
        dict
            Summary statistics for the route
        """
        route_data = merged_df[merged_df['ROUTE'] == route]
        
        if len(route_data) == 0:
            return None
        
        stats_dict = {
            'route': route,
            'n_months': len(route_data),
            'total_flights': route_data['TOTAL_FLIGHTS'].sum(),
            'avg_load_factor': route_data['LOAD_FACTOR'].mean(),
            'std_load_factor': route_data['LOAD_FACTOR'].std(),
            'min_load_factor': route_data['LOAD_FACTOR'].min(),
            'max_load_factor': route_data['LOAD_FACTOR'].max(),
            'avg_dep_ontime_pct': route_data['DEP_ONTIME_PCT'].mean(),
            'std_dep_ontime_pct': route_data['DEP_ONTIME_PCT'].std(),
            'avg_arr_ontime_pct': route_data['ARR_ONTIME_PCT'].mean(),
            'std_arr_ontime_pct': route_data['ARR_ONTIME_PCT'].std(),
            'avg_cancellation_pct': route_data['CANCELLATION_PCT'].mean()
        }
        
        # Calculate correlations
        corr_lf_dep = MetricsCalculator.calculate_correlation(
            route_data, 'LOAD_FACTOR', 'DEP_ONTIME_PCT'
        )
        corr_lf_arr = MetricsCalculator.calculate_correlation(
            route_data, 'LOAD_FACTOR', 'ARR_ONTIME_PCT'
        )
        
        stats_dict['corr_lf_dep_ontime'] = corr_lf_dep['correlation']
        stats_dict['corr_lf_dep_pvalue'] = corr_lf_dep['p_value']
        stats_dict['corr_lf_arr_ontime'] = corr_lf_arr['correlation']
        stats_dict['corr_lf_arr_pvalue'] = corr_lf_arr['p_value']
        
        return stats_dict