# MyMusicMaestro - React Frontend

A responsive React single-page application (SPA) for browsing music catalogues, built as the consumer-facing proof-of-concept for MyMusicMaestro.

## Overview

This React application serves as the public-facing interface for music lovers to discover and explore albums. It consumes the MyMusicMaestro Django API to provide a seamless browsing experience.

## Features

### User Stories Implemented

**Home Page** (`/`)
- Browse all albums with cover art, title, artist, release year, and brief descriptions
- Click album titles to navigate to detailed views
- Responsive grid layout adapting to screen sizes

**Album Details Page** (`/albums/:id`)
- View comprehensive album information including cover, title, artist, release year, total playtime
- Complete tracklist with track positions and durations
- Breadcrumb navigation back to home page
- Responsive design for mobile and desktop

### Technical Features

- **React Query**: Efficient data fetching and caching
- **React Router**: Client-side routing
- **React Bootstrap**: Responsive UI components
- **Error Handling**: Loading states and error boundaries
- **Performance**: Optimized rendering and data fetching

## Dependencies

The application uses only the specified dependencies:

- **React 18** - Core framework
- **React Router DOM** - Routing
- **Bootstrap 5** - CSS framework
- **React Bootstrap** - Bootstrap components for React
- **React Query** - Data fetching and state management
- **Axios** - HTTP client

## Getting Started

### Prerequisites
- Node.js 16+
- npm
- MyMusicMaestro Django backend running on `http://localhost:8000`

### Installation

1. **Navigate to React app directory**
   ```bash
   cd react-app
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm start
   ```

4. **Open application**
   - Application will open at: http://localhost:3000
   - Ensure Django backend is running at: http://localhost:8000

## Application Structure

```
src/
├── pages/
│   ├── Home.js              # Album listing page
│   └── AlbumDetails.js      # Individual album details
├── services/
│   └── api.js               # API service layer
├── App.js                   # Main application component
├── App.css                  # Application styles
└── index.js                 # Application entry point
```

## API Integration

The application consumes the following Django API endpoints:

- `GET /api/albums/` - Fetch all albums for home page
- `GET /api/albums/:id/` - Fetch specific album details

### Data Flow

1. **Home Page**: Fetches albums list from `/api/albums/`
2. **Album Details**: Fetches individual album from `/api/albums/:id/`
3. **Caching**: React Query manages data caching and revalidation
4. **Error Handling**: Graceful fallbacks for network errors

## Responsive Design

The application implements responsive design using React Bootstrap:

- **Mobile** (xs-sm): Single column layout
- **Tablet** (md): Two column grid
- **Desktop** (lg+): Four column grid for albums

## Components Overview

### Home Component
- Displays album grid with responsive columns
- Handles loading and error states
- Links to individual album pages

### AlbumDetails Component  
- Shows comprehensive album information
- Displays tracklist with formatted durations
- Provides breadcrumb navigation
- Responsive layout for cover art and details

### API Service
- Centralized API calls using Axios
- Base URL configuration for backend communication
- Error handling and response parsing

## Development

### Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm test` - Run test suite
- `npm run eject` - Eject from Create React App

### Code Standards

- **ES6+**: Modern JavaScript features
- **Functional Components**: React hooks-based components
- **Bootstrap Classes**: Consistent styling with utility classes
- **Error Boundaries**: Graceful error handling

## Testing

The application includes comprehensive error handling:

- **Loading States**: Spinners during data fetching
- **Error States**: User-friendly error messages
- **Empty States**: Appropriate messaging for no data
- **Network Errors**: Fallbacks for API failures

## Performance

### Optimizations Implemented

- **React Query Caching**: 5-minute stale time for album data
- **Image Optimization**: Responsive images with proper sizing
- **Code Splitting**: Route-based code splitting with React Router
- **Lazy Loading**: Components loaded on demand

## Browser Support

- Modern browsers supporting ES6+
- Mobile browsers (iOS Safari, Chrome Mobile)
- Responsive design for all screen sizes

## API Data Format

### Album List Response
```json
{
  "results": [
    {
      "id": 1,
      "title": "Album Title",
      "artist": "Artist Name", 
      "release_year": 2023,
      "short_description": "Brief description...",
      "cover_image_url": "/media/album_covers/cover.jpg"
    }
  ]
}
```

### Album Detail Response
```json
{
  "id": 1,
  "title": "Album Title",
  "artist": "Artist Name",
  "release_year": 2023,
  "total_playtime": 2400,
  "description": "Full description...",
  "cover_image_url": "/media/album_covers/cover.jpg",
  "tracklist": [
    {
      "position": 1,
      "song": {
        "id": 1,
        "title": "Song Title",
        "running_time": 240
      }
    }
  ]
}
```

## Deployment

### Production Build
```bash
npm run build
```

### Environment Variables
- `REACT_APP_API_URL` - Backend API URL (defaults to localhost:8000)

## Contributing

This application follows the exact requirements specification for COM2025 coursework. All features are implemented according to the provided user stories and technical constraints.

## Support

For issues related to the React frontend, ensure:
1. Django backend is running and accessible
2. API endpoints return expected data format
3. Network connectivity between frontend and backend
4. Browser developer tools for debugging API calls
