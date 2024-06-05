# Installation Guide

Complete installation instructions for the Differential Gene Expression Dashboard.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
- [Verification](#verification)
- [Troubleshooting](#troubleshooting)
- [Platform-Specific Notes](#platform-specific-notes)

---

## Prerequisites

### System Requirements

- **Operating System**: Windows 10+, macOS 10.14+, or Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Disk Space**: 500MB for installation + space for data

### Python Packages

All required packages are automatically installed. Main dependencies:
- streamlit >= 1.28.0
- pandas >= 2.0.0
- numpy >= 1.24.0
- plotly >= 5.17.0
- altair >= 5.0.0
- openpyxl >= 3.1.0

---

## Installation Methods

### Method 1: Quick Install (Recommended)

```bash
# Clone the repository
git clone https://github.com/yourusername/Differential-Gene-Expression.git
cd Differential-Gene-Expression

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app/dashboard.py
```

### Method 2: Using pip (PyPI)

Once published to PyPI:

```bash
# Install from PyPI
pip install differential-gene-expression-dashboard

# Run the dashboard
degdash
```

### Method 3: Using setup.py

```bash
# Clone the repository
git clone https://github.com/yourusername/Differential-Gene-Expression.git
cd Differential-Gene-Expression

# Install in editable mode (for development)
pip install -e .

# Or regular installation
pip install .
```

### Method 4: With Virtual Environment (Recommended for Isolation)

#### Using venv

```bash
# Create virtual environment
python -m venv degdash-env

# Activate (Windows)
degdash-env\Scripts\activate

# Activate (Unix/MacOS)
source degdash-env/bin/activate

# Install
pip install -r requirements.txt
```

#### Using conda

```bash
# Create conda environment
conda create -n degdash python=3.10

# Activate environment
conda activate degdash

# Install dependencies
pip install -r requirements.txt
```

---

## Verification

### Test Installation

```bash
# Run test suite
python tests/test_dashboard.py
```

Expected output:
```
============================================================
🧬 Differential Gene Expression Dashboard - Test Suite
============================================================

🧪 Test 1: Loading sample data... ✅ PASSED
🧪 Test 2: Validating required columns... ✅ PASSED
🧪 Test 3: Checking optional columns... ✅ PASSED
🧪 Test 4: Testing calculations... ✅ PASSED
🧪 Test 5: Checking dependencies... ✅ PASSED
🧪 Test 6: Checking file structure... ✅ PASSED
🧪 Test 7: Testing export functions... ✅ PASSED

📊 Test Summary
✅ Passed: 7/7

🎉 All tests passed! Dashboard is ready to use.
```

### Launch Dashboard

```bash
streamlit run app/dashboard.py
```

The dashboard should open in your browser at `http://localhost:8501`

---

## Troubleshooting

### Common Issues

#### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
pip install streamlit
# or
pip install -r requirements.txt
```

#### Issue: "Python version not supported"

**Solution:**
Upgrade Python to 3.8 or higher:
```bash
python --version  # Check current version
# Download from https://www.python.org/downloads/
```

#### Issue: "Permission denied" on Linux/MacOS

**Solution:**
```bash
# Use user installation
pip install --user -r requirements.txt

# Or use sudo (not recommended)
sudo pip install -r requirements.txt
```

#### Issue: Dashboard won't start on Windows

**Solution:**
```bash
# Check if Streamlit is in PATH
where streamlit

# If not found, use python -m
python -m streamlit run app/dashboard.py
```

#### Issue: "Port 8501 already in use"

**Solution:**
```bash
# Use different port
streamlit run app/dashboard.py --server.port 8502

# Or kill existing process
# Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Linux/MacOS:
lsof -i :8501
kill -9 <PID>
```

#### Issue: Slow installation on Windows

**Solution:**
```bash
# Use pre-built wheels
pip install --prefer-binary -r requirements.txt

# Or upgrade pip
python -m pip install --upgrade pip
```

---

## Platform-Specific Notes

### Windows

**Using PowerShell:**
```powershell
# Enable script execution (if needed)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Activate virtual environment
.\venv\Scripts\Activate.ps1
```

**Using Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

**Firewall:**
Windows Defender may ask for network access permission. Click "Allow access" for the dashboard to work.

### macOS

**Install Python via Homebrew:**
```bash
brew install python@3.10
```

**Fix SSL certificate issues:**
```bash
# If you get SSL errors
/Applications/Python\ 3.10/Install\ Certificates.command
```

### Linux (Ubuntu/Debian)

**Install Python and dependencies:**
```bash
sudo apt update
sudo apt install python3.10 python3-pip python3-venv

# Install build dependencies
sudo apt install build-essential
```

### Linux (Red Hat/CentOS)

```bash
sudo yum install python3 python3-pip
sudo yum groupinstall "Development Tools"
```

---

## Development Installation

For contributors and developers:

```bash
# Clone repository
git clone https://github.com/yourusername/Differential-Gene-Expression.git
cd Differential-Gene-Expression

# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install in development mode with dev dependencies
pip install -e .
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/
python tests/test_dashboard.py
```

---

## Updating

### Update from Git

```bash
cd Differential-Gene-Expression
git pull origin main
pip install --upgrade -r requirements.txt
```

### Update from PyPI

```bash
pip install --upgrade differential-gene-expression-dashboard
```

---

## Uninstallation

```bash
# If installed via pip
pip uninstall differential-gene-expression-dashboard

# Remove virtual environment
rm -rf venv  # or rmdir /s venv on Windows

# Remove cloned repository
cd ..
rm -rf Differential-Gene-Expression
```

---

## Docker Installation (Alternative)

Coming soon! Docker support is planned for version 2.1.0.

---

## Next Steps

After successful installation:

1. **Try the sample data**: `examples/sample_data.csv`
2. **Read the user guide**: [docs/USER_GUIDE.md](USER_GUIDE.md)
3. **Prepare your data**: Export from DESeq2/edgeR
4. **Launch and analyze!**

---

## Getting Help

If you encounter issues not covered here:

1. Check [Troubleshooting section](#troubleshooting)
2. Search [GitHub Issues](https://github.com/yourusername/Differential-Gene-Expression/issues)
3. Open a new issue with:
   - Operating system and version
   - Python version (`python --version`)
   - Error message (full traceback)
   - Steps to reproduce

---

## System Compatibility Matrix

| OS | Python 3.8 | Python 3.9 | Python 3.10 | Python 3.11 | Python 3.12 |
|----|------------|------------|-------------|-------------|-------------|
| Windows 10+ | ✅ | ✅ | ✅ | ✅ | ✅ |
| macOS 10.14+ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Ubuntu 20.04+ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Debian 11+ | ✅ | ✅ | ✅ | ✅ | ✅ |
| CentOS 8+ | ✅ | ✅ | ✅ | ✅ | ⚠️ |

✅ Fully supported | ⚠️ Limited testing | ❌ Not supported

---

**Version**: 2.0.0  
**Last Updated**: October 2025


