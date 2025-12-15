# Python Developer Portfolio Website

A modern, responsive portfolio website built with FastAPI and vanilla JavaScript.

## Features

- Clean, modern design
- Responsive layout for all devices
- FastAPI backend for API endpoints
- Smooth animations and transitions
- Contact form functionality
- Project showcase section
- Skills and experience display

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
uvicorn main:app --reload --port 5001
```

3. Open your browser and navigate to:
```
http://localhost:5001
```

## Project Structure

```
.
├── main.py                 # FastAPI application entry point
├── routes/                 # API routes
│   ├── __init__.py
│   └── portfolio.py       # Portfolio-related endpoints
├── static/                 # Static files (CSS, JS, images)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
├── templates/              # HTML templates
│   └── index.html
└── requirements.txt        # Python dependencies
```

## Technologies Used

- **Backend**: FastAPI
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Server**: Uvicorn

