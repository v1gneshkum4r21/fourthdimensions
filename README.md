# FourthDimensions - Hero Section Landing Page

A modern, responsive hero section for FourthDimensions company featuring a clean design with professional styling.

## Features

- **Modern Design**: Clean, professional layout with a calming light grey background
- **Responsive**: Fully responsive design that works on all device sizes
- **Interactive Elements**: 
  - Clickable category tabs (Interior, Construction, Property Consultancy)
  - Animated play button for company video
  - Modal popup for video content
- **Smooth Animations**: Elegant entrance animations and hover effects
- **Professional Color Scheme**: Brown and gold branding as requested

## Design Elements

### Logo
- "Fourth" in brown (#8B4513)
- "Dimensions" in gold gradient (#FFD700 to #FFA500)
- Large, prominent typography with modern font (Inter)

### Category Tabs
- Three main service categories with icons
- Hover effects and active states
- Glassmorphism design with backdrop blur

### Play Button
- Large, centered circular button
- Gold gradient background
- Pulsing glow animation
- Opens video modal on click

### Color Palette
- **Background**: Light grey gradient (#f8f9fa to #e9ecef)
- **Primary Gold**: #FFD700
- **Secondary Gold**: #FFA500
- **Brown**: #8B4513
- **Text**: #333 (dark grey)

## File Structure

```
fourth-dimensions/
├── index.html          # Main HTML file
├── styles.css          # CSS styles and animations
├── script.js           # JavaScript functionality
└── README.md           # This file
```

## Getting Started

1. **Open the project**: Simply open `index.html` in your web browser
2. **No build process required**: This is a static HTML/CSS/JS project
3. **Live server recommended**: For development, use a local server like Live Server in VS Code

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers

## Customization

### Colors
You can easily customize the color scheme by modifying the CSS variables in `styles.css`:

```css
/* Main brand colors */
--primary-gold: #FFD700;
--secondary-gold: #FFA500;
--brand-brown: #8B4513;
--background-light: #f8f9fa;
--background-dark: #e9ecef;
```

### Content
- Update the logo text in `index.html`
- Modify category names and icons
- Replace the video placeholder with actual video content
- Add more sections below the hero

### Animations
All animations are defined in the CSS file and can be easily modified or disabled.

## Features in Detail

### Tab Functionality
- Click any category tab to activate it
- Smooth transitions between states
- Console logging for category changes (can be extended for content switching)

### Video Modal
- Opens when play button is clicked
- Can be closed by:
  - Clicking the X button
  - Clicking outside the modal
  - Pressing the Escape key
- Prevents background scrolling when open

### Responsive Design
- Mobile-first approach
- Breakpoints at 768px and 480px
- Optimized for all screen sizes

## Performance

- Lightweight (no heavy frameworks)
- Fast loading times
- Optimized animations
- Minimal JavaScript footprint

## Future Enhancements

- Add actual video content
- Implement content switching based on selected tabs
- Add more sections (About, Services, Contact)
- Integrate with a backend for dynamic content
- Add form functionality for contact/inquiry

## License

This project is open source and available under the MIT License. 