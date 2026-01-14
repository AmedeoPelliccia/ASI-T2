# Videos - Procedure and Training Content

This directory contains video content for ATA-57 Wings documentation.

## Content Types

- **Procedure Videos** - Step-by-step maintenance procedures
- **Training Videos** - Technical training materials
- **Inspection Videos** - Visual inspection techniques
- **Safety Videos** - Safety procedure demonstrations
- **Assembly Videos** - Component assembly sequences

## File Formats

- **MP4 (H.264)** - Primary format, best browser compatibility
- **WebM (VP9)** - Alternative format for modern browsers
- **MOV** - Supported format (convert to MP4 for web use)

## Quality Standards

- **Resolution**: 1080p (1920x1080) or 720p (1280x720) minimum
- **Frame Rate**: 30 fps or 60 fps
- **Bitrate**: 5-8 Mbps for 1080p, 2-4 Mbps for 720p
- **Audio**: AAC codec, 128-192 kbps stereo
- **Duration**: Keep under 10 minutes per segment

## Naming Convention

Videos follow S1000D multimedia naming:
```
ICN-[MIC]-[SDC]-[SC][SSC][SSSC]-[TYPE]-[SEQ]-[VAR].[ext]
```

Example: `ICN-BWQ1-A-571010-V-001-01.mp4`

Where:
- **ICN** = Information Control Number (multimedia prefix)
- **BWQ1** = Model Identification Code
- **A** = System Difference Code
- **571010** = Wing Structure subsystem
- **V** = Video type
- **001** = Sequence number
- **01** = Variant

## Usage in Data Modules

Reference videos in S1000D XML:

```xml
<multimedia>
  <multimediaObject multimediaCode="ICN-BWQ1-A-571010-V-001-01" 
                    multimediaType="video"/>
  <multimediaCaption>Wing box assembly demonstration</multimediaCaption>
</multimedia>
```

## IETP Integration

Videos are automatically embedded in the IETP with:
- **Responsive 16:9 aspect ratio**
- **Custom play button overlay**
- **Full browser controls** (play, pause, volume, fullscreen)
- **No autoplay** (accessible by default)
- **Caption support** from S1000D metadata

## Production Guidelines

1. **Filming**
   - Use stable tripod or gimbal
   - Ensure proper lighting
   - Record clean audio (minimize background noise)
   - Frame subject clearly in center

2. **Editing**
   - Add title cards at beginning
   - Include step numbers for procedures
   - Add text overlays for key information
   - Include safety warnings prominently

3. **Export Settings**
   - Format: MP4 (H.264)
   - Resolution: 1920x1080 @ 30fps
   - Bitrate: 5000 kbps (variable)
   - Audio: AAC 192 kbps stereo

4. **Quality Check**
   - Preview on multiple devices
   - Verify audio clarity
   - Check for proper color balance
   - Ensure readability of text overlays

---

**Classification**: INTERNAL–EVIDENCE-REQUIRED
