import pytest
import pandas as pd
import numpy as np
from synthgen.core import SynthGen

@pytest.fixture
def generator():
    """Create a SynthGen instance with a fixed seed for testing."""
    return SynthGen(seed=42)

def test_init():
    """Test SynthGen initialization."""
    gen = SynthGen(seed=42)
    assert gen.get_seed() == 42
    
    gen = SynthGen()
    assert gen.get_seed() is None

def test_generate_tabular_basic(generator):
    """Test basic tabular data generation."""
    # Test default parameters
    df = generator.generate_tabular()
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 100  # default rows
    assert len(df.columns) == 5  # default columns
    
    # Test custom dimensions
    df = generator.generate_tabular(rows=50, cols=3)
    assert len(df) == 50
    assert len(df.columns) == 3

def test_generate_tabular_column_types(generator):
    """Test generation with different column types."""
    col_types = ['numeric', 'categorical', 'numeric']
    df = generator.generate_tabular(cols=3, col_types=col_types)
    
    # Check numeric columns
    assert df.iloc[:, 0].dtype in (np.float64, np.float32)
    assert df.iloc[:, 2].dtype in (np.float64, np.float32)
    
    # Check categorical column
    assert df.iloc[:, 1].dtype == object

def test_generate_tabular_column_names(generator):
    """Test custom column names."""
    col_names = ['A', 'B', 'C']
    df = generator.generate_tabular(cols=3, col_names=col_names)
    assert list(df.columns) == col_names

def test_generate_tabular_with_noise(generator):
    """Test data generation with noise."""
    # Generate data without noise
    df_no_noise = generator.generate_tabular(cols=1, noise=0.0)
    
    # Generate data with noise
    df_noise = generator.generate_tabular(cols=1, noise=1.0)
    
    # Data with noise should have higher variance
    assert df_noise.iloc[:, 0].std() > df_no_noise.iloc[:, 0].std()

def test_generate_tabular_with_params(generator):
    """Test data generation with custom parameters."""
    numeric_params = [
        {'mean': 10, 'std': 2},
        {'mean': -5, 'std': 1}
    ]
    categorical_params = [
        {'categories': ['X', 'Y', 'Z']}
    ]
    
    df = generator.generate_tabular(
        cols=3,
        col_types=['numeric', 'categorical', 'numeric'],
        numeric_params=numeric_params,
        categorical_params=categorical_params
    )
    
    # Check numeric column parameters
    assert abs(df.iloc[:, 0].mean() - 10) < 1
    assert abs(df.iloc[:, 2].mean() - (-5)) < 1
    
    # Check categorical column parameters
    assert set(df.iloc[:, 1].unique()).issubset({'X', 'Y', 'Z'})

def test_generate_tabular_errors(generator):
    """Test error handling."""
    # Test invalid rows
    with pytest.raises(ValueError):
        generator.generate_tabular(rows=0)
    
    # Test invalid cols
    with pytest.raises(ValueError):
        generator.generate_tabular(cols=-1)
    
    # Test mismatched column types
    with pytest.raises(ValueError):
        generator.generate_tabular(cols=3, col_types=['numeric', 'categorical'])
    
    # Test mismatched column names
    with pytest.raises(ValueError):
        generator.generate_tabular(cols=3, col_names=['A', 'B'])
    
    # Test invalid column type
    with pytest.raises(ValueError):
        generator.generate_tabular(cols=1, col_types=['invalid'])

def test_categorical_values(generator):
    """Test setting custom categorical values."""
    new_values = ['X', 'Y', 'Z']
    generator.set_categorical_values(new_values)
    
    df = generator.generate_tabular(cols=1, col_types=['categorical'])
    assert set(df.iloc[:, 0].unique()).issubset(set(new_values))

def test_seed_reproducibility(generator):
    """Test that results are reproducible with the same seed."""
    # Generate data with first generator
    df1 = generator.generate_tabular()
    
    # Create new generator with same seed
    gen2 = SynthGen(seed=42)
    df2 = gen2.generate_tabular()
    
    # Results should be identical
    pd.testing.assert_frame_equal(df1, df2)

def test_seed_management():
    """Test seed getting and setting."""
    gen = SynthGen(seed=42)
    assert gen.get_seed() == 42
    
    gen.set_seed(100)
    assert gen.get_seed() == 100
    
    gen.set_seed(None)
    assert gen.get_seed() is None