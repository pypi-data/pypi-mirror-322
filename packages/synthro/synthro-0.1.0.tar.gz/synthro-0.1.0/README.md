# SynthGen

**SynthGen** is a Python library designed to generate synthetic datasets for testing, prototyping, and research purposes. It supports generating tabular datasets with customizable features and is designed for extensibility.

## Features

- Generate synthetic tabular datasets with numeric and categorical columns
- Add Gaussian noise to numeric data for variability
- Fully customizable columns and data types
- Set random seeds for reproducibility
- Easy-to-use API

## Installation

You can install the library using pip:

```bash
pip install synthgen
```

Alternatively, clone the repository and install locally:

```bash
git clone https://github.com/davitacols/synthgen.git
cd synthgen
pip install .
```

## Quick Start

Here's how you can use SynthGen to generate synthetic tabular data:

### Example Usage

```python
from synthgen.core import SynthGen

# Initialize the generator
generator = SynthGen(seed=42)

# Generate a dataset with 100 rows, 3 columns
dataset = generator.generate_tabular(
    rows=100,
    cols=3,
    col_types=['numeric', 'categorical', 'numeric'],
    noise=0.1
)

# Display the first few rows
print(dataset.head())

# Save the dataset to a CSV file
dataset.to_csv('synthetic_dataset.csv', index=False)
```

## API Reference

### Class: `SynthGen`

The `SynthGen` class provides methods for generating synthetic datasets.

#### Constructor

```python
SynthGen(seed: int = None)
```

**Parameters**:
- `seed` (int, optional): Random seed for reproducibility. Default is `None`.

#### Method: `generate_tabular`

```python
generate_tabular(rows=100, cols=5, col_types=None, noise=0.0)
```

**Parameters**:
- `rows` (int): Number of rows in the dataset
- `cols` (int): Number of columns in the dataset
- `col_types` (list): List of column types (`numeric`, `categorical`). Defaults to `numeric` for all columns
- `noise` (float): Standard deviation of Gaussian noise for numeric data. Defaults to `0.0`

**Returns**:
- `pandas.DataFrame`: A DataFrame containing the generated dataset

## Directory Structure

```
synthgen/
├── synthgen/
│   ├── __init__.py    # Package initializer
│   ├── core.py        # Core functionality
│   ├── tabular.py     # Tabular data generation
│   └── utils.py       # Helper functions
├── tests/             # Unit tests
│   ├── test_core.py   # Tests for core functionality
│   └── test_tabular.py# Tests for tabular data
├── examples/          # Example usage scripts
│   └── generate_tabular.py
├── README.md          # Project documentation
├── setup.py          # Package configuration for PyPI
├── requirements.txt   # List of dependencies
└── .gitignore        # Ignored files for Git
```

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Commit your changes with a clear message
4. Push the branch and open a pull request

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For questions or support, reach out to:

- **Name:** David Ansa
- **Email:** davitacols@gmail.com
- **GitHub:** davitacols