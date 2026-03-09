import React, { useState, useEffect, useRef, useMemo } from 'react';
import {
    Activity, BarChart2, Globe, Layers, ThumbsUp, ThumbsDown, Minus,
    Link, FileText, ChevronDown, ChevronUp, TrendingUp, TrendingDown,
    AlertTriangle, Zap, Brain, Users, Building, MapPin, DollarSign,
    Search, Eye, Shield, Cpu, Sparkles, ExternalLink, Newspaper, PieChart as PieChartIcon
} from 'lucide-react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Stars, Points, PointMaterial } from '@react-three/drei';
import * as random from 'maath/random/dist/maath-random.esm';
import { Toaster, toast } from 'react-hot-toast';
import {
    ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid,
    Tooltip, BarChart as ReBarChart, Bar, Cell, PieChart as RePieChart, Pie
} from 'recharts';
import { Routes, Route, Link as RouterLink } from 'react-router-dom';
import LandingPage from './LandingPage';
import './App.css';

const API_BASE = '/api';

// ── Error Boundary ────────────────────────────────────────────
class ErrorBoundary extends React.Component {
    constructor(props) {
        super(props);
        this.state = { hasError: false };
    }
    static getDerivedStateFromError() { return { hasError: true }; }
    render() {
        if (this.state.hasError) return <div className="app-container loading-container overlay-ui"><div className="loading-text">Intelligence Interface Degraded. Please reload.</div></div>;
        return this.props.children;
    }
}
function ParticleSphere({ count, color = '#7c6cf0' }) {
    const ref = useRef();
    const pointsCount = Math.min(count || 5000, 15000);
    const sphere = useMemo(() => random.inSphere(new Float32Array(pointsCount * 3), { radius: 1.5 }), [pointsCount]);

    useFrame((state, delta) => {
        if (ref.current) {
            ref.current.rotation.x -= delta / 15;
            ref.current.rotation.y -= delta / 20;
            const scale = 1 + Math.sin(state.clock.elapsedTime) * 0.05;
            ref.current.scale.set(scale, scale, scale);
        }
    });

    return (
        <group rotation={[0, 0, Math.PI / 4]}>
            <Points ref={ref} positions={sphere} stride={3} frustumCulled={false}>
                <PointMaterial transparent color={color} size={0.012} sizeAttenuation={true} depthWrite={false} opacity={0.6} />
            </Points>
        </group>
    );
}

function InnerRing() {
    const ref = useRef();
    const ring = useMemo(() => random.inSphere(new Float32Array(2000 * 3), { radius: 0.6 }), []);

    useFrame((state, delta) => {
        if (ref.current) {
            ref.current.rotation.z += delta / 8;
        }
    });

    return (
        <Points ref={ref} positions={ring} stride={3} frustumCulled={false}>
            <PointMaterial transparent color="#00e5d0" size={0.006} sizeAttenuation={true} depthWrite={false} opacity={0.5} />
        </Points>
    );
}


