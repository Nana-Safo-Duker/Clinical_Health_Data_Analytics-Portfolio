"""
Streamlit Cloud Entry Point
Main entry point for Streamlit Cloud deployment.

To deploy:
1. Go to https://share.streamlit.io/
2. Connect your GitHub repository
3. Set Main file path to: streamlit_app.py
4. Or set Main file path to: app/dashboard.py (both work)
"""

# Import all components from the dashboard module
import sys
from pathlib import Path

# Ensure the app directory is in the path
app_dir = Path(__file__).parent / "app"
if str(app_dir) not in sys.path:
    sys.path.insert(0, str(app_dir.parent))

# Import the dashboard (this executes all the Streamlit code)
from app import dashboard
