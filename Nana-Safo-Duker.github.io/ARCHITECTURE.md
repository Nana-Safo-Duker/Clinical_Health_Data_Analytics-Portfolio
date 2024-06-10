# Architecture Documentation

## Overview

This portfolio website is built with a modern, lightweight architecture focused on performance, accessibility, and maintainability.

## File Structure

```
Nana-Safo-Duker.github.io/
│
├── index.html              # Main entry point
├── W_P.html               # Original file (backup/legacy)
├── W_P.css                # Original stylesheet (backup/legacy)
├── README.md              # Project documentation
├── ARCHITECTURE.md        # This file - technical documentation
├── .gitignore             # Git ignore rules
├── .gitattributes         # Git LFS and line ending rules
│
├── css/
│   └── styles.css         # Main stylesheet with theme system
│
├── js/                    # JavaScript files (future)
│
├── assets/
│   ├── images/            # Image assets
│   └── icons/             # Icon files, favicons
│
├── docs/                  # Additional documentation
├── projects/              # Project-specific resources
├── research/              # Research materials
└── publications/          # Publication files

```

## Technology Stack

### Core
- **HTML5**: Semantic markup for accessibility and SEO
- **CSS3**: Modern styling with CSS custom properties
- **JavaScript (Vanilla)**: No frameworks for optimal performance

### Libraries & CDNs
- **Font Awesome 6.4.0**: Icons
- **Google Fonts**: Inter (sans-serif) & Playfair Display (serif)
- **GitHub Pages**: Hosting

## Design System

### Color Palette

#### Dark Theme (Default)
```css
--bg-dark: #0d1117          /* GitHub-style background */
--text-dark: #e6edf3         /* Light text */
--primary-dark: #58a6ff      /* Blue accent */
--accent-dark: #0070f3       /* Strong blue */
--card-bg-dark: #161b22      /* Card background */
--border-dark: #30363d       /* Borders */
```

#### Light Theme
```css
--bg-light: #ffffff          /* White background */
--text-light: #1a1a1a        /* Dark text */
--primary-light: #1b3c59     /* Dark blue */
--accent-light: #0077ff      /* Bright blue */
--card-bg-light: #f8f9fa     /* Light card background */
--border-light: #e0e0e0      /* Light borders */
```

### Typography
- **Headers**: Playfair Display (serif, bold)
- **Body**: Inter (sans-serif, regular, semi-bold)
- **Responsive**: Fluid typography using rem units

### Spacing
- Base unit: `1rem` (16px)
- Consistent spacing scale: 0.5rem, 1rem, 1.5rem, 2rem, 3rem, 4rem

## Component Architecture

### Header/Hero
- Full-width gradient background
- Animated grid pattern overlay
- Centered content with social links
- Theme toggle button (fixed position)

### Navigation
- Icon + text links
- Glassmorphism styling
- Hover animations
- Responsive layout

### Sections
- About, Projects, Publications
- Consistent card-based layout
- Fade-in animations with delay
- Hover effects

### Cards/Articles
- Elevated shadow on hover
- Left border accent on hover
- Smooth transitions
- Responsive padding

### Buttons
- Gradient backgrounds
- Ripple effect on hover
- Arrow indicator
- Accessible focus states

### Footer
- Simple, centered layout
- Theme-appropriate styling
- Copyright and attribution

## Theme System

### Implementation
- CSS custom properties for theming
- JavaScript localStorage for persistence
- Smooth transitions between themes
- Toggle button with icon states

### Theme Toggle Logic
```javascript
1. User clicks toggle button
2. Toggle 'dark-theme' class on body
3. Update icon (sun/moon)
4. Save preference to localStorage
5. Smooth CSS transitions handle visual change
```

## Responsive Design

### Breakpoints
- **Desktop**: 1100px (max-width for content)
- **Tablet**: 768px (navigation adjustments)
- **Mobile**: 480px (stacked layout)

