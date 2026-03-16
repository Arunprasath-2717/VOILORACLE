import React, { useRef, useState, useEffect, useMemo } from 'react';
import { Link } from 'react-router-dom';
import {
    ChevronRight, ArrowUpRight, Menu, X,
    Zap, BarChart3, Cloud, Globe as GlobeIcon,
    Shield, Cpu, Brain, Activity, Eye, Sparkles,
    TrendingUp, Users, Newspaper, Landmark, FlaskConical,
    Layers, ArrowDown, Github, FileText, Network
} from 'lucide-react';
import './LandingPage.css';
import Globe from 'react-globe.gl';

/* ══════════════════════════════════════════════════════════
   DATA
   ══════════════════════════════════════════════════════════ */
const CITIES = [
    { name: 'New York', lat: 40.7128, lng: -74.0060, value: 80 },
    { name: 'London', lat: 51.5074, lng: -0.1278, value: 90 },
    { name: 'Tokyo', lat: 35.6762, lng: 139.6503, value: 95 },
    { name: 'Paris', lat: 48.8566, lng: 2.3522, value: 70 },
    { name: 'Sydney', lat: -33.8688, lng: 151.2093, value: 65 },
    { name: 'Dubai', lat: 25.2048, lng: 55.2708, value: 85 },
    { name: 'Singapore', lat: 1.3521, lng: 103.8198, value: 80 },
    { name: 'Mumbai', lat: 19.0760, lng: 72.8777, value: 70 },
    { name: 'São Paulo', lat: -23.5505, lng: -46.6333, value: 55 },
    { name: 'Seoul', lat: 37.5665, lng: 126.9780, value: 85 },
    { name: 'Toronto', lat: 43.6532, lng: -79.3832, value: 60 },
    { name: 'Frankfurt', lat: 50.1109, lng: 8.6821, value: 50 },
    { name: 'Los Angeles', lat: 34.0522, lng: -118.2437, value: 65 },
    { name: 'Hong Kong', lat: 22.3193, lng: 114.1694, value: 75 },
];

const generateArcs = () => {
    const arcs = [];
    for (let i = 0; i < CITIES.length; i++) {
        for (let j = i + 1; j < CITIES.length; j++) {
            if (Math.random() > 0.6) {
                arcs.push({
                    startLat: CITIES[i].lat, startLng: CITIES[i].lng,
                    endLat: CITIES[j].lat, endLng: CITIES[j].lng,
                    color: ['rgba(99,102,241,0.6)', 'rgba(6,182,212,0.6)', 'rgba(37,99,235,0.6)'][Math.floor(Math.random() * 3)]
                });
            }
        }
    }
    return arcs;
};
const INITIAL_ARCS = generateArcs();

/* ── Globe Component ── */
const GlobeVisualization = ({ size }) => {
    const globeRef = useRef();
    useEffect(() => {
        if (globeRef.current) {
            globeRef.current.controls().autoRotate = true;
            globeRef.current.controls().autoRotateSpeed = 0.5;
            globeRef.current.controls().enableZoom = false;
            globeRef.current.pointOfView({ altitude: 2.2 });
        }
    }, [size]);
    if (!size.width || !size.height) return null;
    return (
        <Globe ref={globeRef} width={size.width} height={size.height}
            globeImageUrl="//unpkg.com/three-globe/example/img/earth-blue-marble.jpg"
            bumpImageUrl="//unpkg.com/three-globe/example/img/earth-topology.png"
            atmosphereColor="#818cf8" atmosphereAltitude={0.18} backgroundColor="rgba(0,0,0,0)"
            arcsData={INITIAL_ARCS} arcColor="color" arcDashLength={0.4} arcDashGap={0.2}
            arcDashAnimateTime={2000} arcsTransitionDuration={1000} arcStroke={0.8}
            pointsData={CITIES} pointLat="lat" pointLng="lng" pointColor={() => "#6366f1"}
            pointAltitude={(d) => d.value * 0.001} pointRadius={0.35} pointsMerge={true}
        />
    );
};

