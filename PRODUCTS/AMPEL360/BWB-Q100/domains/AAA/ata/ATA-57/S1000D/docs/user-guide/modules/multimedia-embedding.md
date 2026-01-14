# IETP Multimedia Embedding Features

This document demonstrates the new multimedia embedding features added to the IETP (Interactive Electronic Technical Publication) system.

## Overview

The IETP now supports rich multimedia content embedding with:

- **Video embedding** with custom controls and autoplay options
- **Audio playback** with responsive controls
- **Interactive images** with zoom capabilities
- **Responsive design** that adapts to all screen sizes
- **S1000D multimedia object** reference support

## Features

### 1. MediaEmbed Component

A JavaScript component (`media-embed.js`) that automatically detects and enhances multimedia content:

- **Automatic initialization** - Scans content and applies enhancements
- **Responsive containers** - Maintains aspect ratios across devices
- **Custom controls** - Play buttons and overlays for better UX
- **Image zoom** - Click images to view full-screen
- **S1000D integration** - Processes multimedia object references

### 2. Video Embedding

Videos can be embedded with:

```html
<video controls>
  <source src="../../multimedia/videos/example.mp4" type="video/mp4">
</video>
```

Or using S1000D multimedia references:

```html
<div data-s1000d-multimedia="video" 
     data-multimedia-path="../../multimedia/videos/example.mp4"
     data-multimedia-code="ICN-BWQ1-A-571010-V-001-01">
</div>
```

**Features:**
- Responsive 16:9 aspect ratio by default
- Custom play button overlay
- Full browser controls support
- Autoplay control (disabled by default for accessibility)
- Loop support
- Mute options

### 3. Audio Embedding

Audio files can be embedded with:

```html
<audio controls>
  <source src="../../multimedia/videos/example.mp3" type="audio/mpeg">
</audio>
```

Or using S1000D references:

```html
<div data-s1000d-multimedia="audio" 
     data-multimedia-path="../../multimedia/videos/example.mp3"
     data-multimedia-code="ICN-BWQ1-A-571010-A-001-01">
</div>
```

**Features:**
- Clean audio player interface
- Volume controls
- Progress bar
- Playback speed control (browser-dependent)

### 4. Interactive Images

Images can be made interactive with zoom capabilities:

```html
<img src="../../multimedia/photos/example.png" 
     alt="Technical diagram" 
     data-interactive="zoom">
```

**Features:**
- Click to zoom full-screen
- Modal overlay with backdrop
- ESC key to close
- Close button in corner
- Maintains image aspect ratio

### 5. Multimedia Captions

Add captions to any multimedia element:

```html
<div class="media-embed-container">
  <video controls>...</video>
  <div class="media-caption">
    <div class="caption-title">Wing Box Assembly Process</div>
    <div class="caption-code">Multimedia Code: ICN-BWQ1-A-571010-V-001-01</div>
  </div>
</div>
```

### 6. Multimedia Grid Layout

Display multiple media items in a responsive grid:

```html
<div class="media-grid">
  <div class="media-grid-item">
    <img src="photo1.png" alt="Photo 1">
  </div>
  <div class="media-grid-item">
    <img src="photo2.png" alt="Photo 2">
  </div>
  <div class="media-grid-item">
    <img src="photo3.png" alt="Photo 3">
  </div>
</div>
```

## Configuration Options

The MediaEmbed component can be configured when manually initialized:

```javascript
new MediaEmbed(document.querySelector('.content'), {
  autoplay: false,        // Auto-start videos (default: false)
  controls: true,         // Show media controls (default: true)
  loop: false,            // Loop playback (default: false)
  muted: false,           // Mute audio/video (default: false)
  responsive: true,       // Enable responsive behavior (default: true)
  aspectRatio: '16:9',    // Video aspect ratio (default: '16:9')
  maxWidth: '100%'        // Maximum width for media (default: '100%')
});
```

## S1000D Integration

The system automatically processes S1000D multimedia object references in data modules:

### XML Structure

```xml
<multimedia>
  <multimediaObject multimediaCode="ICN-BWQ1-A-571010-V-001-01" 
                    multimediaType="video"/>
  <multimediaCaption>Wing box assembly demonstration video</multimediaCaption>
</multimedia>
```

### Generated HTML

The build system (`build_ietp.py`) automatically converts these to:

```html
<div class="media-embed-container">
  <div data-s1000d-multimedia="video" 
       data-multimedia-path="../../multimedia/videos/ICN-BWQ1-A-571010-V-001-01.mp4"
       data-multimedia-code="ICN-BWQ1-A-571010-V-001-01">
    <video controls>
      <source src="../../multimedia/videos/ICN-BWQ1-A-571010-V-001-01.mp4" type="video/mp4">
    </video>
  </div>
  <div class="media-caption">
    <div class="caption-title">Wing box assembly demonstration video</div>
    <div class="caption-code">Multimedia Code: ICN-BWQ1-A-571010-V-001-01</div>
  </div>
</div>
```

## Responsive Design

All multimedia elements automatically adapt to screen size:

- **Desktop (>1024px)**: Maximum 900px width, full features
- **Tablet (769-1024px)**: Flexible width, optimized controls
- **Mobile (<768px)**: Full width, compact controls, touch-friendly

## Accessibility

The multimedia system includes accessibility features:

- **Keyboard navigation** - All controls accessible via keyboard
- **Focus indicators** - Clear focus states for keyboard users
- **ARIA labels** - Proper labels for screen readers
- **Reduced motion** - Respects `prefers-reduced-motion` setting
- **High contrast** - Supports high contrast mode
- **No autoplay** - Videos don't auto-start (default) for better UX

## Browser Support

The MediaEmbed component works with:

- Modern browsers supporting HTML5 video/audio
- Chrome, Firefox, Safari, Edge (latest versions)
- Mobile browsers (iOS Safari, Chrome Mobile)
- Progressive enhancement for older browsers

## File Format Support

### Video Formats
- MP4 (H.264) - Primary format, best compatibility
- WebM (VP8/VP9) - Alternative format
- MOV - Supported on many browsers

### Audio Formats
- MP3 - Primary format, universal support
- AAC - High quality alternative
- WAV - Lossless audio
- OGG Vorbis - Open format

### Image Formats
- PNG - Technical diagrams, screenshots
- JPEG - Photographs
- SVG - Vector graphics, scalable diagrams
- GIF - Simple animations

## Usage in Data Modules

To include multimedia in your S1000D data modules:

1. **Place multimedia files** in appropriate directories:
   - Videos: `multimedia/videos/`
   - Audio: `multimedia/videos/` (or separate audio directory)
   - Images: `multimedia/photos/` or `multimedia/graphics/`

2. **Reference in XML** using standard S1000D multimedia object elements

3. **Build IETP** - Run `python3 build_ietp.py` to generate HTML

4. **View in browser** - Open generated HTML to see embedded multimedia

## Example: Complete Data Module with Multimedia

```xml
<dmodule>
  <identAndStatusSection>
    <!-- ... metadata ... -->
  </identAndStatusSection>
  <content>
    <description>
      <levelledPara>
        <title>Wing Box Assembly Procedure</title>
        <para>Follow the steps shown in the video below:</para>
        <multimedia>
          <multimediaObject multimediaCode="ICN-BWQ1-A-571010-V-001-01" 
                            multimediaType="video"/>
          <multimediaCaption>Complete wing box assembly demonstration</multimediaCaption>
        </multimedia>
        <para>Key structural components are shown in this diagram:</para>
        <multimedia>
          <multimediaObject multimediaCode="ICN-BWQ1-A-571010-G-001-01" 
                            multimediaType="graphic"/>
          <multimediaCaption>Wing box structural components exploded view</multimediaCaption>
        </multimedia>
      </levelledPara>
    </description>
  </content>
</dmodule>
```

## Performance Considerations

- **Lazy loading** - Videos only load when in viewport (browser default)
- **Responsive images** - Serve appropriately sized images
- **Video compression** - Use H.264 with appropriate bitrate
- **CDN hosting** - Consider CDN for multimedia assets in production

## Future Enhancements

Potential future improvements:

- Multiple video quality options (480p, 720p, 1080p)
- Video chapters and markers
- Interactive hotspots on images
- 360° image viewers
- WebVR/AR content integration
- Real-time video streaming support
- Transcript overlay for videos

## Testing the Features

To test the multimedia embedding:

1. Build the IETP site: `cd ietp && python3 build_ietp.py`
2. Serve locally: `cd site && python3 -m http.server 8080`
3. Open browser: `http://localhost:8080`
4. Navigate to any data module page
5. Add test multimedia files to the multimedia directories
6. Rebuild and refresh to see embedded content

---

**Classification**: INTERNAL–EVIDENCE-REQUIRED  
**Last Updated**: 2026-01-14  
**Version**: 1.0