// ═══════════════════════════════════════════════════════════════
// DASHBOARD COMPONENT (Extracted from old App)
// ═══════════════════════════════════════════════════════════════
const Dashboard = () => {
    // ── State ─────────────────────────────────────────────────
    const [metrics, setMetrics] = useState({
        article_count: 0, event_count: 0,
        sentiment_distribution: { Positive: 0, Negative: 0, Neutral: 0 }
    });
    const [events, setEvents] = useState([]);
    const [impacts, setImpacts] = useState([]);
    const [entities, setEntities] = useState({ entities: [], grouped: {} });
    const [trends, setTrends] = useState({ rising: [], falling: [], total_analyzed: 0 });
    const [anomalies, setAnomalies] = useState({ anomalies: [], critical_count: 0, warning_count: 0 });
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [expandedEvent, setExpandedEvent] = useState(null);
    const [activeTab, setActiveTab] = useState('overview');
    const [articlesList, setArticlesList] = useState([]);
    const [globalSearch, setGlobalSearch] = useState('');
    const [sectorSearch, setSectorSearch] = useState('');
    const [sectorNews, setSectorNews] = useState([]);
    const [isSearchingSector, setIsSearchingSector] = useState(false);
    const [systemStatus, setSystemStatus] = useState({ last_update: null, status: 'initializing', article_count: 0 });
    const prevArticleCount = useRef(0);

    // ── Data Fetching ─────────────────────────────────────────
    const fetchData = async () => {
        try {
            const [metricsRes, eventsRes, impactsRes, entitiesRes, trendsRes, anomaliesRes, articlesListRes, statusRes] = await Promise.all([
                fetch(`${API_BASE}/metrics`).catch(() => null),
                fetch(`${API_BASE}/events?limit=100`).catch(() => null),
                fetch(`${API_BASE}/impacts`).catch(() => null),
                fetch(`${API_BASE}/ai/entities`).catch(() => null),
                fetch(`${API_BASE}/ai/trends`).catch(() => null),
                fetch(`${API_BASE}/ai/anomalies`).catch(() => null),
                fetch(`${API_BASE}/articles?limit=200`).catch(() => null),
                fetch(`${API_BASE}/status`).catch(() => null),
            ]);

            if (statusRes && statusRes.ok) setSystemStatus(await statusRes.json());

            if (metricsRes && metricsRes.ok) {
                const data = await metricsRes.json();
                setMetrics(data);

                // Show notification if new articles arrive
                if (prevArticleCount.current > 0 && data.article_count > prevArticleCount.current) {
                    const diff = data.article_count - prevArticleCount.current;
                    toast.success(`Ingested ${diff} new global intelligence signals`, {
                        icon: '📡',
                        style: {
                            background: '#0c0c1a',
                            color: '#7c6cf0',
                            border: '1px solid rgba(124, 108, 240, 0.3)',
                            fontSize: '0.8rem',
                            fontWeight: '600'
                        }
                    });
                }
                prevArticleCount.current = data.article_count;
            }
            if (eventsRes && eventsRes.ok) setEvents(await eventsRes.json());
            if (impactsRes && impactsRes.ok) setImpacts(await impactsRes.json());
            if (entitiesRes && entitiesRes.ok) setEntities(await entitiesRes.json());
            if (trendsRes && trendsRes.ok) setTrends(await trendsRes.json());
            if (anomaliesRes && anomaliesRes.ok) setAnomalies(await anomaliesRes.json());
            if (articlesListRes && articlesListRes.ok) setArticlesList(await articlesListRes.json());

            setLoading(false);
            setError(null);
        } catch (err) {
            console.error("Fetch error:", err);
            setError("Failed to connect to VEILORACLE API.");
            setLoading(false);
        }
    };

    const fetchSectorNews = async (sector) => {
        if (!sector) {
            setSectorNews([]);
            return;
        }
        setIsSearchingSector(true);
        try {
            const res = await fetch(`${API_BASE}/articles/sector/${encodeURIComponent(sector)}`);
            const data = await res.json();
            setSectorNews(data);
        } catch (err) {
            console.error("Error fetching sector news:", err);
        } finally {
            setIsSearchingSector(false);
        }
    };

    const handleSectorSearch = (e) => {
        const val = e.target.value;
        setSectorSearch(val);
        if (val.length > 2) {
            fetchSectorNews(val);
        } else {
            setSectorNews([]);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 45000);
        return () => clearInterval(interval);
    }, []);

    // ── Real-time socket connection ───────────────────────────
    useEffect(() => {
        const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const wsUrl = `${protocol}://${window.location.host}/ws`;
        const ws = new WebSocket(wsUrl);
        ws.onopen = () => console.log("WS connected");
        ws.onmessage = (evt) => {
            try {
                const data = JSON.parse(evt.data);
                setSystemStatus(prev => ({ ...prev, ...data }));
            } catch (e) {
                console.warn("WS parse error", e);
            }
        };
        ws.onclose = () => console.log("WS closed");
        return () => ws.close();
    }, []);

    // ── Pre-calculations ──────────────────────────────────────
    const isLive = metrics?.article_count > 0;
    const filteredImpacts = (impacts || []).filter(imp =>
        (imp.sector || '').toLowerCase().includes(sectorSearch.toLowerCase() || globalSearch.toLowerCase())
    );
    const filteredEvents = (events || []).filter(ev =>
        (ev.label || '').toLowerCase().includes(globalSearch.toLowerCase()) ||
        (ev.sentiment_label || '').toLowerCase().includes(globalSearch.toLowerCase())
    );
    const filteredArticles = (articlesList || []).filter(art =>
        (art.title || '').toLowerCase().includes(globalSearch.toLowerCase()) ||
        (art.source || '').toLowerCase().includes(globalSearch.toLowerCase())
    );

    const totalPositive = metrics?.sentiment_distribution?.Positive || 0;
    const totalNegative = metrics?.sentiment_distribution?.Negative || 0;
    const totalNeutral = metrics?.sentiment_distribution?.Neutral || 0;
    const isBullish = totalPositive > totalNegative;
    const stabilityScore = metrics?.article_count > 0 ? ((totalPositive / metrics.article_count) * 100).toFixed(1) : '--';
    const moodColor = isBullish ? '#00e5d0' : '#ff5252';
    const activePulseSpeed = loading ? 0.8 : 0.4;

    // ── Tab Definitions ───────────────────────────────────────
    const tabs = [
        { id: 'overview', label: 'Overview', icon: <Eye size={14} /> },
        { id: 'events', label: 'Live Events', icon: <Zap size={14} />, badge: filteredEvents.length },
        { id: 'sectors', label: 'Sector Analysis', icon: <Activity size={14} />, badge: filteredImpacts.length },
        { id: 'articles', label: 'News Feed', icon: <Newspaper size={14} />, badge: filteredArticles.length },
    ];

    // ── Mood Color ────────────────────────────────────────────
    const moodClass = isBullish ? 'mood-bullish' : 'mood-bearish';

    // ── Entity Icon ───────────────────────────────────────────
    const entityIcon = (label) => {
        switch (label) {
            case 'ORG': return <Building size={12} />;
            case 'PERSON': return <Users size={12} />;
            case 'GPE': case 'LOC': return <MapPin size={12} />;
            case 'MONEY': return <DollarSign size={12} />;
            default: return <Sparkles size={12} />;
        }
    };



    return (
        <>
            {/* ── 3D Background (Constant) ────────────────────────── */}
            <div className="canvas-container">
                <ErrorBoundary>
                    <Canvas camera={{ position: [0, 0, 3] }}>
                        <ambientLight intensity={0.3} />
                        <Stars radius={100} depth={50} count={2000} factor={4} saturation={0} fade speed={1} />
                        <ParticleSphere count={loading ? 2000 : 5000} color={moodColor} />
                        {!loading && <InnerRing />}
                        <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={activePulseSpeed} />
                    </Canvas>
                </ErrorBoundary>
                <div className="canvas-overlay"></div>
            </div>
            <Toaster position="bottom-right" />

            {/* ── Conditional UI Overlay ──────────────────────────── */}
            {loading ? (
                <div className="app-container loading-container overlay-ui">
                    <div className="loading-spinner"></div>
                    <div className="loading-text">Initializing Neural Intelligence Matrix...</div>
                    <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', marginTop: '1rem' }}>
                        Fetching real-time telemetry from global nodes...
                    </div>
                </div>
            ) : (
                <div className="app-container overlay-ui">

                    {/* Header */}
                    <header className="header">
                        <div className="title-container">
                            <div className="oracle-title">🔮 VOILORACLE</div>
                            <div className="oracle-subtitle">Enhanced Global Intelligence Network</div>
                        </div>
                        <div className="header-actions">
                            <div className="search-box">
                                <Search className="search-icon" size={16} color="var(--text-muted)" />
                                <input
                                    type="text"
                                    placeholder="Search systems intelligence..."
                                    value={globalSearch}
                                    onChange={(e) => setGlobalSearch(e.target.value)}
                                />
                            </div>
                            <div className="status-container">
                                <div className="status-indicator">
                                    <span className={`status-dot ${isLive ? 'status-live' : 'status-offline'}`}></span>
                                    <span className="status-text">{isLive ? 'SYSTEMS LIVE' : 'OFFLINE'}</span>
                                </div>
                                <div className="update-time">
                                    Last Update: {systemStatus.last_update ? new Date(systemStatus.last_update).toLocaleTimeString() : '--:--:--'}
                                </div>
                            </div>
                        </div>
                    </header>

                    {error ? (
                        <div className="error-banner">⚠️ {error}</div>
                    ) : (
                        <>
                            {/* ── Dashboard Pulse — Global Stability ─── */}
                            <div className="intelligence-overview">
                                <div className="overview-main glass-panel">
                                    <div className="stability-core">
                                        <div className="stability-meter">
                                            <svg viewBox="0 0 100 100">
                                                <circle cx="50" cy="50" r="45" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="8" />
                                                <circle cx="50" cy="50" r="45" fill="none" stroke="var(--accent-cyan)" strokeWidth="8"
                                                    strokeDasharray={`${(stabilityScore === '--' ? 0 : stabilityScore) * 2.8} 283`}
                                                    strokeLinecap="round" transform="rotate(-90 50 50)" />
                                            </svg>
                                            <div className="stability-value">
                                                <span>{stabilityScore}%</span>
                                                <small>STABILITY</small>
                                            </div>
                                        </div>
                                        <div className="stability-info">
                                            <div className="briefing-tag">GLOBAL INTEERELIGENCE STATUS</div>
                                            <div className="briefing-title">Neural Matrix: {isBullish ? 'Bullish' : 'Bearish'}</div>
                                            <div className="briefing-text">Analyzing global domains, detecting market structures and mapping events across {metrics.article_count} neural impact points.</div>
                                        </div>
                                    </div>
                                </div>

                                <div className="overview-stats">
                                    <div className="stat-box glass-panel">
                                        <div className="stat-icon"><Globe size={18} color="var(--accent-blue)" /></div>
                                        <div className="stat-data">
                                            <div className="stat-val">{metrics.article_count.toLocaleString()}</div>
                                            <div className="stat-lbl">SIGNS INGESTED</div>
                                        </div>
                                    </div>
                                    <div className="stat-box glass-panel">
                                        <div className="stat-icon"><Zap size={18} color="var(--accent-cyan)" /></div>
                                        <div className="stat-data">
                                            <div className="stat-val">{metrics.event_count.toLocaleString()}</div>
                                            <div className="stat-lbl">CLUSTERS DETECTED</div>
                                        </div>
                                    </div>
                                    <div className="stat-box glass-panel">
                                        <div className="stat-icon"><TrendingUp size={18} color="var(--positive)" /></div>
                                        <div className="stat-data">
                                            <div className="stat-val">{trends.rising?.length || 0}</div>
                                            <div className="stat-lbl">RISING DOMAINS</div>
                                        </div>
                                    </div>
                                    <div className="stat-box glass-panel">
                                        <div className="stat-icon"><AlertTriangle size={18} color="var(--negative)" /></div>
                                        <div className="stat-data">
                                            <div className="stat-val">{anomalies.critical_count || 0}</div>
                                            <div className="stat-lbl">CRITICAL RISKS</div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* ── Tab Navigation ─── */}
                            <div className="tab-nav">
                                {tabs.map(tab => (
                                    <button
                                        key={tab.id}
                                        className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
                                        onClick={() => setActiveTab(tab.id)}
                                    >
                                        {tab.icon}
                                        {tab.label}
                                        {tab.badge > 0 && <span className="tab-badge">{tab.badge > 999 ? '999+' : tab.badge}</span>}
                                    </button>
                                ))}
                            </div>

                            {/* ═══════════════════════════════════════════════
                            TAB: OVERVIEW
                           ═══════════════════════════════════════════════ */}
                            {activeTab === 'overview' && (
                                <div className="main-content">
                                    <div className="section glass-panel">
                                        <div className="section-title">
                                            <TrendingUp size={18} color="var(--accent-purple)" />
                                            Intelligence Domain Shifts
                                        </div>
                                        <div className="shift-grid">
                                            {trends.rising?.slice(0, 4).map((t, i) => (
                                                <div key={i} className="shift-card glass-card">
                                                    <div className="shift-header">
                                                        <span className="shift-sector" title={t.sector}>{t.sector}</span>
                                                        <span className="shift-momentum rising">↑ {t.momentum?.toFixed(1) || t.momentum}</span>
                                                    </div>
                                                    <div className="shift-bar"><div className="shift-fill positive" style={{ width: `${(t.confidence || 0.5) * 100}%` }}></div></div>
                                                    <div className="shift-footer">RELIABILITY: {((t.confidence || 0.5) * 100).toFixed(0)}%</div>
                                                </div>
                                            ))}
                                            {trends.falling?.slice(0, 4).map((t, i) => (
                                                <div key={i} className="shift-card glass-card">
                                                    <div className="shift-header">
                                                        <span className="shift-sector" title={t.sector}>{t.sector}</span>
                                                        <span className="shift-momentum falling">↓ {Math.abs(t.momentum?.toFixed(1) || t.momentum)}</span>
                                                    </div>
                                                    <div className="shift-bar"><div className="shift-fill negative" style={{ width: `${(t.confidence || 0.5) * 100}%` }}></div></div>
                                                    <div className="shift-footer">RISK LEVEL: {((t.confidence || 0.5) * 100).toFixed(0)}%</div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className="section glass-panel">
                                        <div className="section-title">
                                            <Activity size={18} color="var(--accent-cyan)" />
                                            Market Matrix Heatmap
                                        </div>
                                        <div className="impact-grid virtualized-scroll">
                                            {impacts.slice(0, 64).map((imp, i) => {
                                                let cl = imp.direction === "Bullish" ? "bullish" : imp.direction === "Bearish" ? "bearish" : "mixed";
                                                return (
                                                    <div key={i} className={`matrix-node ${cl}`} title={`${imp.sector}: ${imp.direction}`}></div>
                                                );
                                            })}
                                        </div>
                                        <div className="matrix-legend">
                                            <span><span className="status-dot status-live"></span> Bullish Signal</span>
                                            <span><span className="status-dot status-offline" style={{ background: 'var(--negative)' }}></span> Bearish Threat</span>
                                            <span><span className="status-dot" style={{ background: 'var(--text-muted)' }}></span> Mixed/Neutral</span>
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* ═══════════════════════════════════════════════
                            TAB: LIVE EVENTS (Smart Event Cards)
                           ═══════════════════════════════════════════════ */}
                            {activeTab === 'events' && (
                                <div className="main-content single-column">
                                    <div className="smart-event-list">
                                        {events.length > 0 ? events.map((ev, i) => (
                                            <div key={i} className={`smart-event-card glass-panel ${expandedEvent === i ? 'expanded' : ''}`} onClick={() => setExpandedEvent(expandedEvent === i ? null : i)}>
                                                <div className="event-meta">
                                                    <div className="event-score" style={{ borderLeft: `4px solid ${ev.sentiment_label === 'Positive' ? 'var(--positive)' : ev.sentiment_label === 'Negative' ? 'var(--negative)' : 'var(--neutral)'}` }}>
                                                        <div className="score-val">{ev.importance_score?.toFixed(0) || 50}</div>
                                                        <div className="score-lbl">IMPORTANCE</div>
                                                    </div>
                                                    <div className="event-body">
                                                        <div className="event-header">
                                                            <div className="event-title">{ev.label}</div>
                                                        </div>
                                                        <div className="event-footer">
                                                            <div className={`event-sentiment-badge badge-${(ev.sentiment_label || 'neutral').toLowerCase()}`}>
                                                                {ev.sentiment_label}
                                                            </div>
                                                            <div className={`event-sentiment-badge`} style={{ background: 'var(--accent-purple)', color: 'white' }}>
                                                                Lifecycle: {(ev.lifecycle || 'emerging').toUpperCase()}
                                                            </div>
                                                            <div className="event-impacts">
                                                                {ev.impacts?.map((imp, idx) => (
                                                                    <span key={idx} className={`impact-chip ${imp.direction.toLowerCase()}`}>
                                                                        {imp.sector} {imp.direction === 'Bullish' ? '↑' : '↓'}
                                                                    </span>
                                                                ))}
                                                                {ev.size > 1 && <span className="entity-chip"><Globe size={10} /> {ev.size} signals (Weight: {ev.weight_score?.toFixed(2) || '1.00'})</span>}
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div className="event-chevron">
                                                        {expandedEvent === i ? <ChevronUp size={20} /> : <ChevronDown size={20} />}
                                                    </div>
                                                </div>

                                                {expandedEvent === i && (
                                                    <div className="event-expanded-content animate-fadeIn">
                                                        <div className="event-briefing glass-card">
                                                            <div className="briefing-header"><Sparkles size={14} color="var(--accent-cyan)" /> AI Neural Briefing</div>
                                                            <div className="briefing-text">{ev.ai_summary || "Analyzing intelligence vectors for this event cluster..."}</div>
                                                        </div>
                                                        <div className="article-links">
                                                            {ev.articles && ev.articles.slice(0, 10).map((art, j) => (
                                                                <a key={j} href={art.url} target="_blank" rel="noopener noreferrer" className="article-link-item" onClick={(e) => e.stopPropagation()}>
                                                                    <span className="title">{art.title}</span>
                                                                    <span className="source-meta">
                                                                        {art.source && <span className="source-name">{art.source}</span>}
                                                                        <ExternalLink size={10} color="var(--accent-purple)" />
                                                                    </span>
                                                                </a>
                                                            ))}
                                                        </div>
                                                    </div>
                                                )}
                                            </div>
                                        )) : (
                                            <div className="empty-state">
                                                <div className="empty-state-icon">📡</div>
                                                <div className="empty-state-text">Matrix stabilized. No event clusters detected.</div>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}

                            {/* ═══════════════════════════════════════════════
                            TAB: INTELLIGENCE (Combined Analysis)
                           ═══════════════════════════════════════════════ */}
                            {activeTab === 'intelligence' && (
                                <div className="main-content">
                                    <div className="section glass-panel">
                                        <div className="section-title">
                                            <Layers size={18} color="var(--accent-cyan)" />
                                            Entity Neural Network
                                        </div>
                                        <div className="entity-cloud">
                                            {entities.entities?.slice(0, 40).map((ent, i) => (
                                                <div key={i} className="entity-pill glass-card">
                                                    {entityIcon(ent.label)}
                                                    <span className="entity-text">{ent.text}</span>
                                                    <span className="entity-count">{ent.count}</span>
                                                </div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className="section glass-panel">
                                        <div className="section-title">
                                            <AlertTriangle size={18} color="var(--negative)" />
                                            Neural Anomalies & Threats
                                            <span className="section-title-count">({anomalies.total_detected || 0})</span>
                                        </div>
                                        <div className="anomaly-list">
                                            {anomalies.anomalies?.slice(0, 10).map((anom, i) => (
                                                <div key={i} className={`anomaly-card glass-card ${anom.severity}`}>
                                                    <div className="anomaly-header">
                                                        <span className="anomaly-sector">{anom.dimension}</span>
                                                        <span className={`severity-badge ${anom.severity}`}>{anom.severity.toUpperCase()}</span>
                                                    </div>
                                                    <div className="anomaly-msg">{anom.message}</div>
                                                    <div className="anomaly-meta">Z-Score: {anom.score.toFixed(2)}</div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            )}
                            {/* ═══════════════════════════════════════════════
                            TAB: ARTICLES (Clickable News Feed)
                           ═══════════════════════════════════════════════ */}
                            {activeTab === 'articles' && (
                                <div className="main-content single-column">
                                    {/* AI TOP PICKS / SUGGESTIONS SECTION */}
                                    {articlesList.length > 0 && (
                                        <div className="section glass-panel" style={{ marginBottom: '20px' }}>
                                            <div className="section-title">
                                                <Sparkles size={18} color="var(--accent-purple)" />
                                                AI Top Picks & Suggestions
                                                <span className="section-title-count">(Curated for you)</span>
                                            </div>
                                            <div className="top-picks-grid" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '15px', marginTop: '15px' }}>
                                                {[...articlesList]
                                                    .sort((a, b) => Math.abs(b.sentiment_score || 0) - Math.abs(a.sentiment_score || 0))
                                                    .slice(0, 3)
                                                    .map((art, i) => (
                                                        <a key={`pick-${i}`} href={art.url || '#'} target="_blank" rel="noopener noreferrer" className="top-pick-card glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '10px', padding: '15px', textDecoration: 'none' }}>
                                                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                                                <span className="badge" style={{ background: 'rgba(124,108,240,0.15)', color: 'var(--accent-purple)', border: '1px solid rgba(124,108,240,0.3)' }}>{['🔥 Hot Pick', '💡 Deep Insight', '📈 High Impact'][i]}</span>
                                                                <ExternalLink size={14} color="var(--accent-purple)" />
                                                            </div>
                                                            <div style={{ fontSize: '0.95rem', fontWeight: '500', color: 'var(--text-light)', lineHeight: '1.4' }}>{art.title}</div>
                                                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                                                                <span className={`badge badge-${(art.sentiment_label || '').toLowerCase()}`}>{art.sentiment_label}</span>
                                                                <span className="article-source-badge">{art.source}</span>
                                                            </div>
                                                        </a>
                                                    ))}
                                            </div>
                                        </div>
                                    )}

                                    <div className="section glass-panel">
                                        <div className="section-title">
                                            <Newspaper size={18} color="var(--accent-blue)" />
                                            Live News Feed
                                            <span className="section-title-count">(Click any article to read on its original source)</span>
                                        </div>
                                        <div className="events-list">
                                            {articlesList.length > 0 ? articlesList.map((art, i) => (
                                                <a
                                                    key={art.id || i}
                                                    className="article-feed-card glass-card"
                                                    href={art.url || '#'}
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                >
                                                    <div className="article-feed-main">
                                                        <div className="article-feed-title">
                                                            <FileText size={14} color="var(--text-muted)" style={{ flexShrink: 0, marginTop: 2 }} />
                                                            {art.title}
                                                        </div>
                                                        <div className="article-feed-meta">
                                                            <span className="article-source-badge">{art.source}</span>
                                                            <span className={`badge badge-${(art.sentiment_label || '').toLowerCase()}`}>
                                                                {art.sentiment_label}
                                                            </span>
                                                            <span className={`badge ${art.fake_news_label === 'Fake' ? 'badge-negative' : 'badge-neutral'}`} style={{ border: art.fake_news_label === 'Fake' ? '1px solid #ff5252' : '1px solid var(--accent-cyan)' }}>
                                                                {art.fake_news_label === 'Fake' ? '🚨 Disinformation Flags' : 'Verified Real'} ({(art.fake_news_score * 100).toFixed(0)}%)
                                                            </span>
                                                            <span style={{ color: 'var(--text-muted)', fontSize: '0.68rem', fontFamily: "'JetBrains Mono', monospace" }}>
                                                                Score: {(art.sentiment_score || 0).toFixed(2)}
                                                            </span>
                                                            {art.published_at && (
                                                                <span style={{ color: 'var(--text-muted)', fontSize: '0.65rem' }}>
                                                                    {new Date(art.published_at).toLocaleDateString()}
                                                                </span>
                                                            )}
                                                        </div>
                                                    </div>
                                                    <ExternalLink size={16} color="var(--accent-purple)" style={{ flexShrink: 0 }} />
                                                </a>
                                            )) : (
                                                <div className="empty-state">
                                                    <div className="empty-state-icon">📰</div>
                                                    <div className="empty-state-text">No articles yet. Run the pipeline to collect news.</div>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* ═══════════════════════════════════════════════
                            TAB: SECTORS (Full Sector View)
                           ═══════════════════════════════════════════════ */}
                            {activeTab === 'sectors' && (
                                <div className="main-content">
                                    <div className="section glass-panel">
                                        <div className="section-title">
                                            <Activity size={18} color="var(--accent-purple)" />
                                            Deep Intelligence Matrix
                                            <span className="section-title-count">({impacts.length.toLocaleString()} sectors analyzed)</span>
                                        </div>
                                        <div className="search-box glass-panel" style={{ width: '100%', marginBottom: '1.5rem', background: 'rgba(255,255,255,0.03)' }}>
                                            <Search className="search-icon" size={16} color="var(--text-muted)" />
                                            <input
                                                type="text" placeholder="Search across all AI-analyzed sectors..."
                                                style={{ background: 'transparent', border: 'none', outline: 'none', color: 'white', width: '100%', padding: '8px 0' }}
                                                value={sectorSearch}
                                                onChange={handleSectorSearch}
                                            />
                                        </div>
                                        <div className="impact-grid virtualized-scroll" style={{ maxHeight: 'calc(100vh - 400px)' }}>
                                            {filteredImpacts.slice(0, 150).map((imp, i) => {
                                                let arr = "→", cl = "impact-mixed";
                                                if (imp.direction === "Bullish") { arr = "↑"; cl = "impact-bullish"; }
                                                else if (imp.direction === "Bearish") { arr = "↓"; cl = "impact-bearish"; }
                                                return (
                                                    <div key={i} className="impact-cell mini-cell glass-card" onClick={() => { setSectorSearch(imp.sector); fetchSectorNews(imp.sector); }} style={{ cursor: 'pointer' }}>
                                                        <div className="impact-sector" title={imp.sector}>{imp.sector}</div>
                                                        <div className={`impact-direction ${cl}`}>{arr}</div>
                                                        <div className="impact-stats">
                                                            <span className="up">▲{imp.bullish}</span> • <span className="down">▼{imp.bearish}</span>
                                                        </div>
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    </div>

                                    <div className="section glass-panel">
                                        <div className="section-title">
                                            <Sparkles size={18} color="var(--accent-cyan)" />
                                            Linked Sector Intel (Past News)
                                            {sectorSearch && <span className="section-title-count" style={{ color: 'var(--accent-purple)' }}> - {sectorSearch}</span>}
                                        </div>
                                        <div className="events-list">
                                            {isSearchingSector ? (
                                                <div className="empty-state">
                                                    <div className="loading-spinner" style={{ width: 30, height: 30 }}></div>
                                                    <div className="empty-state-text">Retrieving past intelligence vectors...</div>
                                                </div>
                                            ) : sectorNews.length > 0 ? sectorNews.map((art, i) => (
                                                <a key={art.id || i} className="article-feed-card glass-card" href={art.url || '#'} target="_blank" rel="noopener noreferrer">
                                                    <div className="article-feed-main">
                                                        <div className="article-feed-title" style={{ fontSize: '0.82rem' }}>{art.title}</div>
                                                        <div className="article-feed-meta">
                                                            <span className="article-source-badge">{art.source}</span>
                                                            <span className={`badge badge-${(art.sentiment_label || '').toLowerCase()}`}>{art.sentiment_label}</span>
                                                            <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)' }}>{art.published_at ? new Date(art.published_at).toLocaleDateString() : ''}</span>
                                                        </div>
                                                    </div>
                                                    <ExternalLink size={14} color="var(--accent-purple)" />
                                                </a>
                                            )) : (
                                                <div className="empty-state">
                                                    <div className="empty-state-icon">📚</div>
                                                    <div className="empty-state-text">Select a sector to view contributing news articles.</div>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* ═══════════════════════════════════════════════
                            TAB: EVENTS (Full Events View)
                           ═══════════════════════════════════════════════ */}
                            {activeTab === 'events' && (
                                <div className="main-content single-column">
                                    <div className="section glass-panel">
                                        <div className="section-title">
                                            <Zap size={18} color="var(--accent-cyan)" />
                                            AI-Detected Event Clusters
                                            <span className="section-title-count">(DBSCAN Clustering + Sentence Embeddings)</span>
                                        </div>
                                        <div className="events-list">
                                            {events.map((ev, i) => (
                                                <div key={ev.id || i} className="event-card glass-card" onClick={() => setExpandedEvent(expandedEvent === i ? null : i)}>
                                                    <div className="event-header">
                                                        <div className="event-title">
                                                            <div className="event-title-icon">
                                                                {ev.is_cluster ? <Link size={13} color="var(--accent-purple)" /> : <FileText size={13} />}
                                                            </div>
                                                            {(ev.label || '').substring(0, 120)}{(ev.label || '').length > 120 ? '...' : ''}
                                                        </div>
                                                        {expandedEvent === i ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
                                                    </div>
                                                    <div className="event-meta">
                                                        <span className={`badge badge-${(ev.sentiment_label || '').toLowerCase()}`}>{ev.sentiment_label}</span>
                                                        <span>Score: {(ev.sentiment_score || 0).toFixed(3)}</span>
                                                        <span>•</span>
                                                        <span>{ev.size} Article{ev.size !== 1 ? 's' : ''}</span>
                                                        {ev.is_cluster && <span className="badge" style={{ background: 'rgba(124,108,240,0.15)', color: 'var(--accent-purple)', border: '1px solid rgba(124,108,240,0.3)' }}>CLUSTER</span>}
                                                    </div>
                                                    {expandedEvent === i && ev.articles && (
                                                        <div className="event-articles">
                                                            {ev.articles.map((art, j) => (
                                                                <a key={j} className="article-item article-link" href={art.url || '#'} target="_blank" rel="noopener noreferrer" onClick={(e) => e.stopPropagation()}>
                                                                    <span className="article-title">{art.title}</span>
                                                                    <span className="article-meta-row">
                                                                        {art.source && <span className="article-source-badge">{art.source}</span>}
                                                                        <span className={`badge badge-${(art.sentiment_label || '').toLowerCase()}`}>{art.sentiment_label}</span>
                                                                        <ExternalLink size={11} color="var(--accent-purple)" />
                                                                    </span>
                                                                </a>
                                                            ))}
                                                        </div>
                                                    )}
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* ═══════════════════════════════════════════════
                            TAB: NER ENTITIES (spaCy-extracted)
                           ═══════════════════════════════════════════════ */}
                            {activeTab === 'entities' && (
                                <div className="main-content single-column">
                                    <div className="section glass-panel">
                                        <div className="section-title">
                                            <Brain size={18} color="var(--accent-blue)" />
                                            AI Named Entity Recognition
                                            <span className="section-title-count">(spaCy NLP Engine)</span>
                                        </div>

                                        {entities.grouped && Object.keys(entities.grouped).length > 0 ? (
                                            <>
                                                {entities.grouped.ORG && entities.grouped.ORG.length > 0 && (
                                                    <>
                                                        <div className="entity-section-title"><Building size={14} /> Organizations</div>
                                                        <div className="entity-cloud">
                                                            {entities.grouped.ORG.map((ent, i) => (
                                                                <div key={i} className="entity-chip entity-ORG" style={{ animationDelay: `${i * 0.03}s` }}>
                                                                    <Building size={12} />
                                                                    {ent.text}
                                                                    <span className="entity-count">×{ent.count}</span>
                                                                </div>
                                                            ))}
                                                        </div>
                                                    </>
                                                )}

                                                {entities.grouped.PERSON && entities.grouped.PERSON.length > 0 && (
                                                    <>
                                                        <div className="entity-section-title"><Users size={14} /> People</div>
                                                        <div className="entity-cloud">
                                                            {entities.grouped.PERSON.map((ent, i) => (
                                                                <div key={i} className="entity-chip entity-PERSON" style={{ animationDelay: `${i * 0.03}s` }}>
                                                                    <Users size={12} />
                                                                    {ent.text}
                                                                    <span className="entity-count">×{ent.count}</span>
                                                                </div>
                                                            ))}
                                                        </div>
                                                    </>
                                                )}

                                                {entities.grouped.GPE && entities.grouped.GPE.length > 0 && (
                                                    <>
                                                        <div className="entity-section-title"><MapPin size={14} /> Locations</div>
                                                        <div className="entity-cloud">
                                                            {entities.grouped.GPE.map((ent, i) => (
                                                                <div key={i} className="entity-chip entity-GPE" style={{ animationDelay: `${i * 0.03}s` }}>
                                                                    <MapPin size={12} />
                                                                    {ent.text}
                                                                    <span className="entity-count">×{ent.count}</span>
                                                                </div>
                                                            ))}
                                                        </div>
                                                    </>
                                                )}

                                                {entities.grouped.MONEY && entities.grouped.MONEY.length > 0 && (
                                                    <>
                                                        <div className="entity-section-title"><DollarSign size={14} /> Financial Amounts</div>
                                                        <div className="entity-cloud">
                                                            {entities.grouped.MONEY.map((ent, i) => (
                                                                <div key={i} className="entity-chip entity-MONEY" style={{ animationDelay: `${i * 0.03}s` }}>
                                                                    <DollarSign size={12} />
                                                                    {ent.text}
                                                                    <span className="entity-count">×{ent.count}</span>
                                                                </div>
                                                            ))}
                                                        </div>
                                                    </>
                                                )}

                                                {entities.grouped.OTHER && entities.grouped.OTHER.length > 0 && (
                                                    <>
                                                        <div className="entity-section-title"><Sparkles size={14} /> Other Entities</div>
                                                        <div className="entity-cloud">
                                                            {entities.grouped.OTHER.map((ent, i) => (
                                                                <div key={i} className="entity-chip entity-OTHER" style={{ animationDelay: `${i * 0.03}s` }}>
                                                                    <Sparkles size={12} />
                                                                    {ent.text}
                                                                    <span className="entity-count">×{ent.count}</span>
                                                                </div>
                                                            ))}
                                                        </div>
                                                    </>
                                                )}
                                            </>
                                        ) : (
                                            <div className="empty-state">
                                                <div className="empty-state-icon">🧠</div>
                                                <div className="empty-state-text">Run the pipeline to extract entities with AI</div>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}

                            {/* ═══════════════════════════════════════════════
                            TAB: ANALYTICS (Pro Dashboards)
                           ═══════════════════════════════════════════════ */}
                            {activeTab === 'analytics' && (
                                <div className="main-content">
                                    <div className="section glass-panel">
                                        <div className="section-title">
                                            <BarChart2 size={18} color="var(--accent-cyan)" />
                                            Sentiment Dynamics
                                        </div>
                                        <div style={{ height: '300px', width: '100%' }}>
                                            <ResponsiveContainer width="100%" height="100%">
                                                <AreaChart data={[
                                                    { name: 'Prev', positive: metrics.sentiment_distribution.Positive * 0.8, negative: metrics.sentiment_distribution.Negative * 0.9 },
                                                    { name: 'Current', positive: metrics.sentiment_distribution.Positive, negative: metrics.sentiment_distribution.Negative }
                                                ]}>
                                                    <defs>
                                                        <linearGradient id="pos" x1="0" y1="0" x2="0" y2="1">
                                                            <stop offset="5%" stopColor="var(--positive)" stopOpacity={0.3} />
                                                            <stop offset="95%" stopColor="var(--positive)" stopOpacity={0} />
                                                        </linearGradient>
                                                        <linearGradient id="neg" x1="0" y1="0" x2="0" y2="1">
                                                            <stop offset="5%" stopColor="var(--negative)" stopOpacity={0.3} />
                                                            <stop offset="95%" stopColor="var(--negative)" stopOpacity={0} />
                                                        </linearGradient>
                                                    </defs>
                                                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                                                    <XAxis dataKey="name" stroke="var(--text-muted)" fontSize={10} />
                                                    <YAxis stroke="var(--text-muted)" fontSize={10} />
                                                    <Tooltip contentStyle={{ background: '#0c0c1a', border: '1px solid var(--glass-border)' }} />
                                                    <Area type="monotone" dataKey="positive" stroke="var(--positive)" fillOpacity={1} fill="url(#pos)" />
                                                    <Area type="monotone" dataKey="negative" stroke="var(--negative)" fillOpacity={1} fill="url(#neg)" />
                                                </AreaChart>
                                            </ResponsiveContainer>
                                        </div>
                                        <div className="analytics-insight">
                                            The intelligence matrix shows a <strong>{((metrics.sentiment_distribution.Positive / (metrics.article_count || 1)) * 100).toFixed(1)}%</strong> overall positive density across recent signals.
                                        </div>
                                    </div>

                                    <div className="section glass-panel">
                                        <div className="section-title">
                                            <PieChartIcon size={18} color="var(--accent-purple)" />
                                            Intelligence Domain Distribution
                                        </div>
                                        <div style={{ height: '300px', width: '100%' }}>
                                            <ResponsiveContainer width="100%" height="100%">
                                                <ReBarChart data={impacts.slice(0, 10)}>
                                                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
                                                    <XAxis dataKey="sector" stroke="var(--text-muted)" fontSize={8} interval={0} angle={-30} textAnchor="end" height={60} />
                                                    <YAxis stroke="var(--text-muted)" fontSize={10} />
                                                    <Tooltip contentStyle={{ background: '#0c0c1a', border: '1px solid var(--glass-border)' }} />
                                                    <Bar dataKey="total" radius={[4, 4, 0, 0]}>
                                                        {impacts.slice(0, 10).map((entry, index) => (
                                                            <Cell key={`cell-${index}`} fill={index % 2 === 0 ? 'var(--accent-purple)' : 'var(--accent-blue)'} />
                                                        ))}
                                                    </Bar>
                                                </ReBarChart>
                                            </ResponsiveContainer>
                                        </div>
                                    </div>
                                </div>
                            )}

                        </>
                    )}
                </div>
            )}
        </>
    );
};

// ═══════════════════════════════════════════════════════════════
// MAIN APP ROUTER
// ═══════════════════════════════════════════════════════════════
function App() {
    return (
        <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
    );
}

export default App;
