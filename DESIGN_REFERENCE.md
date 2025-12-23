# TechElevate - New UI Design Quick Reference

## 🎨 Color Palette

### Primary Gradients
**Light Mode:**
- Start: `#667eea` (Vibrant Purple)
- 25%: `#764ba2` (Deep Purple)
- 50%: `#f093fb` (Bright Pink)
- 75%: `#4facfe` (Sky Blue)
- End: `#00f2fe` (Cyan)

**Dark Mode:**
- Start: `#1a1a2e` (Dark Navy)
- 25%: `#16213e` (Navy Blue)
- 50%: `#0f3460` (Deep Blue)
- 75%: `#533483` (Dark Purple)
- End: `#1a1a2e` (Dark Navy)

### Accent Colors
- **Buttons**: `linear-gradient(135deg, #ff6b6b, #ee5a6f)`
- **Dark Mode Buttons**: `linear-gradient(135deg, #667eea, #764ba2)`
- **Highlights**: `#ffeb3b` (Yellow)
- **Text**: `#fff` (White) / `#ddd` (Light Gray for dark mode)

## 🔮 Glassmorphism Recipe

### Standard Glass Container
```css
background: rgba(255, 255, 255, 0.15);
backdrop-filter: blur(20px);
border: 1px solid rgba(255, 255, 255, 0.3);
border-radius: 20px;
box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
```

### Glass Input Fields
```css
background: rgba(255, 255, 255, 0.2);
backdrop-filter: blur(10px);
border: 1px solid rgba(255, 255, 255, 0.3);
border-radius: 10px;
```

### Glass Navbar
```css
background: rgba(255, 255, 255, 0.1);
backdrop-filter: blur(20px);
border-bottom: 1px solid rgba(255, 255, 255, 0.2);
box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
```

## ✨ Animation Keyframes

### Gradient Shift
```css
@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
```

### Usage
```css
background-size: 400% 400%;
animation: gradientShift 15s ease infinite;
```

## 🎯 Interactive States

### Hover Effects
```css
/* Buttons */
button:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(238, 90, 111, 0.6);
}

/* Cards */
.card:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3);
}

/* Inputs */
input:focus {
  transform: translateY(-2px);
  background: rgba(255, 255, 255, 0.25);
  border-color: rgba(255, 255, 255, 0.5);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}
```

## 📐 Spacing & Sizing

### Border Radius
- **Large containers**: `20px`
- **Cards**: `15-20px`
- **Buttons**: `10px`
- **Inputs**: `10px`
- **Pills/Tags**: `30px`

### Padding
- **Containers**: `40px`
- **Cards**: `25-30px`
- **Buttons**: `12-14px`
- **Inputs**: `14px`

### Shadows
- **Light**: `0 4px 15px rgba(0, 0, 0, 0.2)`
- **Medium**: `0 8px 32px rgba(0, 0, 0, 0.2)`
- **Heavy**: `0 12px 40px rgba(0, 0, 0, 0.3)`

## 🌓 Dark Mode Adjustments

### Container Backgrounds
```css
/* Light Mode */
background: rgba(255, 255, 255, 0.15);

/* Dark Mode */
background: rgba(30, 30, 46, 0.4);
```

### Input Fields
```css
/* Light Mode */
background: rgba(255, 255, 255, 0.2);

/* Dark Mode */
background: rgba(255, 255, 255, 0.1);
```

## 🎭 Overlay Effects

### Radial Gradient Overlay
```css
body::before {
  content: '';
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: 
    radial-gradient(circle at 20% 50%, rgba(120, 119, 198, 0.3), transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(252, 70, 107, 0.3), transparent 50%),
    radial-gradient(circle at 40% 20%, rgba(99, 179, 237, 0.3), transparent 50%);
  pointer-events: none;
  z-index: 0;
}
```

## 📱 Responsive Breakpoints

### Mobile (max-width: 768px)
- Stack cards vertically
- Reduce padding to `20px`
- Adjust font sizes
- Simplify animations

### Desktop
- Grid layouts for cards
- Full padding and spacing
- Enhanced hover effects
- All animations active

## 🔧 Common Patterns

### Page Structure
```html
<body>
  <!-- Animated gradient background applied to body -->
  
  <nav class="navbar">
    <!-- Glassmorphism navbar -->
  </nav>
  
  <div class="container">
    <!-- Glassmorphism container with content -->
  </div>
</body>
```

### Form Pattern
```html
<div class="form-container">
  <h2>Title</h2>
  <form>
    <input type="text" placeholder="Input">
    <button>Submit</button>
  </form>
</div>
```

### Card Pattern
```html
<div class="card">
  <i class="icon"></i>
  <h3>Title</h3>
  <button class="cta">Action</button>
</div>
```

## 🎨 Typography

### Font Families
- **Primary**: 'Segoe UI', 'Roboto', sans-serif
- **Headings**: Bold (600-700)
- **Body**: Regular (400)

### Font Sizes
- **H1**: `2-3rem`
- **H2**: `1.5-2rem`
- **H3**: `1.2-1.5rem`
- **Body**: `15-16px`
- **Small**: `0.85-0.9em`

### Text Colors
- **Light Mode**: `#fff` (white)
- **Dark Mode**: `#ddd` (light gray)
- **Errors**: `#ffeb3b` (yellow)
- **Success**: `#66ff99` (green)

## 🚀 Performance Tips

1. **Use CSS transforms** instead of position changes
2. **Limit backdrop-filter** usage to visible elements
3. **Use will-change** for animated elements
4. **Optimize gradient complexity**
5. **Reduce animation duration** on mobile

## ✅ Checklist for New Pages

- [ ] Apply animated gradient background
- [ ] Add radial gradient overlay (::before)
- [ ] Use glassmorphism for containers
- [ ] Implement hover effects
- [ ] Add focus states for inputs
- [ ] Include dark mode support
- [ ] Test responsive behavior
- [ ] Verify z-index layering
- [ ] Check animation performance
- [ ] Validate color contrast

---

**Last Updated**: December 2025
**Version**: 2.0
**Design System**: TechElevate Modern UI
