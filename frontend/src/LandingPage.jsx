import React, { useRef, useState, useCallback, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import {
    ChevronRight, ArrowUpRight, Menu, X, Droplets, Wind,
    Snowflake, Sun, Zap, BarChart3, MapPin, Cloud
} from 'lucide-react';
import './LandingPage.css';

/* ══════════════════════════════════════════════════════════
   ENERGY GRID VISUALIZATION — SVG Map with glowing lines
   ══════════════════════════════════════════════════════════ */

import Globe from 'react-globe.gl';

const CITIES = [
    { name: 'New York', lat: 40.7128, lng: -74.0060, value: 80 },
    { name: 'London', lat: 51.5074, lng: -0.1278, value: 90 },
    { name: 'Tokyo', lat: 35.6762, lng: 139.6503, value: 95 },
    { name: 'Paris', lat: 48.8566, lng: 2.3522, value: 70 },
    { name: 'Sydney', lat: -33.8688, lng: 151.2093, value: 65 },
    { name: 'Dubai', lat: 25.2048, lng: 55.2708, value: 85 },
    { name: 'Singapore', lat: 1.3521, lng: 103.8198, value: 80 },
    { name: 'Hong Kong', lat: 22.3193, lng: 114.1694, value: 75 },
    { name: 'Toronto', lat: 43.6532, lng: -79.3832, value: 60 },
    { name: 'Frankfurt', lat: 50.1109, lng: 8.6821, value: 50 },
    { name: 'Mumbai', lat: 19.0760, lng: 72.8777, value: 70 },
    { name: 'São Paulo', lat: -23.5505, lng: -46.6333, value: 55 },
    { name: 'Los Angeles', lat: 34.0522, lng: -118.2437, value: 65 },
    { name: 'Seoul', lat: 37.5665, lng: 126.9780, value: 85 }
];

const generateArcs = () => {
    const arcs = [];
    for (let i = 0; i < CITIES.length; i++) {
        for (let j = i + 1; j < CITIES.length; j++) {
            if (Math.random() > 0.6) {
                arcs.push({
                    startLat: CITIES[i].lat,
                    startLng: CITIES[i].lng,
                    endLat: CITIES[j].lat,
                    endLng: CITIES[j].lng,
                    color: ['rgba(37, 99, 235, 0.9)', 'rgba(8, 145, 178, 0.9)', 'rgba(99, 102, 241, 0.9)'][Math.floor(Math.random() * 3)]
                });
            }
        }
    }
    return arcs;
};

const INITIAL_ARCS = generateArcs();

/* ── Animated 3D Globe Visualization ── */
const EnergyMapVisualization = () => {
    const globeRef = useRef();
    const containerRef = useRef();
    const [size, setSize] = useState({ width: 0, height: 0 });
    const [arcsData] = useState(INITIAL_ARCS);

    useEffect(() => {
        const observer = new ResizeObserver((entries) => {
            if (entries[0]) {
                const { width, height } = entries[0].contentRect;
                setSize({ width, height });
            }
        });
        if (containerRef.current) observer.observe(containerRef.current);
        return () => observer.disconnect();
    }, []);

    useEffect(() => {
        if (globeRef.current) {
            globeRef.current.controls().autoRotate = true;
            globeRef.current.controls().autoRotateSpeed = 0.6;
            globeRef.current.pointOfView({ altitude: 2.2 });
        }
    }, [size]);

    return (
        <div ref={containerRef} className="energy-map-container" style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'absolute', top: 0, left: 0 }}>
            {size.width > 0 && size.height > 0 && (
                <Globe
                    ref={globeRef}
                    width={size.width}
                    height={size.height}
                    globeImageUrl="//unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
                    bumpImageUrl="//unpkg.com/three-globe/example/img/earth-topology.png"
                    atmosphereColor="#60a5fa"
                    atmosphereAltitude={0.15}
                    backgroundColor="rgba(0,0,0,0)"
                    arcsData={arcsData}
                    arcColor="color"
                    arcDashLength={0.4}
                    arcDashGap={0.2}
                    arcDashAnimateTime={2000}
                    arcsTransitionDuration={1000}
                    arcStroke={0.8}
                    pointsData={CITIES}
                    pointLat="lat"
                    pointLng="lng"
                    pointColor={() => "#2563eb"}
                    pointAltitude={(d) => d.value * 0.001}
                    pointRadius={0.3}
                    pointsMerge={true}
                />
            )}
        </div>
    );
};

