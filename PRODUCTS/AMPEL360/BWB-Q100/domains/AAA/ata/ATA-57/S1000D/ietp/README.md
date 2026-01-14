# Interactive Electronic Technical Publication (IETP) for ATA-57

This directory contains the IETP static site generator for ATA-57 Wings (BWB-H₂ Q100).

## Overview

The IETP system generates a modern, interactive web interface for browsing S1000D data modules organized by:
- **Subsystems**: 57-10 through 57-50 (Wing Structure, Fuel Interfaces, Control Surfaces, High-Lift, Equipment Integration)
- **Information Code Categories**: Description, Tests, Procedures, Fault Isolation, IPD/Parts
- **Multimedia Content**: Embedded video, audio, images, and interactive diagrams

## Files

- `build_ietp.py` - Static site generator (Python 3.9+, stdlib only)
- `assets/css/ietp.css` - Dark theme styling
- `assets/css/media-embed.css` - Multimedia component styling
- `assets/js/ietp.js` - Client-side filtering and search
- `assets/js/media-embed.js` - Multimedia embedding component
- `site/` - Generated static HTML (created after build)

## Building the IETP

From the S1000D root directory:

```bash
cd ietp
python3 build_ietp.py
```

Output will be generated in `ietp/site/`:
- `index.html` - Main landing page with subsystem cards
- `subsystem/57-{nn}.html` - Pages for each subsystem
- `dm/DMC-*.html` - Individual data module pages
- `site_index.json` - Search index for client-side search
- `multimedia-demo.html` - Interactive demo of multimedia features

## Features

### Organization
- **Index page**: Cards for each ATA-57 subsystem
- **Subsystem pages**: Organized by information code buckets
- **Data module pages**: Renders actual DM content when available

### Interactive Features
- **Category filtering**: Click chips to filter by information code type
- **Quick search**: Search titles and DM keys
- **Responsive design**: Works on desktop and mobile
- **Status indicators**: Shows authored vs pending modules
- **Multimedia embedding**: Video, audio, images with interactive controls
- **Image zoom**: Click to view full-screen images
- **Video controls**: Custom play overlays and responsive playback

### Multimedia Features (NEW)
- **Video embedding**: Responsive video playback with custom controls
- **Audio playback**: Clean audio player with full controls
- **Interactive images**: Click-to-zoom functionality for technical diagrams
- **S1000D integration**: Automatic processing of multimedia object references
- **Responsive containers**: Maintains aspect ratios across all devices
- **Accessibility**: Keyboard navigation, ARIA labels, reduced motion support

### Information Code Mapping

| Category | Info Codes | Description |
|----------|------------|-------------|
| Description | 040, 042, 034, 050-056 | Technical data, function descriptions |
| Tests | 310, 345, 350 | Inspections, operational checks |
| Removal | 500-599 | Removal procedures |
| Install | 700-799 | Installation and rigging |
| Servicing | 600-699 | Servicing procedures |
| FI-General | 420 | General fault isolation |
| FI-Specific | 421-428 | Specific fault isolation |
| IPD | 900, 910 | Illustrated parts data |

## Data Sources

The generator reads from:
- `publication_modules/DML-BWQ1-ATA57-00_EN-US.xml` - Data Module Requirements List
- `indices/dm_index.xml` - Index of actual DM files and paths
- `data_modules/` - Actual S1000D XML files for content rendering

## Content Rendering

- **Authored modules**: Extracts and renders title, description paragraphs, and lists
- **Pending modules**: Shows placeholder indicating content will appear when XML is authored
- **Missing modules**: Clearly marked with "pending" status

## CI Integration

Add to your workflow after indices are generated:

```yaml
- name: Build IETP (static)
  working-directory: PRODUCTS/AMPEL360/BWB-Q100/domains/AAA/ata/ATA-57/S1000D/ietp
  run: python3 build_ietp.py
- name: Upload IETP artifact
  uses: actions/upload-artifact@v4
  with:
    name: IETP-ATA57
    path: PRODUCTS/AMPEL360/BWB-Q100/domains/AAA/ata/ATA-57/S1000D/ietp/site
```

## Technical Details

- **No dependencies**: Uses only Python standard library (with optional defusedxml)
- **Static output**: Pure HTML/CSS/JS, can be served from any web server
- **Dark theme**: Professional appearance matching technical documentation standards
- **Progressive enhancement**: Works without JavaScript, enhanced with JS features

---

**Classification**: INTERNAL–EVIDENCE-REQUIRED  
**S1000D Version**: 6.0  
**Last Updated**: 2025-01-21