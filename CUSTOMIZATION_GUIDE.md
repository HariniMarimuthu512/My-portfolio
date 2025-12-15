# Portfolio Customization Guide

## ✅ What's Been Added

1. **Resume Download Button** - Added in the hero section
2. **Social Links** - LinkedIn, GitHub, and Email in the footer
3. **Contact Section Links** - Added LinkedIn and GitHub links in the contact section

## 🔧 What You Need to Customize

### 1. Add Your Resume
- Save your resume as a PDF file
- Name it: `resume.pdf`
- Place it in: `static/resume.pdf`
- The download button will automatically work!

### 2. Update Social Links

**In `templates/index.html`:**

**Footer Links (around line 179-183):**
```html
<a href="https://github.com/yourusername" ...>GitHub</a>
<a href="https://linkedin.com/in/yourusername" ...>LinkedIn</a>
<a href="mailto:your.email@example.com" ...>Email</a>
```

**Contact Section Links (around line 147-150):**
```html
<a href="https://linkedin.com/in/yourusername" ...>LinkedIn</a>
<a href="https://github.com/yourusername" ...>GitHub</a>
```

**Contact Email (around line 140):**
```html
<a href="mailto:your.email@example.com">your.email@example.com</a>
```

### 3. Replace Placeholder Values

Replace these with your actual information:
- `yourusername` → Your GitHub/LinkedIn username
- `your.email@example.com` → Your actual email address

## 📍 File Locations

- Resume: `static/resume.pdf`
- HTML Template: `templates/index.html`
- CSS Styles: `static/css/style.css`

## 🎨 Features Added

- ✅ Resume download button with icon
- ✅ LinkedIn link with icon
- ✅ GitHub link with icon  
- ✅ Email link with icon
- ✅ Styled social links in footer
- ✅ Contact section with social links

All links open in new tabs (except email which opens mail client).