/* ── Production Gauge Component ── */
const ProductionGauge = () => {
    const [production] = useState(1.03);
    const [consumption] = useState(0.94);

    return (
        <div className="gauge-panel">
            <div className="gauge-label-top">MWh</div>
            <div className="gauge-visual">
                <svg viewBox="0 0 120 70" className="gauge-svg">
                    <defs>
                        <linearGradient id="gaugeGrad" x1="0%" y1="0%" x2="100%" y2="0%">
                            <stop offset="0%" stopColor="#10b981" />
                            <stop offset="50%" stopColor="#f59e0b" />
                            <stop offset="100%" stopColor="#ef4444" />
                        </linearGradient>
                    </defs>
                    {/* Background arc */}
                    <path
                        d="M 15 60 A 45 45 0 0 1 105 60"
                        fill="none"
                        stroke="#1e293b"
                        strokeWidth="6"
                        strokeLinecap="round"
                    />
                    {/* Active arc */}
                    <path
                        d="M 15 60 A 45 45 0 0 1 105 60"
                        fill="none"
                        stroke="url(#gaugeGrad)"
                        strokeWidth="6"
                        strokeLinecap="round"
                        strokeDasharray="141"
                        strokeDashoffset={141 * (1 - production / 2)}
                    />
                    {/* Needle */}
                    <line
                        x1="60" y1="58"
                        x2={60 + 35 * Math.cos(Math.PI * (1 - production / 2))}
                        y2={58 - 35 * Math.sin(Math.PI * (1 - production / 2))}
                        stroke="#ffffff"
                        strokeWidth="1.5"
                        strokeLinecap="round"
                    />
                    <circle cx="60" cy="58" r="3" fill="#1e293b" stroke="#fff" strokeWidth="1" />
                </svg>
            </div>
            <div className="gauge-values">
                <div className="gauge-value production">
                    <span className="gauge-number">{production}</span>
                    <span className="gauge-sub">Production</span>
                </div>
                <div className="gauge-value consumption">
                    <span className="gauge-number">{consumption}</span>
                    <span className="gauge-sub">Consumption</span>
                </div>
            </div>
            <div className="gauge-spend-row">
                <div className="gauge-spend">
                    <span className="spend-symbol">$</span>
                    <span className="spend-amount">89.5</span>
                    <span className="spend-unit">M</span>
                    <span className="spend-dot green"></span>
                </div>
                <div className="gauge-spend">
                    <span className="spend-symbol">$</span>
                    <span className="spend-amount">120.32</span>
                    <span className="spend-dot amber"></span>
                </div>
            </div>
            <div className="gauge-spend-labels">
                <span>Total Spends</span>
                <span>Avg spend per sqft</span>
            </div>
        </div>
    );
};

/* ── Fuel Source Bars ── */
const FuelSourceBars = () => {
    const fuels = [
        { name: 'Solar', value: 120, color: '#10b981', gradient: 'linear-gradient(180deg, #10b981, #059669)' },
        { name: 'Wind', value: 567, color: '#8b5cf6', gradient: 'linear-gradient(180deg, #8b5cf6, #7c3aed)' },
        { name: 'Hydro', value: 894, color: 'linear-gradient(180deg, #3b82f6, #06b6d4)', gradient: 'linear-gradient(180deg, #3b82f6, #06b6d4)' },
    ];

    return (
        <div className="fuel-bars-row">
            {fuels.map((fuel, i) => (
                <div key={i} className="fuel-bar-item">
                    <div className="fuel-bar-track">
                        <div
                            className="fuel-bar-fill"
                            style={{
                                height: `${(fuel.value / 900) * 100}%`,
                                background: fuel.gradient
                            }}
                        />
                    </div>
                    <span className="fuel-bar-name">{fuel.name}</span>
                    <span className="fuel-bar-value">{fuel.value}</span>
                </div>
            ))}
        </div>
    );
};

/* ══════════════════════════════════════════════════════════
   MAIN LANDING PAGE
   ══════════════════════════════════════════════════════════ */
