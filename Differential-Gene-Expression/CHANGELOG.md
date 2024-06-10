# Changelog

All notable changes to the Differential Gene Expression Dashboard will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-10-28

### Added
- **Enhanced Dashboard**: Complete redesign with 10x more features
- **Multiple Visualizations**:
  - Interactive volcano plots (Plotly and Altair engines)
  - MA plots for expression-dependent bias detection
  - Top genes bar charts with customizable gene count
  - Distribution plots for log2FC and p-values
- **Advanced Filtering**:
  - Adjustable log2 fold change thresholds
  - P-value significance cutoffs
  - Regulation status filtering
  - Multi-gene search functionality
- **Export Capabilities**:
  - CSV export for significant genes
  - Excel export with formatting
  - Complete dataset export option
- **Data Validation**:
  - Comprehensive column validation
  - Numeric type checking
  - Missing data detection and reporting
  - User-friendly error messages
- **Real-time Statistics**:
  - Total genes count
  - Significant genes with percentage
  - Up/downregulated gene counts
  - Distribution metrics
- **Quality Features**:
  - Session state management
  - Custom CSS styling
  - Tabbed interface for better organization
  - Metric cards with visual indicators
- **Documentation**:
  - Comprehensive USER_GUIDE.md with tutorials
  - API.md for function reference
  - IMPROVEMENTS.md with feature comparison
  - PROJECT_SUMMARY.md with overview
  - CONTRIBUTING.md for contributors
- **Testing**:
  - Automated test suite (7 comprehensive tests)
  - Sample data for testing (51 genes)
  - Quick start script with dependency checking
- **Project Structure**:
  - Professional directory organization
  - Modular code architecture
  - Proper Python package structure

### Changed
- **UI/UX**: Complete redesign with modern, professional interface
- **Error Handling**: From generic to specific, actionable error messages
- **Performance**: Optimized data processing with better memory management
- **Code Quality**: Refactored for better maintainability and extensibility

### Fixed
- Column name flexibility (works with any CSV structure)
- NaN value handling throughout the pipeline
- Edge cases in significance calculations
- Export functionality for large datasets

## [1.0.0] - 2025-10-20

### Added
- Initial release with basic functionality
- Single volcano plot visualization
- Basic column mapping
- Threshold sliders for filtering
- Simple data upload

---

## Version Numbering

- **Major version** (X.0.0): Incompatible API changes
- **Minor version** (0.X.0): Added functionality (backward compatible)
- **Patch version** (0.0.X): Bug fixes (backward compatible)

---

## Upgrade Guide

### From 1.0.0 to 2.0.0

The dashboard is **100% backward compatible**. Your existing CSV files will work without modification.

**New Features Available:**
1. Try different visualization types in the new tabbed interface
2. Use the gene search box to find specific genes
3. Export your results in CSV or Excel format
4. Explore MA plots if your data includes baseMean column
5. View real-time statistics in the metrics dashboard

**Breaking Changes:** None

---

## Future Releases

### Planned for 2.1.0
- [ ] Gene Set Enrichment Analysis (GSEA) integration
- [ ] Pathway enrichment visualization
- [ ] Heatmap for top differentially expressed genes
- [ ] PDF report generation

### Planned for 2.2.0
- [ ] Batch comparison mode (multiple datasets)
- [ ] Database integration (NCBI, Ensembl)
- [ ] Advanced clustering visualizations
- [ ] Custom color scheme selection

### Planned for 3.0.0
- [ ] Machine learning-based gene prioritization
- [ ] Network analysis visualization
- [ ] Docker containerization
- [ ] REST API for programmatic access

---

## Support

For questions or issues with specific versions:
- Open an [issue](https://github.com/yourusername/Differential-Gene-Expression/issues)
- Check the [documentation](docs/)
- Join [discussions](https://github.com/yourusername/Differential-Gene-Expression/discussions)


