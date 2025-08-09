import React from 'react';
import { Navbar, Container } from 'react-bootstrap';
import { Link } from 'react-router-dom';

const CustomNavbar = () => {
  return (
    <Navbar expand="lg" className="navbar-custom" fixed="top">
      <Container>
        <Navbar.Brand as={Link} to="/" className="d-flex align-items-center">
          <div className="me-3">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="20" cy="20" r="18" fill="url(#gradient)" stroke="#667eea" strokeWidth="2"/>
              <circle cx="20" cy="20" r="12" fill="none" stroke="#764ba2" strokeWidth="2"/>
              <circle cx="20" cy="20" r="6" fill="none" stroke="#667eea" strokeWidth="2"/>
              <circle cx="20" cy="20" r="2" fill="#764ba2"/>
              <defs>
                <linearGradient id="gradient" x1="0%" y1="0%" x2="100%" y2="100%">
                  <stop offset="0%" stopColor="#667eea" stopOpacity="0.2"/>
                  <stop offset="100%" stopColor="#764ba2" stopOpacity="0.2"/>
                </linearGradient>
              </defs>
            </svg>
          </div>
          <span className="fs-4 fw-bold">
            🎵 MyMusicMaestro
          </span>
        </Navbar.Brand>
      </Container>
    </Navbar>
  );
};

export default CustomNavbar; 