const ResponsiveGlobe = () => {
    const containerRef = useRef();
    const [size, setSize] = useState({ width: 0, height: 0 });
    useEffect(() => {
        const obs = new ResizeObserver((entries) => {
            if (entries[0]) { const { width, height } = entries[0].contentRect; setSize({ width, height }); }
        });
        if (containerRef.current) obs.observe(containerRef.current);
        return () => obs.disconnect();
    }, []);
    return (
        <div ref={containerRef} style={{ width: '100%', height: '100%', position: 'absolute', inset: 0 }}>
            <GlobeVisualization size={size} />
        </div>
    );
};

/* ── Floating Particles ── */
const FloatingParticles = () => {
    const particles = useMemo(() =>
        Array.from({ length: 25 }, (_, i) => ({
            id: i, left: `${Math.random() * 100}%`, size: 3 + Math.random() * 4,
            duration: 12 + Math.random() * 15, delay: Math.random() * 10,
            bg: ['rgba(99,102,241,0.25)', 'rgba(6,182,212,0.25)', 'rgba(139,92,246,0.2)'][i % 3],
        })), []);
    return (
        <div className="floating-particles">
            {particles.map(p => (
                <div key={p.id} className="f-particle" style={{
                    left: p.left, width: p.size, height: p.size, background: p.bg,
                    animationDuration: `${p.duration}s`, animationDelay: `${p.delay}s`,
                }} />
            ))}
        </div>
    );
};

/* ── Scroll Reveal Hook ── */
const useScrollReveal = () => {
    useEffect(() => {
        const nodes = document.querySelectorAll('.sr');
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(e => { if (e.isIntersecting) { e.target.classList.add('revealed'); observer.unobserve(e.target); } });
        }, { threshold: 0.1, rootMargin: '0px 0px -30px 0px' });
        nodes.forEach(n => observer.observe(n));
        return () => observer.disconnect();
    }, []);
};

/* ── Animated Counter ── */
const AnimatedNumber = ({ end, suffix = '' }) => {
    const [val, setVal] = useState(0);
    const ref = useRef();
    useEffect(() => {
        const obs = new IntersectionObserver(([e]) => {
            if (e.isIntersecting) {
                let start = 0; const step = end / 50;
                const timer = setInterval(() => {
                    start += step;
                    if (start >= end) { setVal(end); clearInterval(timer); }
                    else setVal(Math.floor(start));
                }, 20);
                obs.unobserve(e.target);
            }
        }, { threshold: 0.3 });
        if (ref.current) obs.observe(ref.current);
        return () => obs.disconnect();
    }, [end]);
    return <span ref={ref}>{val.toLocaleString()}{suffix}</span>;
};

/* ══════════════════════════════════════════════════════════
   MAIN LANDING PAGE
   ══════════════════════════════════════════════════════════ */
