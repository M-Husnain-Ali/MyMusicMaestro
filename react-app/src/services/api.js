import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Albums API
const albumsAPI = {
    // Get all albums with computed fields
    getAll: () => api.get('/albums/').then(response => response.data.results || response.data),
    
    // Get album details by ID
    getById: (id) => api.get(`/albums/${id}/`).then(response => response.data),
};

// Songs API
export const songsAPI = {
    // Get all songs
    getAll: () => api.get('/songs/').then(response => response.data.results || response.data),
    
    // Get song details by ID
    getById: (id) => api.get(`/songs/${id}/`).then(response => response.data),
};

// Tracklist API
export const tracklistAPI = {
    // Get all tracklist items
    getAll: () => api.get('/tracklist/').then(response => response.data.results || response.data),
    
    // Get tracklist item by ID
    getById: (id) => api.get(`/tracklist/${id}/`).then(response => response.data),
};

export default albumsAPI;