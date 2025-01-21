import numpy as np
import pandas as pd
from typing import List, Optional, Union

class TabularGenerator:
    """
    A class for generating synthetic tabular data with customizable features.
    """
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize the TabularGenerator.
        
        Args:
            seed (int, optional): Random seed for reproducibility
        """
        self.rng = np.random.RandomState(seed)
        self._categorical_values = ['A', 'B', 'C', 'D', 'E']
    
    def generate_numeric_column(self, rows: int, mean: float = 0.0, 
                              std: float = 1.0, noise: float = 0.0) -> np.ndarray:
        """
        Generate a numeric column with optional Gaussian noise.
        
        Args:
            rows (int): Number of rows to generate
            mean (float): Mean of the distribution
            std (float): Standard deviation of the distribution
            noise (float): Amount of Gaussian noise to add
            
        Returns:
            np.ndarray: Generated numeric column
        """
        base_values = self.rng.normal(mean, std, rows)
        if noise > 0:
            noise_values = self.rng.normal(0, noise, rows)
            return base_values + noise_values
        return base_values
    
    def generate_categorical_column(self, rows: int, 
                                  categories: Optional[List[str]] = None, 
                                  probabilities: Optional[List[float]] = None) -> np.ndarray:
        """
        Generate a categorical column with specified categories and probabilities.
        
        Args:
            rows (int): Number of rows to generate
            categories (List[str], optional): List of possible categories
            probabilities (List[float], optional): Probability weights for each category
            
        Returns:
            np.ndarray: Generated categorical column
        """
        if categories is None:
            categories = self._categorical_values
            
        if probabilities is not None and len(probabilities) != len(categories):
            raise ValueError("Length of probabilities must match length of categories")
            
        return self.rng.choice(categories, size=rows, p=probabilities)
    
    def generate_dataset(self, rows: int, col_types: List[str], 
                        col_names: Optional[List[str]] = None,
                        numeric_params: Optional[List[dict]] = None,
                        categorical_params: Optional[List[dict]] = None) -> pd.DataFrame:
        """
        Generate a complete dataset with specified column types and parameters.
        
        Args:
            rows (int): Number of rows to generate
            col_types (List[str]): List of column types ('numeric' or 'categorical')
            col_names (List[str], optional): Names for the columns
            numeric_params (List[dict], optional): Parameters for numeric columns
            categorical_params (List[dict], optional): Parameters for categorical columns
            
        Returns:
            pd.DataFrame: Generated dataset
        """
        if not col_types:
            raise ValueError("col_types cannot be empty")
            
        if col_names is None:
            col_names = [f"col_{i}" for i in range(len(col_types))]
            
        if len(col_names) != len(col_types):
            raise ValueError("Number of column names must match number of column types")
            
        data = {}
        numeric_idx = 0
        categorical_idx = 0
        
        for i, col_type in enumerate(col_types):
            if col_type.lower() == 'numeric':
                params = {} if numeric_params is None else numeric_params[numeric_idx]
                data[col_names[i]] = self.generate_numeric_column(rows, **params)
                numeric_idx += 1
            elif col_type.lower() == 'categorical':
                params = {} if categorical_params is None else categorical_params[categorical_idx]
                data[col_names[i]] = self.generate_categorical_column(rows, **params)
                categorical_idx += 1
            else:
                raise ValueError(f"Unsupported column type: {col_type}")
                
        return pd.DataFrame(data)
    
    def set_categorical_values(self, values: List[str]) -> None:
        """
        Set the default categorical values used when generating categorical columns.
        
        Args:
            values (List[str]): New list of categorical values
        """
        if not values:
            raise ValueError("Categorical values list cannot be empty")
        self._categorical_values = values.copy()