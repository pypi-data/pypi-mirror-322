from typing import List, Optional, Union, Dict
import pandas as pd
import numpy as np
from .tabular import TabularGenerator

class SynthGen:
    """
    Main interface for synthetic data generation.
    Provides a high-level API for generating various types of synthetic datasets.
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the SynthGen generator.
        
        Args:
            seed (int, optional): Random seed for reproducibility
        """
        self.seed = seed
        self._tabular_generator = TabularGenerator(seed=seed)
        
    def generate_tabular(
        self,
        rows: int = 100,
        cols: int = 5,
        col_types: Optional[List[str]] = None,
        col_names: Optional[List[str]] = None,
        noise: float = 0.0,
        numeric_params: Optional[List[Dict]] = None,
        categorical_params: Optional[List[Dict]] = None
    ) -> pd.DataFrame:
        """
        Generate a synthetic tabular dataset.
        
        Args:
            rows (int): Number of rows in the dataset
            cols (int): Number of columns in the dataset
            col_types (List[str], optional): List of column types ('numeric' or 'categorical')
            col_names (List[str], optional): List of column names
            noise (float): Amount of noise to add to numeric columns
            numeric_params (List[Dict], optional): Parameters for numeric columns
            categorical_params (List[Dict], optional): Parameters for categorical columns
            
        Returns:
            pd.DataFrame: Generated synthetic dataset
            
        Raises:
            ValueError: If input parameters are invalid
        """
        # Validate inputs
        if rows <= 0 or cols <= 0:
            raise ValueError("rows and cols must be positive integers")
            
        # Set default column types if not provided
        if col_types is None:
            col_types = ['numeric'] * cols
        
        # Validate column types
        if len(col_types) != cols:
            raise ValueError(f"Expected {cols} column types, got {len(col_types)}")
            
        for col_type in col_types:
            if col_type.lower() not in ['numeric', 'categorical']:
                raise ValueError(f"Unsupported column type: {col_type}")
        
        # Set default column names if not provided
        if col_names is None:
            col_names = [f"column_{i}" for i in range(cols)]
        
        # Validate column names
        if len(col_names) != cols:
            raise ValueError(f"Expected {cols} column names, got {len(col_names)}")
        
        # Prepare numeric parameters
        if numeric_params is None:
            numeric_params = []
            
        numeric_cols = sum(1 for ct in col_types if ct.lower() == 'numeric')
        while len(numeric_params) < numeric_cols:
            numeric_params.append({'mean': 0.0, 'std': 1.0, 'noise': noise})
            
        # Prepare categorical parameters
        if categorical_params is None:
            categorical_params = []
            
        categorical_cols = sum(1 for ct in col_types if ct.lower() == 'categorical')
        while len(categorical_params) < categorical_cols:
            categorical_params.append({})
        
        # Generate the dataset
        return self._tabular_generator.generate_dataset(
            rows=rows,
            col_types=col_types,
            col_names=col_names,
            numeric_params=numeric_params,
            categorical_params=categorical_params
        )
    
    def set_categorical_values(self, values: List[str]) -> None:
        """
        Set the default categorical values used for categorical columns.
        
        Args:
            values (List[str]): New list of categorical values
        """
        self._tabular_generator.set_categorical_values(values)
    
    def get_seed(self) -> Optional[int]:
        """
        Get the current random seed.
        
        Returns:
            Optional[int]: Current random seed
        """
        return self.seed
    
    def set_seed(self, seed: Optional[int]) -> None:
        """
        Set a new random seed.
        
        Args:
            seed (Optional[int]): New random seed
        """
        self.seed = seed
        self._tabular_generator = TabularGenerator(seed=seed)