# Contributing to Differential Gene Expression Dashboard

First off, thank you for considering contributing to this project! It's people like you that make this tool better for the bioinformatics community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Testing](#testing)

---

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the project maintainers.

### Our Standards

- **Be respectful** and inclusive
- **Be collaborative** and constructive
- **Focus on what is best** for the community
- **Show empathy** towards other community members

---

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When reporting bugs, include:**
- Clear, descriptive title
- Steps to reproduce the issue
- Expected vs actual behavior
- Screenshots (if applicable)
- Your environment (OS, Python version, package versions)
- Sample data (if possible)

**Example:**
```markdown
**Bug**: Volcano plot not rendering with large datasets

**Steps to Reproduce:**
1. Upload CSV with 50,000+ genes
2. Set thresholds
3. Navigate to Volcano plot tab

**Expected:** Plot renders
**Actual:** Browser freezes

**Environment:**
- OS: Windows 10
- Python: 3.9.5
- Streamlit: 1.28.0
- Dataset size: 50,000 genes
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**Include:**
- Clear, descriptive title
- Detailed description of the proposed feature
- Why this enhancement would be useful
- Examples of how it would work
- Mockups or sketches (if applicable)

### Pull Requests

We actively welcome your pull requests!

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

### Setup Steps

```bash
# 1. Fork and clone the repository
git clone https://github.com/yourusername/Differential-Gene-Expression.git
cd Differential-Gene-Expression

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Unix or MacOS:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Install development dependencies (if any)
pip install -r requirements-dev.txt

# 6. Run tests to verify setup
python tests/test_dashboard.py
```

### Project Structure

```
Differential-Gene-Expression/
├── app/
│   ├── dashboard.py          # Main application
│   └── utils/               # Utility modules
├── tests/                   # Test files
├── examples/                # Sample data and demos
├── docs/                    # Documentation
└── scripts/                 # Helper scripts
```

---

## Pull Request Process

### Before Submitting

1. **Update documentation** - If you change functionality
2. **Add tests** - For new features
3. **Run existing tests** - Ensure all pass
4. **Update README** - If you add features
5. **Follow style guidelines** - See below

### PR Checklist

- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] Documentation updated
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] No new warnings
- [ ] README updated (if needed)

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How was this tested?

## Screenshots
If applicable

## Checklist
- [ ] Tests pass
- [ ] Documentation updated
- [ ] Follows style guidelines
```

---

## Style Guidelines

### Python Code Style

We follow **PEP 8** with some modifications:

```python
# Good: Clear function names, docstrings, type hints
def calculate_significance(
    padj: float,
    log2fc: float,
    padj_threshold: float = 0.05,
    fc_threshold: float = 1.0
) -> bool:
    """
    Determine if a gene is significantly differentially expressed.
    
    Args:
        padj: Adjusted p-value
        log2fc: Log2 fold change
        padj_threshold: P-value cutoff (default: 0.05)
        fc_threshold: Fold change cutoff (default: 1.0)
    
    Returns:
        True if gene is significant, False otherwise
    """
    return (padj < padj_threshold) and (abs(log2fc) >= fc_threshold)


# Bad: Unclear names, no documentation
def calc(p, f, pt=0.05, ft=1.0):
    return (p < pt) and (abs(f) >= ft)
```

### Code Organization

```python
# 1. Standard library imports
import os
import sys

# 2. Third-party imports
import pandas as pd
import streamlit as st

# 3. Local imports
from utils.validators import validate_data
```

### Naming Conventions

- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: `_leading_underscore`

```python
# Good
MAX_GENES = 50000
class DataValidator:
    pass

def load_gene_data():
    pass

# Bad
maxGenes = 50000
class data_validator:
    pass

def LoadGeneData():
    pass
```

### Documentation

All functions should have docstrings:

```python
def create_volcano_plot(df: pd.DataFrame, threshold: float) -> go.Figure:
    """
    Create an interactive volcano plot.
    
    Args:
        df: DataFrame with columns 'log2FoldChange' and 'padj'
        threshold: Significance threshold for adjusted p-value
    
    Returns:
        Plotly Figure object with volcano plot
    
    Raises:
        ValueError: If required columns are missing
    
    Example:
        >>> df = load_data('results.csv')
        >>> fig = create_volcano_plot(df, 0.05)
        >>> fig.show()
    """
    # Implementation
```

### Streamlit Specific

```python
# Good: Cache expensive operations
@st.cache_data
def load_large_dataset(filepath: str) -> pd.DataFrame:
    return pd.read_csv(filepath)

# Good: Use session state for user data
if 'df_processed' not in st.session_state:
    st.session_state.df_processed = None

# Good: Clear section organization
st.header("Data Upload")
uploaded_file = st.file_uploader("Choose CSV file", type="csv")

if uploaded_file:
    st.subheader("Preview")
    # Processing code
```

---

## Testing

### Running Tests

```bash
# Run all tests
python tests/test_dashboard.py

# Run specific test
python -m pytest tests/test_utils.py::test_validation

# Run with coverage
python -m pytest --cov=app tests/
```

### Writing Tests

```python
def test_significance_calculation():
    """Test that significance is correctly calculated"""
    # Arrange
    padj = 0.01
    log2fc = 2.5
    
    # Act
    result = calculate_significance(padj, log2fc)
    
    # Assert
    assert result == True
    
def test_edge_cases():
    """Test edge cases"""
    assert calculate_significance(0.05, 1.0) == False  # Boundary
    assert calculate_significance(0.049, 1.0) == True  # Just under
    assert calculate_significance(0.01, 0) == False    # No fold change
```

### Test Coverage

- Aim for **>80% code coverage**
- Test edge cases and error conditions
- Include integration tests for key workflows

---

## Documentation

### README Updates

When adding features:
1. Update feature list
2. Add usage examples
3. Update screenshots if UI changes
4. Modify installation if dependencies change

### Docstring Format

Use **Google style** docstrings:

```python
def function_name(param1: str, param2: int) -> bool:
    """
    Short description.
    
    Longer description if needed. Can span multiple
    lines and include details about the function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
    
    Returns:
        Description of return value
    
    Raises:
        ValueError: When param1 is empty
        TypeError: When param2 is not an integer
    
    Example:
        >>> result = function_name("test", 42)
        >>> print(result)
        True
    """
```

---

## Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Formatting, missing semicolons, etc.
- **refactor**: Code restructuring
- **test**: Adding tests
- **chore**: Maintenance tasks

### Examples

```bash
# Good
git commit -m "feat(plots): add heatmap visualization for top genes"
git commit -m "fix(export): resolve Excel export encoding issue"
git commit -m "docs(readme): update installation instructions"

# Bad
git commit -m "update"
git commit -m "fix bug"
git commit -m "changes"
```

---

## Review Process

1. **Automated checks** run on all PRs
2. **Maintainer review** within 48 hours
3. **Address feedback** promptly
4. **Squash and merge** after approval

### What Reviewers Look For

- Code quality and readability
- Test coverage
- Documentation completeness
- Performance implications
- Security considerations
- Breaking changes

---

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in documentation

---

## Questions?

- Open a [GitHub Discussion](https://github.com/yourusername/Differential-Gene-Expression/discussions)
- Check existing [Issues](https://github.com/yourusername/Differential-Gene-Expression/issues)
- Review [Documentation](docs/)

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing to make differential gene expression analysis more accessible!** 🧬✨


