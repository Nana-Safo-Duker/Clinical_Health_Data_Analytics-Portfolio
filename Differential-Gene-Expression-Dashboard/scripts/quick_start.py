#!/usr/bin/env python3
"""
Quick Start Script for Differential Gene Expression Dashboard
This script checks dependencies and launches the dashboard
"""

import sys
import subprocess
import pkg_resources

def check_dependencies():
    """Check if all required packages are installed"""
    required = {
        'streamlit': '1.28.0',
        'pandas': '2.0.0',
        'numpy': '1.24.0',
        'altair': '5.0.0',
        'plotly': '5.17.0',
        'openpyxl': '3.1.0'
    }
    
    missing = []
    outdated = []
    
    print("🔍 Checking dependencies...\n")
    
    for package, min_version in required.items():
        try:
            installed_version = pkg_resources.get_distribution(package).version
            print(f"✅ {package}: {installed_version}")
            
            # Simple version comparison (works for most cases)
            if installed_version < min_version:
                outdated.append((package, installed_version, min_version))
        except pkg_resources.DistributionNotFound:
            print(f"❌ {package}: Not installed")
            missing.append(package)
    
    print()
    
    if missing or outdated:
        print("⚠️  Issues found:\n")
        
        if missing:
            print("Missing packages:")
            for pkg in missing:
                print(f"  - {pkg}")
        
        if outdated:
            print("\nOutdated packages:")
            for pkg, current, required in outdated:
                print(f"  - {pkg}: {current} (requires >= {required})")
        
        print("\n📦 To install/update all dependencies, run:")
        print("   pip install -r requirements.txt")
        print()
        
        response = input("Would you like to install/update now? (y/n): ")
        if response.lower() == 'y':
            print("\n📥 Installing/updating packages...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Installation complete!\n")
        else:
            print("⏭️  Skipping installation. Some features may not work.\n")
    else:
        print("✅ All dependencies are installed and up to date!\n")
    
    return True

def launch_dashboard():
    """Launch the Streamlit dashboard"""
    print("🚀 Launching Differential Gene Expression Dashboard...")
    print("📊 The dashboard will open in your default web browser")
    print("🌐 URL: http://localhost:8501")
    print("\n⚠️  Press Ctrl+C to stop the dashboard\n")
    print("-" * 60)
    
    try:
        subprocess.run([
            "streamlit", "run",
            "Differential_Gene_Dashboard_Enhanced.py",
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n\n👋 Dashboard stopped. Goodbye!")
    except FileNotFoundError:
        print("\n❌ Error: streamlit command not found.")
        print("Please install streamlit: pip install streamlit")
    except Exception as e:
        print(f"\n❌ Error launching dashboard: {e}")

def main():
    print("=" * 60)
    print("🧬 Differential Gene Expression Dashboard - Quick Start")
    print("=" * 60)
    print()
    
    # Check dependencies
    check_dependencies()
    
    # Launch dashboard
    launch_dashboard()

if __name__ == "__main__":
    main()

