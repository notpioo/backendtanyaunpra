# Academic Chatbot Backend System

## Overview
A Python Flask backend system for an academic virtual assistant chatbot with dark-themed admin panel. This system provides REST API endpoints for Flutter app integration, NLP processing using Google Gemini AI, and comprehensive knowledge base management.

## Recent Changes
- **2025-11-14**: Image Upload System for Knowledge Base
  - **Cloudinary Integration:**
    - Integrated Cloudinary for cloud image storage and management
    - Created `cloudinary_service.py` with upload/delete functionality
    - Credential validation on startup with clear error messages
    - Secure handling of API keys via Replit Secrets
  - **Knowledge Base Image Support:**
    - Extended knowledge entries to support `image_url` and `image_public_id` fields
    - Admin UI supports image upload with live preview
    - Image management: upload new, replace existing, or remove images
    - Proper error handling for upload/delete failures
  - **Chatbot Image Responses:**
    - Chatbot can now send images in responses when relevant to queries
    - Search results include image_url when available
    - Testing interface renders images in chat messages
    - Example use case: Send university logo when asked "apa logo universitas?"
  - **Critical Bug Fixes:**
    - Fixed form data handling to preserve file objects
    - Fixed remove_image flag to handle JSON boolean and form checkbox 'on' value
    - Added 404 validation before processing updates
    - Implemented proper Cloudinary delete error handling
    - Fixed Firebase metadata clearing when images are removed
    - Ensures consistency between Cloudinary storage and Firebase metadata
  - **Production-Ready Implementation:**
    - Complete error handling with user-friendly messages
    - Debug logging for all image operations
    - Prevents stale metadata when Cloudinary operations fail
    - Supports both JSON API and multipart form submissions

- **2025-11-12**: Knowledge Page Enhanced with Search, Filter & Mobile View
  - **Search & Filter Features:**
    - Added search bar for searching across questions, answers, and keywords
    - Added category filter dropdown (Umum, Akademik, Administrasi, Fasilitas, Peraturan)
    - Real-time filtering with live count display
    - Search and filter work on both desktop table and mobile list views
  - **Category Badge System:**
    - Color-coded category badges: Umum (gray), Akademik (blue), Administrasi (green), Fasilitas (orange), Peraturan (red)
    - Badges display consistently in both table and list views
    - Proper lowercase class matching for CSS styling
  - **Responsive Design:**
    - **Desktop (>768px)**: Table view with sortable columns
    - **Mobile (≤768px)**: Card-based list view with better readability
    - Search bar and filter in single row on mobile for space efficiency
    - Mobile list shows question, answer preview, keywords, and action buttons
  - **Interactive Features:**
    - Filter by category dropdown
    - Search across multiple fields simultaneously
    - Add/Edit/Delete functionality preserved on mobile
    - Live count of displayed vs total knowledge entries

- **2025-11-12**: Data User Page Implementation
  - **New Data User Feature:**
    - Created comprehensive user data management page in admin panel
    - Integrated Firebase Firestore for real-time user data fetching
    - Display user information: name, NIM, faculty, and study program
    - **UserService Implementation:**
      - Runtime Firebase detection for better compatibility
      - Fallback to mock data when Firebase is not initialized
      - Fetches from `users` collection in Firestore
      - Support for user profile images and avatars
    - **Responsive UI Design:**
      - Beautiful statistics cards showing total users, faculties, and programs
      - Advanced table with search, filter by faculty, and sortable columns
      - User avatars with placeholder initials when no image available
      - Mobile-friendly responsive design with horizontal scroll for table
      - Dark theme matching existing admin panel design
    - **Interactive Features:**
      - Real-time search across name, NIM, faculty, and program
      - Faculty filter dropdown for quick filtering
      - Sortable columns (name, NIM, faculty, program)
      - Live count of displayed vs total users
    - Added `/users` route in admin panel
    - Navigation menu updated with "Data User" link

- **2025-11-12**: Multiple Announcements System & Bug Fixes
  - **Announcement System Refactoring:**
    - Changed from single announcement to multiple announcements support
    - Added full CRUD operations: Create, Read, Update, Delete
    - Each announcement has unique UUID and timestamps (created_at, updated_at)
    - **Category Classification System:** Added 5 categories (Penting, Akademik, Umum, Info, Peraturan)
      - Color-coded badges: Penting (red), Akademik (blue), Umum (gray), Info (teal), Peraturan (orange)
      - Category select field in create/edit form
      - Backend validation: only allowed categories accepted
      - Default category: 'Umum' for backward compatibility
    - New announcement service methods: `get_all_announcements()`, `create_announcement()`, `update_announcement()`, `delete_announcement()`
    - Updated REST API routes with proper authentication (`@login_required`)
    - Complete UI overhaul: list view with cards, add/edit form, delete confirmation
    - Backward compatibility maintained for dashboard with `get_current_announcement()`
    - Proper error handling and JSON validation for API endpoints
    - Firebase structure: `announcements/` node with UUID-keyed entries
  - **Chatbot Testing Bug Fix:**
    - Fixed response rendering issue where bot messages didn't appear
    - Corrected JavaScript to access `data.response` instead of `data.data.response`
    - Improved error message display for API failures
    
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
  - `/app/services/`: Business logic (Gemini AI, Knowledge management, Cloudinary image service)
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
- **Cloud Storage**: Cloudinary for image hosting with automatic optimization
- **AI Integration**: Google Gemini 2.5 Flash with academic content filtering
- **Frontend**: Dark-themed responsive admin panel with dashboard, CRUD operations, chatbot testing

## Key Features Implemented
1. **Chatbot API** (`/api/chat/message`): Natural Indonesian language responses for academic queries with image support
2. **Knowledge Management API** (`/api/knowledge/`): CRUD operations for knowledge base with image upload/management
3. **Admin Panel**: Dark-themed interface with dashboard, testing, knowledge management, and image uploads
4. **Academic Filtering**: AI-powered filtering to ensure academic-focused responses
5. **Image Management**: Cloudinary integration for uploading, storing, and delivering images in chatbot responses
6. **Mobile Ready**: REST API endpoints ready for Flutter integration

## User Preferences
- Dark theme UI matching provided design
- Indonesian language for all responses
- Academic-focused content only
- Clean, organized code structure for easy maintenance
- No excessive caching for easy development updates