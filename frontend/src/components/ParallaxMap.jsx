import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

const ParallaxMap = () => {
  const mapRef = useRef(null);
  const containerRef = useRef(null);

  useEffect(() => {
    if (!containerRef.current) return;

    // Initialize map directly with Leaflet
    const map = L.map(containerRef.current, {
      center: [20, 0],
      zoom: 3,
      scrollWheelZoom: false,
      zoomControl: false,
      attributionControl: false,
      dragging: false,
      doubleClickZoom: false,
      touchZoom: false
    });

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png').addTo(map);

    mapRef.current = map;

    const handleScroll = () => {
      if (!mapRef.current) return;
      const scrollY = window.scrollY;
      const latOffset = scrollY * 0.005;
      const lngOffset = scrollY * 0.002;
      mapRef.current.setView([20 - latOffset, lngOffset], 3, { animate: false });
    };

    window.addEventListener('scroll', handleScroll, { passive: true });

    return () => {
      window.removeEventListener('scroll', handleScroll);
      if (mapRef.current) {
        mapRef.current.remove();
      }
    };
  }, []);

  return (
    <div className="parallax-map-wrapper" style={{
      position: 'fixed',
      inset: 0,
      zIndex: -1,
      pointerEvents: 'none',
      overflow: 'hidden',
      background: '#f4f9f7'
    }}>
      <div 
        ref={containerRef}
        className="parallax-map-inner" 
        style={{
          width: '100%',
          height: '100%',
          opacity: 0.15,
          filter: 'grayscale(100%) contrast(110%) brightness(1.05)',
        }}
      />
      <div className="parallax-vignette" style={{
        position: 'absolute',
        inset: 0,
        background: 'radial-gradient(circle at center, transparent 0%, rgba(244,249,247,0.7) 100%)',
        zIndex: 1
      }} />
    </div>
  );
};

export default ParallaxMap;
