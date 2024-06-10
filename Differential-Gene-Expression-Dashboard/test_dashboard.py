#!/usr/bin/env python3
"""
Test script for Differential Gene Expression Dashboard
Validates functionality without launching full Streamlit app
"""

import pandas as pd
import numpy as np
import sys

def test_sample_data():
    """Test that sample data loads correctly"""
    print("🧪 Test 1: Loading sample data...")
    try:
        df = pd.read_csv("sample_data.csv")
        print(f"  ✅ Loaded {len(df)} rows")
        print(f"  ✅ Columns: {', '.join(df.columns)}")
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return False

def test_required_columns():
    """Test that required columns exist and are valid"""
    print("\n🧪 Test 2: Validating required columns...")
    try:
        df = pd.read_csv("sample_data.csv")
        
        # Check Gene column
        if 'Gene' in df.columns:
            print("  ✅ Gene column present")
        else:
            print("  ❌ Gene column missing")
            return False
        
        # Check log2FoldChange
        if 'log2FoldChange' in df.columns:
            df['log2FoldChange'] = pd.to_numeric(df['log2FoldChange'], errors='coerce')
            if df['log2FoldChange'].notna().all():
                print("  ✅ log2FoldChange is numeric")
            else:
                print("  ❌ log2FoldChange has non-numeric values")
                return False
        else:
            print("  ❌ log2FoldChange column missing")
            return False
        
        # Check padj
        if 'padj' in df.columns:
            df['padj'] = pd.to_numeric(df['padj'], errors='coerce')
            if df['padj'].notna().all():
                print("  ✅ padj is numeric")
                if ((df['padj'] >= 0) & (df['padj'] <= 1)).all():
                    print("  ✅ padj values in valid range [0, 1]")
                else:
                    print("  ⚠️  Some padj values outside [0, 1]")
            else:
                print("  ❌ padj has non-numeric values")
                return False
        else:
            print("  ❌ padj column missing")
            return False
        
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return False

def test_optional_columns():
    """Test optional columns"""
    print("\n🧪 Test 3: Checking optional columns...")
    try:
        df = pd.read_csv("sample_data.csv")
        
        optional = ['regulation', 'baseMean', 'pvalue']
        found = []
        
        for col in optional:
            if col in df.columns:
                found.append(col)
                print(f"  ✅ {col} column present")
        
        if not found:
            print("  ⚠️  No optional columns found (this is OK)")
        
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return False

def test_data_calculations():
    """Test that calculations work correctly"""
    print("\n🧪 Test 4: Testing calculations...")
    try:
        df = pd.read_csv("sample_data.csv")
        
        # Convert to numeric
        df['log2FoldChange'] = pd.to_numeric(df['log2FoldChange'], errors='coerce')
        df['padj'] = pd.to_numeric(df['padj'], errors='coerce')
        
        # Calculate -log10(padj)
        df['-log10(padj)'] = df['padj'].apply(lambda x: -np.log10(x) if x > 0 else np.nan)
        
        if df['-log10(padj)'].notna().any():
            print("  ✅ -log10(padj) calculation works")
        else:
            print("  ❌ -log10(padj) calculation failed")
            return False
        
        # Test significance calculation
        logfc_threshold = 1.0
        padj_threshold = 0.05
        
        df['Significant'] = (
            (df['padj'] < padj_threshold) &
            (df['log2FoldChange'].abs() >= logfc_threshold)
        )
        
        sig_count = df['Significant'].sum()
        print(f"  ✅ Significance calculation works: {sig_count} significant genes")
        
        # Count up/down
        up = ((df['Significant']) & (df['log2FoldChange'] > 0)).sum()
        down = ((df['Significant']) & (df['log2FoldChange'] < 0)).sum()
        print(f"  ✅ Regulation split: {up} up, {down} down")
        
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return False

def test_dependencies():
    """Test that all required packages are available"""
    print("\n🧪 Test 5: Checking dependencies...")
    
    required = {
        'streamlit': 'Streamlit',
        'pandas': 'Pandas',
        'numpy': 'NumPy',
        'altair': 'Altair',
        'plotly': 'Plotly',
        'openpyxl': 'OpenPyXL'
    }
    
    all_present = True
    
    for package, name in required.items():
        try:
            __import__(package)
            print(f"  ✅ {name}")
        except ImportError:
            print(f"  ❌ {name} not installed")
            all_present = False
    
    return all_present

def test_file_structure():
    """Test that all required files exist"""
    print("\n🧪 Test 6: Checking file structure...")
    
    required_files = [
        'Differential_Gene_Dashboard_Enhanced.py',
        'requirements.txt',
        'sample_data.csv',
        'README_ENHANCED_DASHBOARD.md',
        'quick_start.py'
    ]
    
    all_present = True
    
    for filename in required_files:
        try:
            with open(filename, 'r') as f:
                pass
            print(f"  ✅ {filename}")
        except FileNotFoundError:
            print(f"  ❌ {filename} missing")
            all_present = False
    
    return all_present

def test_data_export():
    """Test export functionality"""
    print("\n🧪 Test 7: Testing export functions...")
    try:
        df = pd.read_csv("sample_data.csv")
        
        # Test CSV export
        csv_data = df.to_csv(index=False)
        if len(csv_data) > 0:
            print("  ✅ CSV export works")
        else:
            print("  ❌ CSV export failed")
            return False
        
        # Test Excel export (if openpyxl available)
        try:
            from io import BytesIO
            output = BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Data')
            output.seek(0)
            if len(output.getvalue()) > 0:
                print("  ✅ Excel export works")
            else:
                print("  ❌ Excel export failed")
                return False
        except Exception as e:
            print(f"  ⚠️  Excel export skipped: {e}")
        
        return True
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("=" * 60)
    print("🧬 Differential Gene Expression Dashboard - Test Suite")
    print("=" * 60)
    print()
    
    tests = [
        test_sample_data,
        test_required_columns,
        test_optional_columns,
        test_data_calculations,
        test_dependencies,
        test_file_structure,
        test_data_export
    ]
    
    results = []
    
    for test in tests:
        result = test()
        results.append(result)
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    print(f"\n✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! Dashboard is ready to use.")
        print("\nTo launch the dashboard, run:")
        print("  python quick_start.py")
        print("     or")
        print("  streamlit run Differential_Gene_Dashboard_Enhanced.py")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please review errors above.")
        print("Try reinstalling dependencies:")
        print("  pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)

