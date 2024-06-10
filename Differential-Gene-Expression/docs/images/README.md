# Dashboard Screenshots

This directory contains screenshots and images for documentation.

## Required Screenshots

To complete the documentation, please add the following screenshots:

### 1. `dashboard-preview.png`
**Description**: Main dashboard overview showing the full interface
**Recommended size**: 1920x1080px
**Content**: 
- File upload section
- Column mapping interface
- Volcano plot
- Statistics metrics

### 2. `volcano-plot.png`
**Description**: Interactive volcano plot example
**Recommended size**: 1200x800px
**Content**:
- Clearly visible up/down regulated genes
- Color-coded points (red/green/gray)
- Axis labels visible
- Hover tooltip shown

### 3. `ma-plot.png`
**Description**: MA plot visualization
**Recommended size**: 1200x800px
**Content**:
- Expression vs fold change relationship
- Significant genes highlighted
- Reference line at y=0

### 4. `top-genes.png`
**Description**: Top genes bar chart
**Recommended size**: 1000x800px
**Content**:
- Horizontal bar chart of top 20 genes
- Color gradient visible
- Gene names clearly readable

### 5. `distribution.png` (Optional)
**Description**: Distribution plots side-by-side
**Recommended size**: 1400x600px

### 6. `export-options.png` (Optional)
**Description**: Export functionality demonstration
**Recommended size**: 800x400px

---

## How to Capture Screenshots

### Method 1: Using the Dashboard

1. Launch dashboard: `streamlit run app/dashboard.py`
2. Upload `examples/sample_data.csv`
3. Navigate through tabs
4. Use screenshot tool:
   - **Windows**: Win + Shift + S
   - **macOS**: Cmd + Shift + 4
   - **Linux**: Shift + PrtScn

### Method 2: Programmatic (Plotly)

```python
import plotly.io as pio

# After creating a figure
fig = create_volcano_plot_plotly(df)

# Save as high-quality PNG
pio.write_image(fig, "docs/images/volcano-plot.png", 
                width=1200, height=800, scale=2)
```

### Method 3: Browser DevTools

1. Open dashboard in Chrome/Firefox
2. Press F12 for DevTools
3. Click device toolbar icon
4. Set resolution (e.g., 1920x1080)
5. Take screenshot

---

## Image Guidelines

### Format
- **Preferred**: PNG (lossless, good for UI)
- **Alternative**: JPG (smaller size, lossy)
- **Avoid**: BMP, TIFF (too large)

### Size
- **Maximum width**: 1920px
- **Maximum file size**: 2MB per image
- **Minimum DPI**: 72 (web) or 150 (print)

### Quality
- Clear, readable text
- No compression artifacts
- Proper aspect ratio
- Representative data

### Content
- Use sample_data.csv for consistency
- Include UI elements (buttons, labels)
- Show interactive features (tooltips)
- Annotate if necessary

---

## Placeholders

Until screenshots are added, the following placeholders are used:

```markdown
![Dashboard Preview](docs/images/dashboard-preview.png)
```

Replace these with actual screenshots after generating them.

---

## Image Optimization

After capturing, optimize images:

```bash
# Using ImageMagick
convert input.png -resize 1200x800 -quality 85 output.png

# Using Python (PIL)
from PIL import Image
img = Image.open('input.png')
img = img.resize((1200, 800), Image.LANCZOS)
img.save('output.png', optimize=True, quality=85)
```

---

## Contributing Screenshots

When adding screenshots:

1. Follow naming convention (lowercase, hyphens)
2. Add to this README with description
3. Reference in main documentation
4. Ensure no sensitive data visible
5. Update relevant .md files

---

**Note**: Screenshots should be updated with each major UI change.


