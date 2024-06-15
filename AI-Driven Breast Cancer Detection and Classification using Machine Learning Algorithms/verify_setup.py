"""
Verification script to check if all dependencies are installed correctly
"""

import sys

def check_python_packages():
    """Check if all required Python packages are installed"""
    required_packages = [
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'scipy',
        'sklearn',
        'xgboost',
        'lightgbm',
        'jupyter'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✓ {package} is installed")
        except ImportError:
            print(f"✗ {package} is NOT installed")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    else:
        print("\n✓ All required Python packages are installed!")
        return True

def check_data_file():
    """Check if data file exists"""
    import os
    data_path = os.path.join('data', 'breast_cancer.csv')
    
    if os.path.exists(data_path):
        print(f"✓ Data file found at {data_path}")
        return True
    else:
        print(f"✗ Data file not found at {data_path}")
        return False

def check_project_structure():
    """Check if project structure is correct"""
    import os
    required_dirs = [
        'data',
        'notebooks/python',
        'notebooks/r',
        'scripts/python',
        'scripts/r',
        'results'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✓ {dir_path} exists")
        else:
            print(f"✗ {dir_path} does NOT exist")
            all_exist = False
    
    return all_exist

def main():
    """Main verification function"""
    print("=" * 60)
    print("PROJECT SETUP VERIFICATION")
    print("=" * 60)
    
    print("\n1. Checking Python packages...")
    packages_ok = check_python_packages()
    
    print("\n2. Checking data file...")
    data_ok = check_data_file()
    
    print("\n3. Checking project structure...")
    structure_ok = check_project_structure()
    
    print("\n" + "=" * 60)
    if packages_ok and data_ok and structure_ok:
        print("✓ ALL CHECKS PASSED! Project is ready to use.")
        return 0
    else:
        print("✗ SOME CHECKS FAILED! Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())