const LandingPage = () => {
    const [isLoaded, setIsLoaded] = useState(false);
    const [mobileMenu, setMobileMenu] = useState(false);
    const [weatherTab, setWeatherTab] = useState('rain');
    const [rainIntensity, setRainIntensity] = useState('heavy');
    const [windSpeed, setWindSpeed] = useState(65);

    const zipCodes = [
        '62153', '98104', '19105', '37206', '46207',
        '53708', '48209', '72201', '55112', '87112',
        '70113', '94102', '98122', '44113'
    ];

    useEffect(() => {
        const t = setTimeout(() => setIsLoaded(true), 200);
        return () => clearTimeout(t);
    }, []);

    return (
        <div className={`landing-container ${isLoaded ? 'loaded' : ''}`}>
            {/* ═══ NAVIGATION ═══ */}
            <nav className="landing-nav">
                <div className="nav-logo">
                    <span className="logo-icon">🔮</span>
                    <span className="logo-text">VOILORACLE</span>
                </div>
                <button className="mobile-menu-toggle" onClick={() => setMobileMenu(!mobileMenu)}>
                    {mobileMenu ? <X size={24} /> : <Menu size={24} />}
                </button>
                <div className={`nav-links ${mobileMenu ? 'open' : ''}`}>
                    <a href="#dashboard-view" className="nav-link">Dashboard</a>
                    <a href="#features" className="nav-link">Analytics</a>
                    <a href="#weather" className="nav-link">Weather</a>
                    <a href="#grid" className="nav-link">Grid Monitor</a>
                    <Link to="/dashboard" className="nav-btn-primary">
                        Launch Platform <ChevronRight size={16} />
                    </Link>
                </div>
            </nav>

            {/* ═══ MAIN DASHBOARD VISUALIZATION ═══ */}
            <section id="dashboard-view" className="dashboard-hero">
                <div className="dashboard-glow-border">
                    <div className="dashboard-inner">

                        {/* ── Map Visualization (Center) ── */}
                        <div className="map-area">
                            <EnergyMapVisualization />
                        </div>

                        {/* ── Left Panel: Production by Fuel Source ── */}
                        <div className="panel-left">
                            <div className="panel-card fuel-panel">
                                <h3 className="panel-title">Production by fuel source</h3>
                                <div className="fuel-source-grid">
                                    <div className="fuel-source-item">
                                        <div className="fuel-icon-wrapper renewable">
                                            <Zap size={14} />
                                        </div>
                                        <div className="fuel-info">
                                            <span className="fuel-type">Renewable energy</span>
                                            <div className="fuel-stats">
                                                <span className="fuel-val">89.5</span>
                                                <span className="fuel-unit">MWh</span>
                                                <span className="fuel-change up">▲ 32%</span>
                                            </div>
                                        </div>
                                    </div>
                                    <div className="fuel-source-item">
                                        <div className="fuel-icon-wrapper fossil">
                                            <BarChart3 size={14} />
                                        </div>
                                        <div className="fuel-info">
                                            <span className="fuel-type">Fossile energy</span>
                                            <div className="fuel-stats">
                                                <span className="fuel-val">193.5</span>
                                                <span className="fuel-unit">MWh</span>
                                                <span className="fuel-change down">▼ 68%</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <FuelSourceBars />
                            </div>

                            {/* ── Gauge Panel ── */}
                            <ProductionGauge />
                        </div>

                        {/* ── Right Panel: Weather + ZIP ── */}
                        <div className="panel-right">
                            <div className="panel-card weather-panel">
                                <div className="weather-header">
                                    <Cloud size={18} className="weather-icon" />
                                    <h3 className="panel-title">Weather conditions parameters</h3>
                                    <button className="weather-close">×</button>
                                </div>

                                {/* Weather tabs */}
                                <div className="weather-tabs">
                                    <button
                                        className={`weather-tab ${weatherTab === 'rain' ? 'active' : ''}`}
                                        onClick={() => setWeatherTab('rain')}
                                    >
                                        <Droplets size={14} />
                                        <span>Rain</span>
                                    </button>
                                    <button
                                        className={`weather-tab ${weatherTab === 'snow' ? 'active' : ''}`}
                                        onClick={() => setWeatherTab('snow')}
                                    >
                                        <Snowflake size={14} />
                                        <span>Snow</span>
                                    </button>
                                </div>

                                {/* Intensity options */}
                                <div className="intensity-grid">
                                    {['light', 'moderate', 'heavy'].map((level) => (
                                        <button
                                            key={level}
                                            className={`intensity-btn ${rainIntensity === level ? 'active' : ''}`}
                                            onClick={() => setRainIntensity(level)}
                                        >
                                            <div className="intensity-radio">
                                                {rainIntensity === level && <div className="intensity-dot" />}
                                            </div>
                                            <div className="intensity-info">
                                                <span className="intensity-label">
                                                    {level.charAt(0).toUpperCase() + level.slice(1)}
                                                </span>
                                                <span className="intensity-range">
                                                    {level === 'light' ? '0.1 - 2.5 mm/hr' :
                                                        level === 'moderate' ? '2.6 - 7.6 mm/hr' :
                                                            '7.7 - 50 mm/hr'}
                                                </span>
                                            </div>
                                            <div className={`intensity-bar ${level}`} />
                                        </button>
                                    ))}
                                </div>

                                {/* Wind Speed */}
                                <div className="wind-section">
                                    <span className="wind-label">Wind Speed (mph)</span>
                                    <div className="wind-slider-container">
                                        <span className="wind-min">5</span>
                                        <div className="wind-slider-track">
                                            <input
                                                type="range"
                                                min="5"
                                                max="201"
                                                value={windSpeed}
                                                onChange={(e) => setWindSpeed(e.target.value)}
                                                className="wind-slider"
                                            />
                                            <div
                                                className="wind-slider-fill"
                                                style={{ width: `${((windSpeed - 5) / 196) * 100}%` }}
                                            />
                                            {/* Color dots on the slider */}
                                            <div className="slider-dots">
                                                <span className="slider-dot green" style={{ left: '10%' }} />
                                                <span className="slider-dot blue" style={{ left: '35%' }} />
                                                <span className="slider-dot cyan" style={{ left: '55%' }} />
                                                <span className="slider-dot purple" style={{ left: '80%' }} />
                                            </div>
                                        </div>
                                        <span className="wind-max">201+</span>
                                    </div>
                                </div>
                            </div>

                            {/* ── ZIP Codes Sidebar ── */}
                            <div className="zip-sidebar">
                                {zipCodes.map((zip, i) => (
                                    <div
                                        key={i}
                                        className={`zip-item ${zip === '72201' ? 'highlighted' : ''}`}
                                    >
                                        {zip === '72201' && <span className="zip-prefix">ZIP</span>}
                                        <span className="zip-code">{zip}</span>
                                        {zip === '72201' && <span className="zip-dot-indicator" />}
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </section>

            {/* ═══ CTA SECTION ═══ */}
            <section className="cta-section">
                <div className="cta-inner">
                    <div className="cta-content">
                        <h2 className="cta-title">
                            Real-Time Energy Grid <span className="text-gradient">Intelligence</span>
                        </h2>
                        <p className="cta-desc">
                            Monitor production, consumption, and weather impacts across your entire energy
                            infrastructure. AI-powered insights for smarter grid management.
                        </p>
                        <div className="cta-actions">
                            <Link to="/dashboard" className="cta-btn-main">
                                Launch Dashboard
                                <ArrowUpRight size={18} />
                            </Link>
                            <a href="#features" className="cta-btn-secondary">
                                Explore Features
                                <ChevronRight size={18} />
                            </a>
                        </div>
                    </div>
                    <div className="cta-stats">
                        <div className="cta-stat">
                            <span className="cta-stat-val">3,000+</span>
                            <span className="cta-stat-lbl">Grid Nodes</span>
                        </div>
                        <div className="cta-stat-divider" />
                        <div className="cta-stat">
                            <span className="cta-stat-val">100M+</span>
                            <span className="cta-stat-lbl">Data Points</span>
                        </div>
                        <div className="cta-stat-divider" />
                        <div className="cta-stat">
                            <span className="cta-stat-val">0.4s</span>
                            <span className="cta-stat-lbl">Latency</span>
                        </div>
                    </div>
                </div>
            </section>

            {/* ═══ FOOTER ═══ */}
            <footer className="landing-footer">
                <div className="footer-inner">
                    <div className="footer-brand">
                        <span className="logo-icon">🔮</span>
                        <span className="logo-text">VOILORACLE</span>
                    </div>
                    <p className="footer-copy">&copy; 2026 VOILORACLE — Enterprise Energy Intelligence. All Rights Reserved.</p>
                    <div className="footer-links">
                        <a href="#dashboard-view">Dashboard</a>
                        <a href="#features">Analytics</a>
                        <Link to="/dashboard">Platform</Link>
                    </div>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;
