/**
 * MediaEmbed Component for IETP
 * Handles embedding and rendering of multimedia content (audio, video, images, diagrams)
 * with support for S1000D multimedia object references
 */
(function() {
  'use strict';

  /**
   * MediaEmbed class - Main component for multimedia embedding
   */
  class MediaEmbed {
    constructor(container, options = {}) {
      this.container = container;
      this.options = {
        autoplay: options.autoplay || false,
        controls: options.controls !== false, // default true
        loop: options.loop || false,
        muted: options.muted || false,
        responsive: options.responsive !== false, // default true
        maxWidth: options.maxWidth || '100%',
        aspectRatio: options.aspectRatio || '16:9',
        ...options
      };
      this.init();
    }

    init() {
      // Initialize multimedia elements in container
      this.processMultimediaElements();
      
      // Set up responsive behavior if enabled
      if (this.options.responsive) {
        this.setupResponsive();
      }

      // Process S1000D multimedia object references
      this.processS1000DMultimedia();
    }

    /**
     * Process existing multimedia elements and enhance them
     */
    processMultimediaElements() {
      // Process video elements
      const videos = this.container.querySelectorAll('video:not([data-media-embed])');
      videos.forEach(video => this.enhanceVideo(video));

      // Process audio elements
      const audios = this.container.querySelectorAll('audio:not([data-media-embed])');
      audios.forEach(audio => this.enhanceAudio(audio));

      // Process image elements that should be interactive
      const images = this.container.querySelectorAll('img[data-interactive]:not([data-media-embed])');
      images.forEach(img => this.enhanceImage(img));
    }

    /**
     * Process S1000D multimedia object references
     * Looks for elements with data-s1000d-multimedia attribute
     */
    processS1000DMultimedia() {
      const mmRefs = this.container.querySelectorAll('[data-s1000d-multimedia]');
      mmRefs.forEach(ref => {
        const mmType = ref.dataset.s1000dMultimedia;
        const mmPath = ref.dataset.multimediaPath;
        const mmCode = ref.dataset.multimediaCode;

        if (!mmPath) return;

        switch (mmType) {
          case 'video':
            this.embedVideo(ref, mmPath, mmCode);
            break;
          case 'audio':
            this.embedAudio(ref, mmPath, mmCode);
            break;
          case 'graphic':
          case 'image':
            this.embedImage(ref, mmPath, mmCode);
            break;
          case 'animation':
            this.embedAnimation(ref, mmPath, mmCode);
            break;
          default:
            console.warn(`Unknown multimedia type: ${mmType}`);
        }
      });
    }

    /**
     * Enhance video element with controls and responsive behavior
     */
    enhanceVideo(video) {
      video.setAttribute('data-media-embed', 'true');
      video.controls = this.options.controls;
      video.autoplay = this.options.autoplay;
      video.loop = this.options.loop;
      video.muted = this.options.muted;

      // Wrap in responsive container
      if (this.options.responsive && !video.parentElement.classList.contains('media-embed-container')) {
        this.wrapInResponsiveContainer(video, 'video');
      }

      // Add play/pause overlay
      if (this.options.controls) {
        this.addPlayOverlay(video);
      }
    }

    /**
     * Enhance audio element
     */
    enhanceAudio(audio) {
      audio.setAttribute('data-media-embed', 'true');
      audio.controls = this.options.controls;
      audio.autoplay = this.options.autoplay;
      audio.loop = this.options.loop;

      // Wrap in container with custom styling
      if (!audio.parentElement.classList.contains('media-embed-container')) {
        this.wrapInResponsiveContainer(audio, 'audio');
      }
    }

    /**
     * Enhance image with interactive features
     */
    enhanceImage(img) {
      img.setAttribute('data-media-embed', 'true');
      
      // Add click to zoom functionality
      if (img.dataset.interactive === 'zoom') {
        this.addZoomFeature(img);
      }

      // Wrap in responsive container
      if (this.options.responsive && !img.parentElement.classList.contains('media-embed-container')) {
        this.wrapInResponsiveContainer(img, 'image');
      }
    }

    /**
     * Embed video from S1000D reference
     */
    embedVideo(container, path, code) {
      const video = document.createElement('video');
      video.src = path;
      video.controls = this.options.controls;
      video.autoplay = this.options.autoplay;
      video.loop = this.options.loop;
      video.muted = this.options.muted;
      video.setAttribute('data-multimedia-code', code || '');
      
      // Clear container and add video
      container.innerHTML = '';
      container.appendChild(video);
      
      this.enhanceVideo(video);
    }

    /**
     * Embed audio from S1000D reference
     */
    embedAudio(container, path, code) {
      const audio = document.createElement('audio');
      audio.src = path;
      audio.controls = this.options.controls;
      audio.autoplay = this.options.autoplay;
      audio.loop = this.options.loop;
      audio.setAttribute('data-multimedia-code', code || '');
      
      container.innerHTML = '';
      container.appendChild(audio);
      
      this.enhanceAudio(audio);
    }

    /**
     * Embed image from S1000D reference
     */
    embedImage(container, path, code) {
      const img = document.createElement('img');
      img.src = path;
      img.alt = `Multimedia object ${code || ''}`;
      img.setAttribute('data-multimedia-code', code || '');
      
      container.innerHTML = '';
      container.appendChild(img);
      
      this.enhanceImage(img);
    }

    /**
     * Embed animation (video or GIF) from S1000D reference
     */
    embedAnimation(container, path, code) {
      // Determine if it's a video or image-based animation
      const ext = path.split('.').pop().toLowerCase();
      
      if (['mp4', 'webm', 'mov'].includes(ext)) {
        this.embedVideo(container, path, code);
      } else {
        this.embedImage(container, path, code);
      }
    }

    /**
     * Wrap element in responsive container
     */
    wrapInResponsiveContainer(element, type) {
      const wrapper = document.createElement('div');
      wrapper.className = `media-embed-container media-embed-${type}`;
      
      // Calculate aspect ratio padding
      if (type === 'video' || type === 'image') {
        const [width, height] = this.options.aspectRatio.split(':').map(Number);
        const paddingBottom = (height / width * 100).toFixed(2);
        wrapper.style.paddingBottom = `${paddingBottom}%`;
      }
      
      element.parentNode.insertBefore(wrapper, element);
      wrapper.appendChild(element);
    }

    /**
     * Add play overlay for video elements
     */
    addPlayOverlay(video) {
      if (video.parentElement.querySelector('.play-overlay')) return;

      const overlay = document.createElement('div');
      overlay.className = 'play-overlay';
      overlay.innerHTML = '<button class="play-button" aria-label="Play video">▶</button>';
      
      video.parentElement.appendChild(overlay);
      
      const playButton = overlay.querySelector('.play-button');
      playButton.addEventListener('click', () => {
        video.play();
        overlay.style.display = 'none';
      });

      video.addEventListener('play', () => {
        overlay.style.display = 'none';
      });

      video.addEventListener('pause', () => {
        if (!video.ended) {
          overlay.style.display = 'flex';
        }
      });

      video.addEventListener('ended', () => {
        overlay.style.display = 'flex';
      });
    }

    /**
     * Add zoom functionality to images
     */
    addZoomFeature(img) {
      img.style.cursor = 'zoom-in';
      
      img.addEventListener('click', (e) => {
        e.preventDefault();
        this.showImageModal(img);
      });
    }

    /**
     * Show image in modal for zoomed view
     */
    showImageModal(img) {
      // Create modal
      const modal = document.createElement('div');
      modal.className = 'media-embed-modal';
      modal.innerHTML = `
        <div class="modal-backdrop"></div>
        <div class="modal-content">
          <button class="modal-close" aria-label="Close">&times;</button>
          <img src="${img.src}" alt="${img.alt}">
        </div>
      `;
      
      document.body.appendChild(modal);
      document.body.style.overflow = 'hidden';
      
      // Close handlers
      const close = () => {
        document.body.removeChild(modal);
        document.body.style.overflow = '';
      };
      
      modal.querySelector('.modal-close').addEventListener('click', close);
      modal.querySelector('.modal-backdrop').addEventListener('click', close);
      
      // ESC key to close
      const escHandler = (e) => {
        if (e.key === 'Escape') {
          close();
          document.removeEventListener('keydown', escHandler);
        }
      };
      document.addEventListener('keydown', escHandler);
    }

    /**
     * Setup responsive behavior with resize observer
     */
    setupResponsive() {
      if (typeof ResizeObserver === 'undefined') return;

      const observer = new ResizeObserver(entries => {
        entries.forEach(entry => {
          const width = entry.contentRect.width;
          const element = entry.target;
          
          // Adjust controls size based on container width
          if (width < 400) {
            element.classList.add('media-embed-small');
          } else {
            element.classList.remove('media-embed-small');
          }
        });
      });

      const mediaContainers = this.container.querySelectorAll('.media-embed-container');
      mediaContainers.forEach(container => observer.observe(container));
    }
  }

  /**
   * Auto-initialize on DOMContentLoaded
   */
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMediaEmbed);
  } else {
    initMediaEmbed();
  }

  function initMediaEmbed() {
    // Initialize for dm-article content
    const articles = document.querySelectorAll('.dm-article, .content');
    articles.forEach(article => {
      new MediaEmbed(article, {
        autoplay: false, // Default: no autoplay for accessibility
        controls: true,
        responsive: true,
        aspectRatio: '16:9'
      });
    });
  }

  // Export for manual initialization
  window.MediaEmbed = MediaEmbed;
})();
