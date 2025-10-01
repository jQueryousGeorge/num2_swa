"""
Southwest Airlines OTP and Load Factor Analysis Package

This package provides tools for analyzing the relationship between
Southwest Airlines' On-Time Performance (OTP) and Load Factor metrics.
"""

from .data_loader import DataLoader, quick_load
from .data_cleaner import DataCleaner, clean_all_data
from .metrics import MetricsCalculator

__version__ = '1.0.0'
__author__ = 'Tyler Skidmore'

__all__ = [
    'DataLoader',
    'DataCleaner',
    'MetricsCalculator',
    'quick_load',
    'clean_all_data'
]