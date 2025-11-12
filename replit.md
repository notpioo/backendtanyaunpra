# Academic Chatbot Backend System

## Overview
A Python Flask backend system for an academic virtual assistant chatbot with dark-themed admin panel. This system provides REST API endpoints for Flutter app integration, NLP processing using Google Gemini AI, and comprehensive knowledge base management.

## Recent Changes
- **2025-11-12**: Mobile & Desktop Navigation Fixes
  - **Mobile Navigation Enhancement:**
    - Mobile hamburger button now moves with navigation drawer (no longer sticky in place)
    - Button relocated inside sidebar-header to track drawer position
    - Transforms into X icon when menu is open with smooth 90deg rotation
    - Icon dynamically switches between `fa-bars` and `fa-times`
    - Full accessibility support with `aria-expanded`, `aria-label`, and `title` attributes
    - All ARIA states stay synchronized across toggle, ESC key, overlay click, and resize events
    - Professional UX matching modern web design standards
  - **Desktop Navigation Fix:**
    - Fixed collapse button being clipped/hidden when sidebar collapsed
    - Optimized collapsed header layout: reduced padding (12px 8px), vertical flex direction
    - Collapse button now 40x40px with full opacity for better visibility
    - Sidebar collapse/expand now works reliably with localStorage persistence

- **2025-11-11**: Enhanced Navigation System & Railway deployment fixes
  - **Navigation Improvements:**
    - Added collapsible sidebar with smooth animations for desktop
    - Icon-only mode when collapsed with tooltips on hover
    - LocalStorage persistence - remembers collapse state
    - Improved mobile menu with smooth slide animations
    - Keyboard shortcuts: `Ctrl/Cmd + B` to toggle sidebar (desktop)
    - Responsive design works perfectly on all screen sizes
    - Better accessibility with ARIA labels
    - Created `navigation.js` with complete navigation logic
  - **Railway Deployment:**
    - Renamed `app.py` to `application.py` to avoid import conflicts
    - Updated `wsgi.py` to import from `application.py`
    - Added `railway.json` with optimal gunicorn configuration
    - Created `Procfile` for platform compatibility
    - Added `gunicorn_config.py` for production optimization
    - Fixed "ModuleNotFoundError" and "ImportError" crashes
    - Created comprehensive deployment guides
    - Created `.gitignore` for Python projects

- **2025-09-15**: Complete implementation of chatbot backend system
  - Flask backend with organized folder structure
  - Google Gemini 2.5 Flash integration for natural Indonesian language responses
  - Mock Firebase database for development (ready for production Firebase integration)
  - Dark-themed admin panel matching user's design specification
  - CRUD operations for knowledge base management
  - Academic-focused response filtering
  - REST API endpoints for Flutter integration

## Project Architecture
- **Backend**: Python Flask with organized MVC structure
  - `/app/routes/`: API endpoint handlers (chat, knowledge, admin)
  - `/app/services/`: Business logic (Gemini AI, Knowledge management)
  - `/app/config/`: Configuration (Firebase mock/real setup)
  - `/app/templates/`: Admin panel HTML templates
  - `/app/static/`: CSS/JS assets for dark theme
  - `application.py`: Main Flask app factory and configuration (renamed from app.py)
  - `wsgi.py`: Production WSGI entry point for deployment

- **Deployment**: Production-ready configuration
  - `railway.json`: Railway platform configuration
  - `Procfile`: Platform-agnostic deployment config
  - `gunicorn_config.py`: Optimized production server settings
  - `.gitignore`: Python project ignore patterns

- **Database**: Mock Firebase Realtime Database (development), ready for production Firebase
- **AI Integration**: Google Gemini 2.5 Flash with academic content filtering
- **Frontend**: Dark-themed responsive admin panel with dashboard, CRUD operations, chatbot testing

## Key Features Implemented
1. **Chatbot API** (`/api/chat/message`): Natural Indonesian language responses for academic queries
2. **Knowledge Management API** (`/api/knowledge/`): CRUD operations for knowledge base
3. **Admin Panel**: Dark-themed interface with dashboard, testing, knowledge management
4. **Academic Filtering**: AI-powered filtering to ensure academic-focused responses
5. **Mobile Ready**: REST API endpoints ready for Flutter integration

## User Preferences
- Dark theme UI matching provided design
- Indonesian language for all responses
- Academic-focused content only
- Clean, organized code structure for easy maintenance
- No excessive caching for easy development updates