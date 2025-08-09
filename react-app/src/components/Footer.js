import React from 'react';
import { Container } from 'react-bootstrap';

const Footer = () => {
  return (
    <footer className="footer mt-5">
      <Container>
        <div className="text-center py-4">
          <p className="mb-2">
            <strong>🎵 MyMusicMaestro</strong> - Your Ultimate Music Catalog
          </p>
          <p className="mb-0 text-muted">
            © 2024 MyMusicMaestro. Discover, explore, and enjoy music like never before.
          </p>
        </div>
      </Container>
    </footer>
  );
};

export default Footer; 