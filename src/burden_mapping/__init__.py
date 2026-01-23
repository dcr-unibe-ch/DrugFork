"""
Disease Burden Mapping Utilities

This module provides tools for preprocessing and loading disease burden data.
"""

from .burden_utils import (
    load_burden_data,
    extract_canonical_classes,
    CANONICAL_CLASSES,
    get_burden_data_path
)

__all__ = [
    'load_burden_data',
    'extract_canonical_classes',
    'CANONICAL_CLASSES',
    'get_burden_data_path'
]
