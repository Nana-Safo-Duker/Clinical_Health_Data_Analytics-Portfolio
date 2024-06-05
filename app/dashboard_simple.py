"""
Simplified test version to diagnose blank page issue
Use this if the main dashboard shows blank
"""
import streamlit as st

# CRITICAL: Page config must be FIRST
st.set_page_config(
    page_title="Test Dashboard",
    layout="wide"
)

st.title("🧬 Test - Dashboard Loading")
st.success("✅ If you see this, Streamlit is working!")

st.write("Testing imports...")

try:
    import pandas as pd
    st.success("✅ pandas imported")
except Exception as e:
    st.error(f"❌ pandas error: {e}")

try:
    import numpy as np
    st.success("✅ numpy imported")
except Exception as e:
    st.error(f"❌ numpy error: {e}")

try:
    import plotly.express as px
    st.success("✅ plotly imported")
except Exception as e:
    st.error(f"❌ plotly error: {e}")

try:
    import altair as alt
    st.success("✅ altair imported")
except Exception as e:
    st.error(f"❌ altair error: {e}")

st.info("If all imports succeeded, the main dashboard should work. Check Streamlit Cloud logs for runtime errors.")

