import pytest
import numpy as np
import pandas as pd
from synthgen.tabular import TabularGenerator

@pytest.fixture
def generator():
    """Fixture to create a TabularGenerator instance with a fixed seed."""
    return TabularGenerator(seed=42)

def test_init():
    """Test TabularGenerator initialization."""
    gen = TabularGenerator(seed=42)
    assert isinstance(gen.rng, np.random.RandomState)
    assert len(gen._categorical_values) > 0

def test_generate_numeric_column(generator):
    """Test generation of numeric columns."""
    rows = 1000
    
    # Test basic generation
    col = generator.generate_numeric_column(rows)
    assert len(col) == rows
    assert isinstance(col, np.ndarray)
    
    # Test with specific mean and std
    mean, std = 10.0, 2.0
    col = generator.generate_numeric_column(rows, mean=mean, std=std)
    assert abs(col.mean() - mean) < 0.5  # Allow for some random variation
    assert abs(col.std() - std) < 0.5
    
    # Test with noise
    col = generator.generate_numeric_column(rows, noise=1.0)
    assert len(col) == rows
    assert col.std() > 0  # Ensure there's variation in the data

def test_generate_categorical_column(generator):
    """Test generation of categorical columns."""
    rows = 1000
    
    # Test basic generation
    col = generator.generate_categorical_column(rows)
    assert len(col) == rows
    assert set(col).issubset(set(generator._categorical_values))
    
    # Test with custom categories
    categories = ['X', 'Y', 'Z']
    col = generator.generate_categorical_column(rows, categories=categories)
    assert set(col).issubset(set(categories))
    
    # Test with probabilities
    categories = ['A', 'B']
    probabilities = [0.8, 0.2]
    col = generator.generate_categorical_column(rows, categories=categories, probabilities=probabilities)
    unique, counts = np.unique(col, return_counts=True)
    ratio = counts[0] / rows
    assert abs(ratio - probabilities[0]) < 0.1  # Allow for random variation
    
    # Test invalid probabilities
    with pytest.raises(ValueError):
        generator.generate_categorical_column(rows, categories=['A', 'B'], probabilities=[0.5])

def test_generate_dataset(generator):
    """Test generation of complete datasets."""
    rows = 100
    col_types = ['numeric', 'categorical', 'numeric']
    col_names = ['num1', 'cat1', 'num2']
    
    # Test basic dataset generation
    df = generator.generate_dataset(rows, col_types, col_names)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == rows
    assert list(df.columns) == col_names
    
    # Test with parameters
    numeric_params = [
        {'mean': 10, 'std': 2},
        {'mean': -5, 'std': 1}
    ]
    categorical_params = [
        {'categories': ['X', 'Y', 'Z']}
    ]
    
    df = generator.generate_dataset(
        rows, col_types, col_names,
        numeric_params=numeric_params,
        categorical_params=categorical_params
    )
    
    assert abs(df['num1'].mean() - 10) < 1
    assert abs(df['num2'].mean() - (-5)) < 1
    assert set(df['cat1'].unique()).issubset({'X', 'Y', 'Z'})
    
    # Test error cases
    with pytest.raises(ValueError):
        generator.generate_dataset(rows, [])  # Empty col_types
        
    with pytest.raises(ValueError):
        generator.generate_dataset(rows, col_types, ['col1'])  # Mismatched col_names
        
    with pytest.raises(ValueError):
        generator.generate_dataset(rows, ['invalid_type'])  # Invalid column type

def test_set_categorical_values(generator):
    """Test setting custom categorical values."""
    new_values = ['X', 'Y', 'Z']
    generator.set_categorical_values(new_values)
    assert generator._categorical_values == new_values
    
    # Test error case
    with pytest.raises(ValueError):
        generator.set_categorical_values([])  # Empty list

def test_reproducibility(generator):
    """Test that results are reproducible with the same seed."""
    rows = 100
    col_types = ['numeric', 'categorical']
    
    df1 = generator.generate_dataset(rows, col_types)
    
    # Create new generator with same seed
    generator2 = TabularGenerator(seed=42)
    df2 = generator2.generate_dataset(rows, col_types)
    
    # Check that both datasets are identical
    pd.testing.assert_frame_equal(df1, df2)