const LandingPage = () => {
    const [mobileMenu, setMobileMenu] = useState(false);
    const [navScrolled, setNavScrolled] = useState(false);
    useScrollReveal();

    useEffect(() => {
        const onScroll = () => setNavScrolled(window.scrollY > 40);
        window.addEventListener('scroll', onScroll, { passive: true });
        return () => window.removeEventListener('scroll', onScroll);
    }, []);

    return (
        <div className="lp-root">
            {/* Ambient BG */}
            <div className="ambient-bg">
                <div className="ambient-orb" /><div className="ambient-orb" />
                <div className="ambient-orb" /><div className="ambient-orb" />
            </div>
            <FloatingParticles />

            {/* ═══════ 1. NAVBAR ═══════ */}
            <nav className={`lp-nav ${navScrolled ? 'scrolled' : ''}`}>
                <div className="lp-nav-logo">
                    <span className="logo-emoji">🔮</span>
                    <span className="logo-name">VEILORACLE</span>
                </div>
                <button className="mobile-toggle" onClick={() => setMobileMenu(!mobileMenu)}>
                    {mobileMenu ? <X size={24} /> : <Menu size={24} />}
                </button>
                <div className={`lp-nav-links ${mobileMenu ? 'open' : ''}`}>
                    <a href="#features">Features</a>
                    <a href="#technology">Technology</a>
                    <a href="#use-cases">Use Cases</a>
                    <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="nav-github">
                        <Github size={16} /> GitHub
                    </a>
                    <Link to="/dashboard" className="lp-nav-cta">
                        Launch Intelligence <ChevronRight size={16} />
                    </Link>
                </div>
            </nav>

            {/* ═══════ 2. HERO ═══════ */}
            <section className="lp-hero">
                <div className="hero-grid">
                    <div className="hero-content sr">
                        <h1 className="hero-title">
                            Global Intelligence<br />
                            <span className="gradient-word">Powered by AI</span>
                        </h1>
                        <p className="hero-subtitle">
                            VEILORACLE analyzes global news streams in real time, detects emerging events,
                            evaluates sentiment across sectors, and delivers actionable intelligence
                            through a powerful analytics dashboard.
                        </p>
                        <div className="hero-actions">
                            <Link to="/dashboard" className="hero-btn-primary">
                                Launch Dashboard <ArrowUpRight size={18} />
                            </Link>
                            <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="hero-btn-secondary">
                                <Github size={18} /> View on GitHub
                            </a>
                        </div>
                        <p className="hero-credibility">
                            Monitoring thousands of global news signals across finance, technology, politics, and more.
                        </p>
                    </div>
                    <div className="hero-globe-wrapper sr" data-delay="2">
                        <div className="hero-globe-glow" />
                        <div className="hero-globe-container">
                            <ResponsiveGlobe />
                        </div>
                    </div>
                </div>
            </section>

            {/* ═══════ 3. PROBLEM ═══════ */}
            <section className="lp-section lp-problem">
                <div className="section-inner">
                    <div className="section-header sr">
                        <div className="section-label"><Activity size={14} /> The Challenge</div>
                        <h2 className="section-heading">
                            The world produces more information<br />
                            <span className="text-gradient">than humans can analyze</span>
                        </h2>
                        <p className="section-desc">
                            Every hour, thousands of articles, reports, and updates are published across the global
                            information ecosystem. Identifying meaningful events and understanding their impact across
                            industries is increasingly difficult.
                        </p>
                    </div>
                    <div className="problem-highlight sr" data-delay="2">
                        <Sparkles size={20} className="problem-icon" />
                        <p>VEILORACLE transforms this information chaos into structured intelligence.</p>
                    </div>
                </div>
            </section>

            {/* ═══════ 4. SOLUTION ═══════ */}
            <section className="lp-section lp-solution">
                <div className="section-inner">
                    <div className="solution-grid">
                        <div className="solution-content sr">
                            <div className="section-label"><Layers size={14} /> The Solution</div>
                            <h2 className="section-heading">
                                A new layer of<br />
                                <span className="text-gradient">global intelligence</span>
                            </h2>
                            <p className="section-desc">
                                VEILORACLE uses advanced AI models to detect real-world events from news data,
                                analyze sentiment signals, and reveal how developments influence global sectors in real time.
                            </p>
                        </div>
                        <div className="solution-bullets sr" data-delay="2">
                            {[
                                { icon: <Zap size={20} />, text: 'Detect emerging global events automatically' },
                                { icon: <TrendingUp size={20} />, text: 'Understand sentiment shifts across industries' },
                                { icon: <BarChart3 size={20} />, text: 'Track sector intelligence in real time' },
                                { icon: <Network size={20} />, text: 'Discover patterns across global information streams' },
                            ].map((b, i) => (
                                <div key={i} className="solution-bullet">
                                    <div className="bullet-icon">{b.icon}</div>
                                    <span>{b.text}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>
            </section>

            {/* ═══════ 5. FEATURES ═══════ */}
            <section id="features" className="lp-section lp-features">
                <div className="section-inner">
                    <div className="section-header sr">
                        <div className="section-label"><Eye size={14} /> Core Capabilities</div>
                        <h2 className="section-heading">
                            Built for <span className="text-gradient">enterprise intelligence</span>
                        </h2>
                    </div>
                    <div className="features-grid">
                        {[
                            {
                                icon: <Zap size={28} />, title: 'Real-Time Event Detection',
                                desc: 'Automatically groups related articles into evolving global events using semantic similarity and clustering algorithms.'
                            },
                            {
                                icon: <Brain size={28} />, title: 'AI Sentiment Intelligence',
                                desc: 'Analyze whether global developments are positive, negative, or neutral for different sectors and markets.'
                            },
                            {
                                icon: <Activity size={28} />, title: 'Sector Impact Analysis',
                                desc: 'Understand how events influence finance, technology, healthcare, energy, politics, and thousands of other sectors.'
                            },
                            {
                                icon: <BarChart3 size={28} />, title: 'Intelligence Dashboard',
                                desc: 'Visualize global insights through real-time charts, event feeds, anomaly alerts, and trend forecasting.'
                            },
                        ].map((f, i) => (
                            <div key={i} className="feature-card sr" data-delay={String(i + 1)}>
                                <div className="feature-icon-wrap">{f.icon}</div>
                                <h3 className="feature-card-title">{f.title}</h3>
                                <p className="feature-card-desc">{f.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ═══════ 6. AI TECHNOLOGY ═══════ */}
            <section id="technology" className="lp-section lp-technology">
                <div className="section-inner">
                    <div className="section-header sr">
                        <div className="section-label"><Cpu size={14} /> Under the Hood</div>
                        <h2 className="section-heading">
                            Built on <span className="text-gradient">advanced artificial intelligence</span>
                        </h2>
                        <p className="section-desc">
                            VEILORACLE combines multiple AI engines to convert unstructured news data
                            into structured intelligence insights.
                        </p>
                    </div>
                    <div className="tech-grid">
                        {[
                            { name: 'Sentence Transformers', desc: 'Semantic embeddings', color: '#6366f1' },
                            { name: 'HDBSCAN', desc: 'Event clustering', color: '#8b5cf6' },
                            { name: 'RoBERTa', desc: 'Sentiment analysis', color: '#2563eb' },
                            { name: 'spaCy', desc: 'Entity extraction', color: '#06b6d4' },
                            { name: 'Transformers', desc: 'AI summarization', color: '#7c3aed' },
                            { name: 'Predictive Analytics', desc: 'Trend forecasting', color: '#0891b2' },
                        ].map((t, i) => (
                            <div key={i} className="tech-card sr" data-delay={String(i + 1)}>
                                <div className="tech-indicator" style={{ background: t.color }} />
                                <div className="tech-name">{t.name}</div>
                                <div className="tech-desc">{t.desc}</div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ═══════ 7. HOW IT WORKS ═══════ */}
            <section className="lp-section lp-pipeline">
                <div className="section-inner">
                    <div className="section-header sr">
                        <div className="section-label"><ArrowDown size={14} /> How It Works</div>
                        <h2 className="section-heading">
                            From global news to<br />
                            <span className="text-gradient">actionable intelligence</span>
                        </h2>
                        <p className="section-desc">
                            VEILORACLE continuously collects and analyzes global news signals
                            to generate structured intelligence insights.
                        </p>
                    </div>
                    <div className="pipeline-flow sr" data-delay="2">
                        {[
                            { icon: <GlobeIcon size={22} />, label: 'Global News Sources' },
                            { icon: <Cpu size={22} />, label: 'AI Text Processing' },
                            { icon: <Zap size={22} />, label: 'Event Detection' },
                            { icon: <Brain size={22} />, label: 'Sentiment & Impact Analysis' },
                            { icon: <BarChart3 size={22} />, label: 'Real-Time Intelligence Dashboard' },
                        ].map((step, i) => (
                            <React.Fragment key={i}>
                                <div className="pipeline-step">
                                    <div className="pipeline-icon">{step.icon}</div>
                                    <span className="pipeline-label">{step.label}</span>
                                </div>
                                {i < 4 && <div className="pipeline-arrow"><ChevronRight size={18} /></div>}
                            </React.Fragment>
                        ))}
                    </div>
                </div>
            </section>

            {/* ═══════ 9. USE CASES ═══════ */}
            <section id="use-cases" className="lp-section lp-usecases">
                <div className="section-inner">
                    <div className="section-header sr">
                        <div className="section-label"><Users size={14} /> Who It's For</div>
                        <h2 className="section-heading">
                            Intelligence for <span className="text-gradient">every domain</span>
                        </h2>
                    </div>
                    <div className="usecases-grid">
                        {[
                            { icon: <TrendingUp size={26} />, title: 'Financial Analysts', desc: 'Track market-moving news events and sector sentiment shifts.' },
                            { icon: <FlaskConical size={26} />, title: 'Researchers', desc: 'Identify emerging trends and evolving global developments.' },
                            { icon: <Newspaper size={26} />, title: 'Journalists', desc: 'Detect news stories and patterns across global information streams.' },
                            { icon: <Landmark size={26} />, title: 'Policy Analysts', desc: 'Understand geopolitical developments and sector impacts.' },
                        ].map((uc, i) => (
                            <div key={i} className="usecase-card sr" data-delay={String(i + 1)}>
                                <div className="usecase-icon">{uc.icon}</div>
                                <h3 className="usecase-title">{uc.title}</h3>
                                <p className="usecase-desc">{uc.desc}</p>
                            </div>
                        ))}
                    </div>
                </div>
            </section>

            {/* ═══════ 10. GLOBAL COVERAGE ═══════ */}
            <section className="lp-section lp-coverage">
                <div className="section-inner">
                    <div className="coverage-grid">
                        <div className="coverage-text sr">
                            <div className="section-label"><GlobeIcon size={14} /> Global Reach</div>
                            <h2 className="section-heading">
                                Intelligence across<br />
                                <span className="text-gradient">thousands of sectors</span>
                            </h2>
                            <p className="section-desc">
                                VEILORACLE monitors more than 3,000 AI-generated sectors across the global
                                information ecosystem.
                            </p>
                        </div>
                        <div className="coverage-sectors sr" data-delay="2">
                            {['Finance', 'Technology', 'Healthcare', 'Energy', 'Politics', 'Science', 'Sports', 'Entertainment', 'Environment'].map((s, i) => (
                                <span key={i} className="sector-tag">{s}</span>
                            ))}
                            <span className="sector-tag sector-more">+3,000 more</span>
                        </div>
                    </div>
                </div>
            </section>

            {/* ═══════ 11. VISION ═══════ */}
            <section className="lp-section lp-vision">
                <div className="section-inner">
                    <blockquote className="vision-quote sr">
                        <Sparkles size={24} className="vision-icon" />
                        <p>
                            VEILORACLE aims to build a global intelligence layer that transforms
                            real-time information into meaningful insights.
                        </p>
                    </blockquote>
                </div>
            </section>

            {/* ═══════ 12. FINAL CTA ═══════ */}
            <section className="lp-section lp-cta">
                <div className="cta-container sr">
                    <h2 className="cta-heading">Explore global intelligence<br />in real time</h2>
                    <div className="cta-actions">
                        <Link to="/dashboard" className="cta-btn-white">
                            Launch Dashboard <ArrowUpRight size={18} />
                        </Link>
                        <a href="https://github.com" target="_blank" rel="noopener noreferrer" className="cta-btn-outline">
                            <Github size={18} /> View Project on GitHub
                        </a>
                    </div>
                </div>
            </section>

            {/* ═══════ 13. FOOTER ═══════ */}
            <footer className="lp-footer">
                <div className="footer-grid">
                    <div className="footer-brand-block">
                        <div className="footer-brand">
                            <span style={{ fontSize: '1.6rem' }}>🔮</span>
                            <span className="logo-name">VEILORACLE</span>
                        </div>
                        <p className="footer-tagline">AI-Powered Global Intelligence Platform</p>
                    </div>
                    <div className="footer-nav-block">
                        <a href="https://github.com" target="_blank" rel="noopener noreferrer">GitHub</a>
                        <a href="#features">Documentation</a>
                        <a href="#features">Contact</a>
                    </div>
                    <p className="footer-copy">© 2026 VEILORACLE</p>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;
