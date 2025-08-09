import React from 'react';
import { Container, Row, Col, Card, Alert, Spinner } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import { useQuery } from 'react-query';
import albumsAPI from '../services/api';

const DefaultAlbumCover = ({ title, artist }) => (
  <div className="default-album-cover">
    <div className="text-center">
      <div className="music-notes mb-2">
        <span className="music-note">🎵</span>
        <span className="music-note">🎶</span>
        <span className="music-note">🎵</span>
      </div>
      <div>
        <strong>{title}</strong>
        <br />
        <small>by {artist}</small>
      </div>
    </div>
  </div>
);

const LoadingSpinner = () => (
    <div className="loading-container">
        <Spinner animation="border" role="status" className="spinner-border">
            <span className="visually-hidden">Loading...</span>
        </Spinner>
        <p className="mt-3">Loading Albums...</p>
    </div>
);

const ErrorMessage = ({ message }) => (
    <div className="error-container">
        <div className="error-icon">🎵</div>
        <h2>Oops! Something went wrong.</h2>
        <p>We couldn't load the music catalog. It might be a temporary issue.</p>
        <p className="text-muted">
            <em>{message}</em>
        </p>
        <button className="btn btn-primary mt-3" onClick={() => window.location.reload()}>
            Try Again
        </button>
    </div>
);

const AlbumCard = ({ album, index }) => (
  <Col xs={12} sm={6} md={4} lg={3} className="mb-4" key={album.id}>
    <Card 
      className="album-card h-100 hover-lift" 
      style={{ 
        animationDelay: `${index * 0.1}s`,
        animationFillMode: 'both'
      }}
    >
      {album.cover_image_url && album.cover_image_url !== '/static/default_album_cover.jpg' ? (
        <Card.Img 
          variant="top" 
          src={album.cover_image_url} 
          alt={`${album.title} cover`}
          className="card-img-top"
          onError={(e) => {
            e.target.style.display = 'none';
            e.target.nextSibling.style.display = 'block';
          }}
        />
      ) : (
        <DefaultAlbumCover title={album.title} artist={album.artist} />
      )}
      
      <Card.Body className="d-flex flex-column">
        <Card.Title as={Link} to={`/albums/${album.id}`} className="text-decoration-none card-title">
          {album.title}
        </Card.Title>
        <Card.Text className="text-muted mb-2">
          <strong>🎤 {album.artist}</strong>
        </Card.Text>
        <Card.Text className="text-muted small mb-2">
          📅 {album.release_year} • 💿 {album.format?.toUpperCase()}
        </Card.Text>
        {album.short_description && (
          <Card.Text className="flex-grow-1 card-text">
            {album.short_description}
          </Card.Text>
        )}
        <div className="mt-auto">
          <Link 
            to={`/albums/${album.id}`} 
            className="btn btn-primary btn-sm w-100"
          >
            🎵 View Details
          </Link>
        </div>
      </Card.Body>
    </Card>
  </Col>
);

const Home = () => {
  const { data: albums, isLoading, error } = useQuery('albums', albumsAPI.getAll, {
    staleTime: 5 * 60 * 1000, // 5 minutes
    cacheTime: 10 * 60 * 1000, // 10 minutes
  });

  return (
    <div style={{ paddingTop: '100px' }}>
      <Container>
        {isLoading && <LoadingSpinner />}

        {error && <ErrorMessage message={`Failed to load albums: ${error.message}`} />}

        {!isLoading && !error && (
            <>
                <div className="text-center mb-5">
                    <h1 className="page-title">
                        🎵 Discover Amazing Music
                    </h1>
                    <p className="page-subtitle">
                        Explore our curated collection of albums from talented artists around the world
                    </p>
                </div>
                
                {albums && albums.length === 0 && (
                    <Alert variant="info" className="text-center glass">
                        <Alert.Heading>🎵 No Albums Yet</Alert.Heading>
                        <p>It looks like there are no albums in our catalog yet. Check back soon!</p>
                    </Alert>
                )}
                
                {albums && albums.length > 0 && (
                    <>
                        <div className="text-center mb-4">
                            <h2 className="text-white mb-3">
                                ✨ Featured Albums ({albums.length})
                            </h2>
                        </div>
                        
                        <Row className="g-4">
                            {albums.map((album, index) => (
                                <AlbumCard key={album.id} album={album} index={index} />
                            ))}
                        </Row>

                        <div className="text-center mt-5">
                            <p className="text-white">
                                🎼 Found something you like? Click on any album to explore its tracks and details!
                            </p>
                        </div>
                    </>
                )}
            </>
        )}
      </Container>
    </div>
  );
};

export default Home; 