### Mobile Optimizations
- Larger tap targets
- Simplified navigation
- Reduced font sizes
- Optimized spacing
- Touch-friendly buttons

## Performance Optimizations

### Loading
- Minimal CSS (no frameworks)
- Vanilla JavaScript (no dependencies)
- CDN resources for fonts/icons
- No blocking resources

### Rendering
- CSS Grid/Flexbox (hardware accelerated)
- GPU-accelerated transforms
- Efficient animations
- Optimized reflows

### Best Practices
- Semantic HTML
- Proper meta tags
- Lazy loading ready
- Minimal DOM manipulation

## Accessibility Features

### WCAG 2.1 Compliance
- **Level AA** target
- Keyboard navigation support
- Screen reader optimization
- Focus indicators
- Color contrast (4.5:1 minimum)

### ARIA Labels
- Button labels
- Link descriptions
- Semantic roles

### Responsive Design
- Text scaling support
- Touch target sizes (44x44px minimum)
- Reduced motion support

## Browser Support

### Modern Browsers
- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions

### Graceful Degradation
- CSS Grid fallback
- CSS custom properties fallback
- JavaScript feature detection

### Polyfills
- None required (targets modern browsers)

## SEO Optimization

### Meta Tags
- Title, description, keywords
- Open Graph (social sharing)
- Twitter Card
- Author information

### Semantic HTML
- Proper heading hierarchy
- Article tags for content
- Nav, header, footer elements
- Alt text ready for images

### Performance Metrics
- Target Lighthouse score: 90+
- Fast Time to First Byte (TTFB)
- Minimal Cumulative Layout Shift (CLS)
- Optimized Largest Contentful Paint (LCP)

## Future Enhancements

### Planned Features
1. **Project Gallery**: Dynamic image gallery
2. **Contact Form**: Functional contact section
3. **Blog Integration**: Medium API integration
4. **PDF Viewer**: Publication viewer
5. **Search**: Content search functionality
6. **Analytics**: Visitor tracking
7. **PWA**: Progressive Web App capabilities

### Technical Improvements
- Service Worker for offline support
- RSS feed generation
- Sitemap.xml
- Robots.txt optimization
- Dark mode media query detection
- Internationalization (i18n)

## Deployment

### GitHub Pages
- Automatic deployment on push
- Custom domain ready
- HTTPS enabled
- Jekyll disabled (static HTML)

### CI/CD (Future)
- Lighthouse CI
- Automated testing
- Pre-commit hooks
- Deployment automation

## Maintenance

### Regular Updates
- Dependencies (CDN resources)
- Content (projects, publications)
- Security patches
- Performance monitoring

### Content Management
- Static HTML (easy to edit)
- No CMS dependencies
- Version controlled
- Markdown ready

## Development Workflow

### Setup
1. Clone repository
2. Open `index.html` in browser
3. Or use local server (recommended)

### Local Server
```bash
# Python
python -m http.server 8000

# Node.js
npx serve

# PHP
php -S localhost:8000
```

### Testing
- Manual browser testing
- Mobile device testing
- Accessibility audit
- Performance audit

### Deployment
1. Commit changes
2. Push to main branch
3. GitHub Pages auto-deploy
4. Verify live site

## Security Considerations

### Content Security
- Static site (no server-side vulnerabilities)
- HTTPS enforced (GitHub Pages)
- No user input processing
- External link security (rel="noopener")

### Privacy
- No tracking by default
- No cookies (except localStorage for theme)
- GDPR compliant
- Privacy-friendly

## License

This project is open source under the MIT License.

## Author

**Nana Safo Duker**
- GitHub: [@Nana-Safo-Duker](https://github.com/Nana-Safo-Duker)
- LinkedIn: [Profile](https://www.linkedin.com/in/nana-safo-duker-0aa25227a/)
- Medium: [@freshsafoduker300](https://medium.com/@freshsafoduker300)

---

*Last Updated: 2025*
