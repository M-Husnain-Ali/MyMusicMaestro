import React from 'react';
import { useParams, Link } from 'react-router-dom';
import { Container, Row, Col, Card, Table, Alert, Spinner, Breadcrumb } from 'react-bootstrap';
import { useQuery } from 'react-query';
import albumsAPI from '../services/api';

const DefaultAlbumCover = ({ title, artist }) => (
  <div className="default-album-cover" style={{ height: '400px', borderRadius: '20px' }}>
    <div className="text-center">
      <div className="music-notes mb-3">
        <span className="music-note" style={{ fontSize: '2rem' }}>🎵</span>
        <span className="music-note" style={{ fontSize: '2.5rem' }}>🎶</span>
        <span className="music-note" style={{ fontSize: '2rem' }}>🎵</span>
      </div>
      <div>
        <h4 className="text-white">{title}</h4>
        <p className="text-white-50">by {artist}</p>
      </div>
    </div>
  </div>
);

const LoadingSpinner = () => (
    <div className="loading-container">
        <Spinner animation="border" role="status" className="spinner-border">
            <span className="visually-hidden">Loading Album...</span>
        </Spinner>
        <p className="mt-3">Loading Album Details...</p>
    </div>
);

const ErrorMessage = ({ message }) => (
    <div className="error-container">
        <div className="error-icon">🎵</div>
        <h2>Oops! Album Not Found.</h2>
        <p>We couldn't load the album you're looking for. It might have been moved or deleted.</p>
        <p className="text-muted">
            <em>{message}</em>
        </p>
        <Link to="/" className="btn btn-primary mt-3">
            Back to All Albums
        </Link>
    </div>
);

const formatDuration = (seconds) => {
  const minutes = Math.floor(seconds / 60);
  const remainingSeconds = seconds % 60;
  return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
};

const formatTotalPlaytime = (seconds) => {
  if (seconds == null || isNaN(seconds)) return '0:00';
  const s = Math.max(0, Math.floor(seconds));
  const h = Math.floor(s / 3600);
  const m = Math.floor((s % 3600) / 60);
  const sec = s % 60;
  return h > 0 ? `${h}:${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}` : `${m}:${String(sec).padStart(2, '0')}`;
};

const AlbumDetails = () => {
  const { id } = useParams();
  
  const { data: album, isLoading, error } = useQuery(
    ['album', id],
    () => albumsAPI.getById(id),
    {
      retry: 3,
      staleTime: 5 * 60 * 1000,
    }
  );

  return (
    <div style={{ paddingTop: '100px' }}>
      <Container>
        {isLoading && <LoadingSpinner />}

        {error && <ErrorMessage message={`Failed to load album details: ${error.message}`} />}

        {!isLoading && !error && album && (
          <>
            {/* Breadcrumb Navigation */}
            <Breadcrumb className="mb-4">
              <Breadcrumb.Item linkAs={Link} linkProps={{ to: '/' }}>
                🏠 Home
              </Breadcrumb.Item>
              <Breadcrumb.Item active>
                🎵 {album?.title}
              </Breadcrumb.Item>
            </Breadcrumb>

            <div className="album-detail-container">
              <Row className="align-items-start">
                {/* Album Cover */}
                <Col md={5} className="album-cover-container">
                  {album?.cover_image_url && album.cover_image_url !== '/static/default_album_cover.jpg' ? (
                    <img 
                      src={album.cover_image_url} 
                      alt={`${album.title} cover`}
                      className="album-cover img-fluid"
                      style={{ maxHeight: '400px', width: '100%', objectFit: 'cover' }}
                    />
                  ) : (
                    <DefaultAlbumCover title={album?.title} artist={album?.artist} />
                  )}
                </Col>

                {/* Album Information */}
                <Col md={7} className="album-info">
                  <h1 className="album-title">{album?.title}</h1>
                  <h2 className="album-artist">by {album?.artist}</h2>
                  
                  <div className="album-details-table">
                    <Row className="mb-3">
                      <Col sm={4}><strong>📅 Release Year:</strong></Col>
                      <Col sm={8}>{album?.release_year}</Col>
                    </Row>
                    <Row className="mb-3">
                      <Col sm={4}><strong>💿 Format:</strong></Col>
                      <Col sm={8}>{album?.format?.toUpperCase()}</Col>
                    </Row>
                    <Row className="mb-3">
                      <Col sm={4}><strong>💰 Price:</strong></Col>
                      <Col sm={8}>£{album?.price}</Col>
                    </Row>
                    <Row className="mb-3">
                      <Col sm={4}><strong>⏱️ Total Playtime:</strong></Col>
                      <Col sm={8}>
                        {album?.total_playtime ? formatTotalPlaytime(album.total_playtime) : 'Unknown'}
                      </Col>
                    </Row>
                    <Row className="mb-3">
                      <Col sm={4}><strong>🎵 Tracks:</strong></Col>
                      <Col sm={8}>
                        {album?.tracklist?.length || 0} tracks
                      </Col>
                    </Row>
                  </div>

                  {album?.description && (
                    <div className="mt-4">
                      <h5 className="text-primary">📝 Description</h5>
                      <p className="lead" style={{ lineHeight: '1.8' }}>
                        {album.description}
                      </p>
                    </div>
                  )}
                </Col>
              </Row>

              {/* Tracklist */}
              {album?.tracklist && album.tracklist.length > 0 && (
                <div className="tracklist-container">
                  <h3 className="tracklist-title">🎼 Tracklist</h3>
                  <div className="table-responsive">
                    <Table className="table-hover">
                      <thead>
                        <tr>
                          <th width="10%">#</th>
                          <th width="70%">🎵 Track Title</th>
                          <th width="20%">⏱️ Duration</th>
                        </tr>
                      </thead>
                      <tbody>
                        {album.tracklist.map((track, index) => (
                          <tr key={track.id || index}>
                            <td>
                              <span className="badge bg-primary rounded-pill">
                                {track.position || index + 1}
                              </span>
                            </td>
                            <td>
                              <strong>{track.song?.title || track.title}</strong>
                            </td>
                            <td>
                              <code>{formatDuration(track.song?.running_time || track.running_time || 0)}</code>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </Table>
                  </div>
                </div>
              )}

              {(!album?.tracklist || album.tracklist.length === 0) && (
                <div className="tracklist-container">
                  <Alert variant="info" className="text-center">
                    <Alert.Heading>🎵 No Tracks Available</Alert.Heading>
                    <p>This album doesn't have any tracks listed yet.</p>
                  </Alert>
                </div>
              )}

              {/* Back to Home Button */}
              <div className="text-center mt-5">
                <Link to="/" className="btn btn-outline-primary btn-lg">
                  🏠 Back to Albums
                </Link>
              </div>
            </div>
          </>
        )}
      </Container>
    </div>
  );
};

export default AlbumDetails; 