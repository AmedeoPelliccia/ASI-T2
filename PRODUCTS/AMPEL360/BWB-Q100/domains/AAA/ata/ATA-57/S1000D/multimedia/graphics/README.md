# Graphics - Technical Diagrams and Illustrations

This directory contains technical graphics and diagrams for ATA-57 Wings documentation.

## Content Types

- **System Diagrams** - Wing system schematics and layouts
- **Exploded Views** - Component assembly illustrations
- **Cutaway Drawings** - Internal structure views
- **Flow Diagrams** - Process and system flows
- **Technical Illustrations** - S1000D compliant graphics

## File Formats

- **SVG** - Preferred format for scalable vector graphics
- **PNG** - High-resolution raster images (300 DPI minimum)
- **CGM** - Computer Graphics Metafile (S1000D standard)

## Naming Convention

Graphics follow S1000D multimedia naming:
```
ICN-[MIC]-[SDC]-[SC][SSC][SSSC]-[TYPE]-[SEQ]-[VAR].[ext]
```

Example: `ICN-BWQ1-A-571010-G-001-01.svg`

Where:
- **ICN** = Information Control Number (multimedia prefix)
- **BWQ1** = Model Identification Code
- **A** = System Difference Code
- **571010** = Wing Structure subsystem
- **G** = Graphic type
- **001** = Sequence number
- **01** = Variant

## Usage in Data Modules

Reference graphics in S1000D XML:

```xml
<multimedia>
  <multimediaObject multimediaCode="ICN-BWQ1-A-571010-G-001-01" 
                    multimediaType="graphic"/>
  <multimediaCaption>Wing box structural components</multimediaCaption>
</multimedia>
```

## IETP Integration

Graphics are automatically embedded in the IETP with:
- **Click-to-zoom** functionality
- **Responsive sizing** for all devices
- **Interactive hotspots** (when configured)
- **Caption display** from S1000D metadata

---

**Classification**: INTERNAL–EVIDENCE-REQUIRED
