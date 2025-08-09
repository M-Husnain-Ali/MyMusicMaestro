# 🎵 MyMusicMaestro

A comprehensive music catalogue web application built with Django (backend) and React (frontend) for managing albums, songs, and users with role-based permissions.

## 📋 Overview

MyMusicMaestro is a modern music catalogue management system that provides:

- **🏢 Back Office (BOP)**: Professional Django-powered admin interface for music industry professionals
- **🌐 REST API**: Comprehensive JSON endpoints for external consumers and integrations  
- **📱 Consumer SPA**: Beautiful React application for end-users to browse and discover music

## 🏗️ Architecture

- **Backend**: Django 5.1.2 with SQLite/PostgreSQL
- **Frontend**: React 18 with React Router, Bootstrap, React Query
- **API**: Django REST Framework with JWT authentication
- **Database**: SQLite (development), PostgreSQL-ready for production
- **Authentication**: Session-based for BOP, JWT for API

## ✨ Features

### 👥 User Roles & Permissions

#### 🎯 **Editor (Admin)**
- ✅ Full CRUD access to all albums and songs
- ✅ Can create, edit, and delete any album
- ✅ Access to Django admin panel
- ✅ Can register new users via admin interface
- ✅ Staff permissions for backend management

#### 🎤 **Artist**
- ✅ Create and manage their own albums (case-insensitive matching)
- ✅ Add and edit songs in their albums
- ✅ View only their own albums in the backend
- ✅ Cannot delete albums or access Django admin
- ✅ Public registration available

#### 👀 **Viewer** (Legacy - not actively used)
- ✅ Read-only access to all albums
- ✅ Cannot create or modify content

### 🗄️ Database Models

#### **MusicManagerUser**
```python
- username: CharField (unique)
- email: EmailField
- display_name: CharField (artist/public name)
- role: CharField (choices: 'artist', 'editor', 'viewer')
- Standard Django user fields
```

#### **Album**
```python
- title: CharField
- artist: CharField (string, not FK)
- price: DecimalField (£0.00-£999.99)
- format: CharField (Digital Download, CD, Vinyl)
- release_date: DateField (max 3 years future)
- description: TextField
- cover_image: ImageField (optional)
- tracks: ManyToMany through AlbumTracklistItem
```

#### **Song**
```python
- title: CharField
- running_time: IntegerField (≥10 seconds)
```

#### **AlbumTracklistItem** (Through Model)
```python
- album: ForeignKey(Album)
- song: ForeignKey(Song)
- position: IntegerField
- unique_together: ('album', 'song')
```

### 🌐 API Endpoints

#### **Albums**
- `GET /api/albums/` - List all albums with metadata
- `GET /api/albums/:id/` - Album details with complete tracklist
- `POST /api/albums/` - Create album (auth required)
- `PUT/PATCH /api/albums/:id/` - Update album (auth required)
- `DELETE /api/albums/:id/` - Delete album (auth required)

#### **Songs**
- `GET /api/songs/` - List all songs
- `POST /api/songs/` - Create song (auth required)
- `PUT/PATCH /api/songs/:id/` - Update song (auth required)
- `DELETE /api/songs/:id/` - Delete song (auth required)

#### **Tracklist**
- `GET /api/tracklist/` - List all tracklist items
- `POST /api/tracklist/` - Add song to album (auth required)

#### **Authentication**
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token

## 🚀 Quick Start

### Prerequisites
- Python 3.10.12+
- Node.js 16+
- npm/yarn

### 🔧 Backend Setup

1. **Navigate to project root**
   ```bash
   cd com2025ra01914-main
   ```

2. **Install Python dependencies**
   ```bash
   pip install django djangorestframework pillow python-decouple djangorestframework-simplejwt django-cors-headers
   ```

3. **Setup database**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create users (using management commands)**
   ```bash
   # Create an admin user
   python manage.py create_admin "John Smith"
   # Creates: username=johnsmith, password=admin123
   
   # Create an artist
   python manage.py create_artist "Taylor Swift"
   # Creates: username=taylorswift, password=artist123
   
   # With custom options
   python manage.py create_artist "Ed Sheeran" --username edsheeran --password mypassword123
   ```

5. **Seed sample data (optional)**
   ```bash
   python manage.py bootstrap
   ```

6. **Start Django server**
   ```bash
   python manage.py runserver
   ```
   Backend available at: http://127.0.0.1:8000

### ⚛️ Frontend Setup

