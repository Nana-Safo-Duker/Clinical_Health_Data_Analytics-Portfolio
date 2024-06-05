import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO

# Set page config
st.set_page_config(
    page_title="Advanced Differential Gene Expression Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better UI
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🧬 Advanced Differential Gene Expression Dashboard")
st.markdown("""
### Upload your gene expression data and explore comprehensive visualizations
This dashboard provides:
- **Flexible column mapping** for any CSV structure
- **Interactive volcano plots** and other visualizations
- **Advanced filtering** and regulation analysis
- **Statistical summaries** and export capabilities
---
""")

# Initialize session state
if 'df_processed' not in st.session_state:
    st.session_state.df_processed = None
if 'column_mapping' not in st.session_state:
    st.session_state.column_mapping = {}

def validate_data(df, gene_col, logfc_col, padj_col):
    """Validate the selected columns contain appropriate data"""
    errors = []
    
    # Check if columns exist
    if gene_col not in df.columns:
        errors.append(f"Gene column '{gene_col}' not found")
    if logfc_col not in df.columns:
        errors.append(f"Log2FC column '{logfc_col}' not found")
    if padj_col not in df.columns:
        errors.append(f"P-adjusted column '{padj_col}' not found")
    
    if errors:
        return False, errors
    
    # Check if numeric columns are actually numeric
    try:
        pd.to_numeric(df[logfc_col], errors='coerce')
        pd.to_numeric(df[padj_col], errors='coerce')
    except Exception as e:
        errors.append(f"Numeric conversion error: {str(e)}")
        return False, errors
    
    # Check for too many NaN values
    logfc_nan_pct = df[logfc_col].isna().sum() / len(df) * 100
    padj_nan_pct = df[padj_col].isna().sum() / len(df) * 100
    
    if logfc_nan_pct > 50:
        errors.append(f"Log2FC column has {logfc_nan_pct:.1f}% missing values")
    if padj_nan_pct > 50:
        errors.append(f"P-adjusted column has {padj_nan_pct:.1f}% missing values")
    
    if errors:
        return False, errors
    
    return True, []

def create_volcano_plot_altair(df):
    """Create interactive volcano plot using Altair"""
    # Create color column for better visualization
    df['Regulation'] = 'Not Significant'
    df.loc[(df['Significant']) & (df['log2FoldChange'] > 0), 'Regulation'] = 'Upregulated'
    df.loc[(df['Significant']) & (df['log2FoldChange'] < 0), 'Regulation'] = 'Downregulated'
    
    color_scale = alt.Scale(
        domain=['Upregulated', 'Downregulated', 'Not Significant'],
        range=['#d62728', '#2ca02c', '#7f7f7f']
    )
    
    chart = alt.Chart(df.dropna(subset=["-log10(padj)"])).mark_circle(size=60, opacity=0.7).encode(
        x=alt.X("log2FoldChange:Q", 
                title="log₂ Fold Change",
                scale=alt.Scale(domain=[df['log2FoldChange'].min() - 0.5, df['log2FoldChange'].max() + 0.5])),
        y=alt.Y("-log10(padj):Q", 
                title="-log₁₀ Adjusted P-value"),
        color=alt.Color('Regulation:N', 
                       scale=color_scale,
                       legend=alt.Legend(title="Gene Regulation")),
        tooltip=[
            alt.Tooltip('Gene:N', title='Gene'),
            alt.Tooltip('log2FoldChange:Q', title='Log2 FC', format='.3f'),
            alt.Tooltip('padj:Q', title='Adj. P-value', format='.2e'),
            alt.Tooltip('Regulation:N', title='Status')
        ]
    ).properties(
        width=800,
        height=600,
        title="Volcano Plot: Differential Gene Expression"
    ).interactive()
    
    return chart

def create_volcano_plot_plotly(df):
    """Create interactive volcano plot using Plotly"""
    df['Regulation'] = 'Not Significant'
    df.loc[(df['Significant']) & (df['log2FoldChange'] > 0), 'Regulation'] = 'Upregulated'
    df.loc[(df['Significant']) & (df['log2FoldChange'] < 0), 'Regulation'] = 'Downregulated'
    
    color_map = {
        'Upregulated': '#d62728',
        'Downregulated': '#2ca02c',
        'Not Significant': '#7f7f7f'
    }
    
    fig = px.scatter(
        df.dropna(subset=["-log10(padj)"]),
        x='log2FoldChange',
        y='-log10(padj)',
        color='Regulation',
        color_discrete_map=color_map,
        hover_data={
            'Gene': True,
            'log2FoldChange': ':.3f',
            'padj': ':.2e',
            'Regulation': True,
            '-log10(padj)': False
        },
        labels={
            'log2FoldChange': 'log₂ Fold Change',
            '-log10(padj)': '-log₁₀ Adjusted P-value'
        },
        title="Volcano Plot: Differential Gene Expression"
    )
    
    fig.update_traces(marker=dict(size=8, opacity=0.7, line=dict(width=0)))
    fig.update_layout(
        height=600,
        hovermode='closest',
        template='plotly_white'
    )
    
    return fig

def create_ma_plot(df):
    """Create MA plot (log2FC vs mean expression)"""
    if 'baseMean' in df.columns:
        df['log10BaseMean'] = np.log10(df['baseMean'] + 1)
        
        fig = px.scatter(
            df,
            x='log10BaseMean',
            y='log2FoldChange',
            color='Significant',
            color_discrete_map={True: '#d62728', False: '#7f7f7f'},
            hover_data={
                'Gene': True,
                'log2FoldChange': ':.3f',
                'padj': ':.2e',
                'log10BaseMean': False
            },
            labels={
                'log10BaseMean': 'log₁₀ Mean Expression',
                'log2FoldChange': 'log₂ Fold Change',
                'Significant': 'Significant'
            },
            title="MA Plot: log₂ Fold Change vs Mean Expression"
        )
        
        fig.add_hline(y=0, line_dash="dash", line_color="gray", opacity=0.5)
        fig.update_traces(marker=dict(size=6, opacity=0.6))
        fig.update_layout(height=600, template='plotly_white')
        
        return fig
    return None

def create_top_genes_chart(df, n_genes=20):
    """Create bar chart of top differentially expressed genes"""
    top_up = df[(df['Significant']) & (df['log2FoldChange'] > 0)].nlargest(n_genes // 2, 'log2FoldChange')
    top_down = df[(df['Significant']) & (df['log2FoldChange'] < 0)].nsmallest(n_genes // 2, 'log2FoldChange')
    top_genes = pd.concat([top_up, top_down]).sort_values('log2FoldChange')
    
    if len(top_genes) == 0:
        return None
    
    fig = px.bar(
        top_genes,
        x='log2FoldChange',
        y='Gene',
        orientation='h',
        color='log2FoldChange',
        color_continuous_scale=['green', 'gray', 'red'],
        color_continuous_midpoint=0,
        labels={'log2FoldChange': 'log₂ Fold Change'},
        title=f"Top {len(top_genes)} Differentially Expressed Genes",
        hover_data={'padj': ':.2e'}
    )
    
    fig.update_layout(
        height=max(400, len(top_genes) * 25),
        yaxis={'categoryorder': 'total ascending'},
        template='plotly_white'
    )
    
    return fig

def create_distribution_plot(df):
    """Create distribution plots for log2FC and p-values"""
    fig = go.Figure()
    
    # Log2 Fold Change distribution
    fig.add_trace(go.Histogram(
        x=df['log2FoldChange'],
        name='log₂ Fold Change',
        opacity=0.7,
        marker_color='steelblue',
        nbinsx=50
    ))
    
    fig.update_layout(
        title="Distribution of log₂ Fold Change",
        xaxis_title="log₂ Fold Change",
        yaxis_title="Frequency",
        height=400,
        template='plotly_white',
        showlegend=False
    )
    
    return fig

def create_pvalue_distribution(df):
    """Create p-value distribution plot"""
    fig = go.Figure()
    
    fig.add_trace(go.Histogram(
        x=df['padj'],
        name='Adjusted P-value',
        opacity=0.7,
        marker_color='coral',
        nbinsx=50
    ))
    
    fig.update_layout(
        title="Distribution of Adjusted P-values",
        xaxis_title="Adjusted P-value",
        yaxis_title="Frequency",
        height=400,
        template='plotly_white',
        showlegend=False
    )
    
    return fig

def export_to_excel(df):
    """Export dataframe to Excel format"""
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Significant_Genes')
    output.seek(0)
    return output

# Sidebar for file upload and settings
with st.sidebar:
    st.header("📁 Data Upload")
    uploaded_file = st.file_uploader("Upload CSV file", type="csv")
    
    if uploaded_file:
        st.success("✅ File uploaded!")
        
        # Option to show raw data
        show_raw = st.checkbox("Show raw data preview", value=False)

# Main content
if uploaded_file:
    try:
        # Load data
        df_raw = pd.read_csv(uploaded_file)
        df_raw.columns = df_raw.columns.str.strip()
        
        if show_raw:
            st.subheader("📊 Raw Data Preview")
            st.dataframe(df_raw.head(10), use_container_width=True)
            st.caption(f"Total rows: {len(df_raw):,} | Total columns: {len(df_raw.columns)}")
        
        # Column selection
        st.subheader("🔧 Column Mapping")
        st.markdown("Select the columns from your dataset that correspond to the required fields:")
        
        col1, col2, col3, col4 = st.columns(4)
        
        all_cols = list(df_raw.columns)
        
        with col1:
            gene_col = st.selectbox("🧬 Gene Name Column", all_cols, key='gene_col')
        with col2:
            logfc_col = st.selectbox("📊 Log2 Fold Change", all_cols, 
                                    index=min(1, len(all_cols)-1) if len(all_cols) > 1 else 0,
                                    key='logfc_col')
        with col3:
            padj_col = st.selectbox("📈 Adjusted P-value", all_cols,
                                   index=min(2, len(all_cols)-1) if len(all_cols) > 2 else 0,
                                   key='padj_col')
        with col4:
            regulation_col = st.selectbox("🔄 Regulation Column (Optional)", ["None"] + all_cols, key='reg_col')
        
        # Additional optional columns
        with st.expander("⚙️ Additional Optional Columns"):
            col_a, col_b = st.columns(2)
            with col_a:
                basemean_col = st.selectbox("Mean Expression (baseMean)", ["None"] + all_cols)
            with col_b:
                pvalue_col = st.selectbox("Raw P-value", ["None"] + all_cols)
        
        # Validate selections
        is_valid, errors = validate_data(df_raw, gene_col, logfc_col, padj_col)
        
        if not is_valid:
            st.error("❌ Data validation failed:")
            for error in errors:
                st.error(f"  • {error}")
            st.stop()
        
        # Process data
        df = df_raw.copy()
        df = df.rename(columns={
            gene_col: "Gene",
            logfc_col: "log2FoldChange",
            padj_col: "padj"
        })
        
        if regulation_col != "None":
            df = df.rename(columns={regulation_col: "regulation"})
        
        if basemean_col != "None":
            df = df.rename(columns={basemean_col: "baseMean"})
            df["baseMean"] = pd.to_numeric(df["baseMean"], errors="coerce")
        
        if pvalue_col != "None":
            df = df.rename(columns={pvalue_col: "pvalue"})
            df["pvalue"] = pd.to_numeric(df["pvalue"], errors="coerce")
        
        # Convert to numeric
        df["log2FoldChange"] = pd.to_numeric(df["log2FoldChange"], errors="coerce")
        df["padj"] = pd.to_numeric(df["padj"], errors="coerce")
        
        # Remove rows with NaN in critical columns
        initial_rows = len(df)
        df = df.dropna(subset=["Gene", "log2FoldChange", "padj"])
        removed_rows = initial_rows - len(df)
        
        if removed_rows > 0:
            st.warning(f"⚠️ Removed {removed_rows:,} rows with missing values in critical columns")
        
        # Calculate -log10(padj)
        df["-log10(padj)"] = df["padj"].apply(lambda x: -np.log10(x) if x > 0 else np.nan)
        df = df.dropna(subset=["-log10(padj)"])
        
        st.success(f"✅ Data processed successfully! {len(df):,} genes loaded.")
        
        # Filter settings
        st.markdown("---")
        st.subheader("🎚️ Significance Thresholds")
        
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            logfc_threshold = st.slider(
                "log₂ Fold Change Threshold",
                min_value=0.0,
                max_value=5.0,
                value=1.0,
                step=0.1,
                help="Genes with |log2FC| >= this value are considered significant"
            )
        
        with col2:
            padj_threshold = st.slider(
                "Adjusted P-value Threshold",
                min_value=0.0,
                max_value=0.1,
                value=0.05,
                step=0.005,
                format="%.3f",
                help="Genes with adjusted p-value < this value are considered significant"
            )
        
        with col3:
            st.metric("log₂FC cutoff", f"±{logfc_threshold}")
            st.metric("p-adj cutoff", f"{padj_threshold}")
        
        # Calculate significance
        df["Significant"] = (
            (df["padj"] < padj_threshold) &
            (df["log2FoldChange"].abs() >= logfc_threshold)
        )
        
        # Regulation filter
        if "regulation" in df.columns:
            st.markdown("### 🔍 Filter by Regulation")
            unique_regs = ["All"] + sorted(df["regulation"].dropna().unique().tolist())
            regulation_filter = st.selectbox("Select regulation type:", unique_regs)
            
            if regulation_filter != "All":
                df_filtered = df[df["regulation"] == regulation_filter].copy()
            else:
                df_filtered = df.copy()
        else:
            df_filtered = df.copy()
        
        # Gene search functionality
        st.markdown("### 🔎 Search Specific Genes")
        gene_search = st.text_input("Search for genes (comma-separated)", placeholder="e.g., TP53, BRCA1, EGFR")
        
        if gene_search:
            search_genes = [g.strip().upper() for g in gene_search.split(',')]
            df_filtered['Gene_upper'] = df_filtered['Gene'].str.upper()
            df_searched = df_filtered[df_filtered['Gene_upper'].isin(search_genes)]
            
            if len(df_searched) > 0:
                st.success(f"Found {len(df_searched)} matching gene(s)")
                st.dataframe(df_searched.drop('Gene_upper', axis=1), use_container_width=True)
            else:
                st.warning("No matching genes found")
        
        # Statistics summary
        st.markdown("---")
        st.subheader("📊 Summary Statistics")
        
        total_genes = len(df_filtered)
        sig_genes = df_filtered["Significant"].sum()
        up_genes = ((df_filtered["Significant"]) & (df_filtered["log2FoldChange"] > 0)).sum()
        down_genes = ((df_filtered["Significant"]) & (df_filtered["log2FoldChange"] < 0)).sum()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Genes", f"{total_genes:,}")
        with col2:
            st.metric("Significant Genes", f"{sig_genes:,}", 
                     delta=f"{sig_genes/total_genes*100:.1f}%")
        with col3:
            st.metric("Upregulated", f"{up_genes:,}",
                     delta=f"{up_genes/sig_genes*100:.1f}%" if sig_genes > 0 else "0%")
        with col4:
            st.metric("Downregulated", f"{down_genes:,}",
                     delta=f"{down_genes/sig_genes*100:.1f}%" if sig_genes > 0 else "0%")
        
        # Visualization tabs
        st.markdown("---")
        st.subheader("📈 Visualizations")
        
        viz_tabs = st.tabs([
            "🌋 Volcano Plot",
            "📊 Top Genes",
            "📉 Distributions",
            "🔬 MA Plot" if 'baseMean' in df_filtered.columns else "🔬 MA Plot (N/A)",
            "📋 Data Table"
        ])
        
        with viz_tabs[0]:
            st.markdown("#### Interactive Volcano Plot")
            plot_engine = st.radio("Select plot engine:", ["Plotly (Recommended)", "Altair"], horizontal=True)
            
            if plot_engine == "Plotly (Recommended)":
                fig = create_volcano_plot_plotly(df_filtered)
                st.plotly_chart(fig, use_container_width=True)
            else:
                chart = create_volcano_plot_altair(df_filtered)
                st.altair_chart(chart, use_container_width=True)
            
            # Add threshold lines info
            st.info(f"🎯 Current thresholds: |log₂FC| ≥ {logfc_threshold}, adjusted p-value < {padj_threshold}")
        
        with viz_tabs[1]:
            st.markdown("#### Top Differentially Expressed Genes")
            n_genes = st.slider("Number of top genes to display:", 10, 50, 20, 5)
            
            fig_top = create_top_genes_chart(df_filtered, n_genes)
            if fig_top:
                st.plotly_chart(fig_top, use_container_width=True)
            else:
                st.warning("No significant genes found with current thresholds")
        
        with viz_tabs[2]:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### log₂ Fold Change Distribution")
                fig_dist = create_distribution_plot(df_filtered)
                st.plotly_chart(fig_dist, use_container_width=True)
            
            with col2:
                st.markdown("#### Adjusted P-value Distribution")
                fig_pval = create_pvalue_distribution(df_filtered)
                st.plotly_chart(fig_pval, use_container_width=True)
        
        with viz_tabs[3]:
            if 'baseMean' in df_filtered.columns:
                st.markdown("#### MA Plot")
                fig_ma = create_ma_plot(df_filtered)
                if fig_ma:
                    st.plotly_chart(fig_ma, use_container_width=True)
            else:
                st.info("ℹ️ MA plot requires a 'baseMean' column. Please map this column in the optional settings above.")
        
        with viz_tabs[4]:
            st.markdown("#### Significantly Differentially Expressed Genes")
            
            # Additional filtering options
            col1, col2 = st.columns([3, 1])
            with col1:
                sort_by = st.selectbox("Sort by:", ["padj", "log2FoldChange", "Gene"])
            with col2:
                sort_order = st.radio("Order:", ["Ascending", "Descending"])
            
            sig_df = df_filtered[df_filtered["Significant"]].copy()
            
            if len(sig_df) > 0:
                sig_df = sig_df.sort_values(
                    sort_by,
                    ascending=(sort_order == "Ascending")
                ).reset_index(drop=True)
                
                st.dataframe(
                    sig_df.style.format({
                        'log2FoldChange': '{:.3f}',
                        'padj': '{:.2e}',
                        '-log10(padj)': '{:.2f}'
                    }),
                    use_container_width=True,
                    height=400
                )
                
                st.caption(f"Showing {len(sig_df):,} significant genes")
            else:
                st.warning("No significant genes found with current thresholds")
        
        # Export section
        st.markdown("---")
        st.subheader("💾 Export Results")
        
        col1, col2, col3 = st.columns(3)
        
        sig_df_export = df_filtered[df_filtered["Significant"]].copy()
        
        with col1:
            if len(sig_df_export) > 0:
                csv = sig_df_export.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Significant Genes (CSV)",
                    data=csv,
                    file_name="significant_genes.csv",
                    mime="text/csv"
                )
            else:
                st.button("📥 Download Significant Genes (CSV)", disabled=True)
        
        with col2:
            if len(sig_df_export) > 0:
                excel_data = export_to_excel(sig_df_export)
                st.download_button(
                    label="📥 Download Significant Genes (Excel)",
                    data=excel_data,
                    file_name="significant_genes.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            else:
                st.button("📥 Download Significant Genes (Excel)", disabled=True)
        
        with col3:
            all_csv = df_filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download All Filtered Data (CSV)",
                data=all_csv,
                file_name="all_filtered_genes.csv",
                mime="text/csv"
            )
        
        # Store processed data in session state
        st.session_state.df_processed = df_filtered
        
    except Exception as e:
        st.error(f"❌ An error occurred while processing your file:")
        st.exception(e)
        st.info("💡 Please ensure your CSV file is properly formatted and contains the required columns.")

else:
    # Landing page
    st.info("👆 Please upload a CSV file to begin analysis")
    
    st.markdown("""
    ### 📋 Expected Data Format
    
    Your CSV file should contain at minimum:
    - **Gene names** (e.g., gene IDs or symbols)
    - **log₂ Fold Change** values
    - **Adjusted P-values** (e.g., from DESeq2, edgeR, or similar)
    
    **Optional columns:**
    - Regulation status (Upregulated/Downregulated)
    - Base mean expression values
    - Raw p-values
    
    ### 🎯 Features
    
    ✅ **Flexible Column Mapping** - Works with any CSV structure  
    ✅ **Interactive Visualizations** - Volcano plots, MA plots, distributions  
    ✅ **Advanced Filtering** - Custom thresholds and gene search  
    ✅ **Statistical Summaries** - Comprehensive gene expression statistics  
    ✅ **Export Capabilities** - Download results in CSV or Excel format  
    ✅ **Publication-Ready Plots** - High-quality, interactive visualizations  
    
    ### 📊 Example Data Structure
    
    ```
    Gene,log2FoldChange,padj,regulation
    TP53,2.5,0.001,Upregulated
    BRCA1,-1.8,0.01,Downregulated
    EGFR,3.2,0.0001,Upregulated
    ```
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>🧬 Advanced Differential Gene Expression Dashboard | Built with Streamlit</p>
    <p style='font-size: 0.8em;'>Analyze, visualize, and export your gene expression data with ease</p>
</div>
""", unsafe_allow_html=True)