1. **Navigate to React app**
   ```bash
   cd react-app
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start React development server**
   ```bash
   npm start
   ```
   Frontend available at: http://localhost:3000

## 📁 Project Structure

```
com2025ra01914-main/
├── django-app/                     # Django backend
│   ├── catalog/                    # Main app
│   │   ├── management/
│   │   │   └── commands/
│   │   │       ├── bootstrap.py    # Sample data seeder
│   │   │       ├── create_admin.py # Create admin users
│   │   │       └── create_artist.py# Create artist users
│   │   ├── migrations/             # Database migrations
│   │   ├── templates/              # Django templates (BOP)
│   │   │   ├── catalog/
│   │   │   │   ├── base.html       # Base template with navigation
│   │   │   │   ├── album_list.html # Album catalog view
│   │   │   │   ├── album_detail.html# Album details view
│   │   │   │   ├── album_form.html # Create/edit album form
│   │   │   │   └── album_confirm_delete.html
│   │   │   └── registration/       # Auth templates
│   │   │       ├── login.html
│   │   │       └── register.html
│   │   ├── templatetags/           # Custom template filters
│   │   │   └── catalog_extras.py   # Duration formatting, animations
│   │   ├── admin.py                # Django admin configuration
│   │   ├── apps.py                 # App configuration
│   │   ├── forms.py                # Django forms
│   │   ├── models.py               # Database models
│   │   ├── permissions.py          # DRF permissions
│   │   ├── serializers.py          # DRF serializers
│   │   ├── tests.py                # Unit tests
│   │   ├── urls.py                 # URL routing
│   │   └── views.py                # Views and API endpoints
│   ├── settings.py                 # Django settings
│   ├── urls.py                     # Root URL configuration
│   ├── wsgi.py & asgi.py          # WSGI/ASGI configuration
│   └── __init__.py
├── react-app/                      # React frontend
│   ├── public/
│   │   ├── index.html              # Main HTML with custom favicon
│   │   ├── manifest.json           # PWA manifest
│   │   └── robots.txt
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.js           # Navigation component
│   │   │   └── Footer.js           # Footer component
│   │   ├── pages/
│   │   │   ├── Home.js             # Album listing page
│   │   │   └── AlbumDetails.js     # Album details page
│   │   ├── services/
│   │   │   └── api.js              # API service layer
│   │   ├── App.js                  # Main React app
│   │   ├── App.css                 # Global styles
│   │   ├── index.js                # React entry point
│   │   └── index.css               # Base styles
│   ├── package.json                # NPM dependencies
│   └── package-lock.json
├── media/                          # User uploaded files
├── db.sqlite3                      # SQLite database
├── manage.py                       # Django management script
└── README.md                       # This file
```

## 🎯 How the Application Works

### 🏢 Back Office (BOP) Workflow

1. **Authentication**: Users log in at `/accounts/login/`
2. **Album Management**: 
   - **Editors**: See all albums, full CRUD access
   - **Artists**: See only their albums (case-insensitive matching)
3. **Album Creation**: Professional form with dynamic track management
   - Add existing songs or create new ones on-the-fly
   - Reorder tracks with up/down buttons
   - Real-time duplicate validation
   - Image upload with preview
4. **Track Management**: Inline formset for adding songs to albums
5. **User Registration**: Public artist registration available

### 🌐 Public Frontend Workflow

1. **Discovery**: Users browse albums on the React SPA
2. **Album Details**: Click any album to see complete information
3. **Responsive Design**: Works on desktop, tablet, and mobile
4. **Loading States**: Professional loading spinners and error handling

### 🔌 API Integration

1. **Authentication**: JWT tokens for external API access
2. **CORS Enabled**: Ready for external frontend integration
3. **Comprehensive Endpoints**: Full CRUD operations available
4. **Computed Fields**: Total playtime, tracklist automatically calculated

## 🎨 UI/UX Features

### 🏢 Back Office Design
- **Modern Gradient Design**: Professional purple/blue theme
- **Glassmorphism Effects**: Modern transparent elements
- **Smooth Animations**: Fade-ins, hover effects, loading states
- **Responsive Layout**: Works on all screen sizes
- **Professional Forms**: Advanced album creation with real-time validation
- **Custom SVG Logo**: Branded navigation and favicon

### 📱 React Frontend Design
- **Attractive Cards**: Album cards with hover effects
- **Default Images**: Placeholder for albums without covers
- **Centered Loading**: Professional loading indicators
- **Error Handling**: User-friendly error messages
- **Animation Effects**: Smooth transitions and interactions

## 🔧 Management Commands

### Create Admin User
```bash
python manage.py create_admin "Admin Name"
# Options: --username, --email, --password
# Default: username=adminname, email=adminname@admin.com, password=admin123
```

### Create Artist User
```bash
python manage.py create_artist "Artist Name"
# Options: --username, --email, --password
# Default: username=artistname, email=artistname@artist.com, password=artist123
```

### Bootstrap Sample Data
```bash
python manage.py bootstrap
# Creates sample users, albums, and songs for testing
```

## 🔐 Authentication & Security

### BOP (Django Sessions)
- Session-based authentication for web interface
- CSRF protection enabled
- Role-based view access control
- Case-insensitive artist matching

### API (JWT Tokens)
- JWT tokens for API authentication
- Token refresh mechanism
- Permission classes for different endpoints
- CORS enabled for external access

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

Test coverage includes:
- Model validation and methods
- View permissions and responses
- API endpoints functionality
- User role-based access control

## 🚀 Deployment Notes

### Production Checklist
- [ ] Set `DEBUG = False` in settings
- [ ] Configure PostgreSQL database
- [ ] Set up static file serving
- [ ] Configure media file storage
- [ ] Set proper CORS origins
- [ ] Configure email backend
- [ ] Set up SSL/HTTPS
- [ ] Configure logging

### Environment Variables
Create a `.env` file:
```
SECRET_KEY=your-secret-key-here
DEBUG=False
DATABASE_URL=postgresql://user:pass@localhost/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

## 📚 API Documentation

### Album Response Example
```json
{
  "id": 1,
  "title": "Album Title",
  "artist": "Artist Name",
  "price": "19.99",
  "format": "Digital Download",
  "release_date": "2025-01-01",
  "description": "Album description",
  "cover_image_url": "http://example.com/media/covers/album.jpg",
  "total_playtime": 2547,
  "release_year": 2025,
  "short_description": "Album description...",
  "tracklist": [
    {
      "position": 1,
      "song": {
        "id": 1,
        "title": "Song Title",
        "running_time": 234
      }
    }
  ]
}
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add/update tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

**🎵 MyMusicMaestro** - Your ultimate music catalog management solution!

