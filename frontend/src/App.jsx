import React, { useState, useEffect, useRef } from 'react';
import {
    Activity, BarChart2, Globe, Layers, ThumbsUp, ThumbsDown, Minus,
    Link as LinkIcon, FileText, ChevronDown, ChevronUp, TrendingUp, TrendingDown,
    AlertTriangle, Zap, Brain, Users, Building, MapPin, DollarSign,
    Search, Eye, Shield, Cpu, Sparkles, ExternalLink, Newspaper, PieChart as PieChartIcon,
    RefreshCw, Clock, ArrowUpRight, Filter, Star, X
} from 'lucide-react';
import { Toaster, toast } from 'react-hot-toast';
import {
    ResponsiveContainer, AreaChart, Area, XAxis, YAxis, CartesianGrid,
    Tooltip, BarChart as ReBarChart, Bar, Cell, PieChart as RePieChart, Pie
} from 'recharts';
import { Routes, Route, Link as RouterLink } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import LandingPage from './LandingPage';
import { supabase } from './supabaseClient';
import './App.css';
import Logo from './Logo.jpeg';

const API_BASE = '/api';

// ── Error Boundary ────────────────────────────────────────────
class ErrorBoundary extends React.Component {
    constructor(props) { super(props); this.state = { hasError: false }; }
    static getDerivedStateFromError() { return { hasError: true }; }
    render() {
        if (this.state.hasError) return (
            <div className="app-container loading-container overlay-ui">
                <div className="loading-text">Intelligence Interface Degraded. Please reload.</div>
            </div>
        );
        return this.props.children;
    }
}

// ═══════════════════════════════════════════════════════════════
// DASHBOARD COMPONENT (Light Premium SaaS Theme)
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
    // Supabase search state
    const [supabaseResults, setSupabaseResults] = useState([]);
    const [isSearchingSupabase, setIsSearchingSupabase] = useState(false);
    const prevArticleCount = useRef(0);
    const searchTimeout = useRef(null);

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
                if (prevArticleCount.current > 0 && data.article_count > prevArticleCount.current) {
                    const diff = data.article_count - prevArticleCount.current;
                    toast.success(`Ingested ${diff} new intelligence signals`, {
                        icon: '📡',
                        style: {
                            background: '#ffffff', color: '#0a0f1e',
                            border: '1px solid rgba(99,102,241,0.2)',
                            fontSize: '0.85rem', fontWeight: '600'
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

    // ── Supabase Search (past fetched news) ────────────────────
    const searchSupabase = async (query) => {
        if (!query || query.length < 3) {
            setSupabaseResults([]);
            return;
        }
        setIsSearchingSupabase(true);
        try {
            const { data, error: sbError } = await supabase
                .from('articles')
                .select('*')
                .or(`title.ilike.%${query}%,description.ilike.%${query}%,source.ilike.%${query}%`)
                .order('id', { ascending: false })
                .limit(50);
            if (sbError) throw sbError;
            setSupabaseResults(data || []);
        } catch (err) {
            console.error('Supabase search error:', err);
            // Fallback to API search
            setSupabaseResults([]);
        } finally {
            setIsSearchingSupabase(false);
        }
    };

    const handleGlobalSearch = (e) => {
        const val = e.target.value;
        setGlobalSearch(val);
        // Debounced Supabase search
        if (searchTimeout.current) clearTimeout(searchTimeout.current);
        searchTimeout.current = setTimeout(() => searchSupabase(val), 400);
    };

    const clearSearch = () => {
        setGlobalSearch('');
        setSupabaseResults([]);
    };

    const fetchSectorNews = async (sector) => {
        if (!sector) { setSectorNews([]); return; }
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
        if (val.length > 2) fetchSectorNews(val);
        else setSectorNews([]);
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 30000);
        return () => clearInterval(interval);
    }, []);

    useEffect(() => {
        const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws';
        const wsUrl = `${protocol}://${window.location.host}/ws`;
        const ws = new WebSocket(wsUrl);
        ws.onopen = () => console.log("WS connected");
        ws.onmessage = (evt) => {
            try {
                const data = JSON.parse(evt.data);
                setSystemStatus(prev => ({ ...prev, ...data }));
            } catch (e) { console.warn("WS parse error", e); }
        };
        ws.onclose = () => console.log("WS closed");
        return () => ws.close();
    }, []);

    // ── Filter logic ──────────────────────────────────────────
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
    const totalSentiment = totalPositive + totalNegative + totalNeutral;
    const isBullish = totalPositive > totalNegative;
    const stabilityScore = metrics?.article_count > 0 ? ((totalPositive / metrics.article_count) * 100).toFixed(1) : '--';
    const moodColor = isBullish ? '#059669' : '#dc2626';

    // ── Computed Analytics Data ──────────────────────────────
    const sentimentPieData = [
        { name: 'Positive', value: totalPositive, fill: '#059669' },
        { name: 'Negative', value: totalNegative, fill: '#dc2626' },
        { name: 'Neutral', value: totalNeutral, fill: '#d97706' },
    ].filter(d => d.value > 0);

    // Source distribution (top 10 sources)
    const sourceMap = {};
    (articlesList || []).forEach(art => {
        const src = art.source || 'Unknown';
        sourceMap[src] = (sourceMap[src] || 0) + 1;
    });
    const sourceDistData = Object.entries(sourceMap)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 10)
        .map(([name, count]) => ({ name, count }));

    // Fake news stats
    const fakeCount = (articlesList || []).filter(a => a.fake_news_label === 'Fake').length;
    const realCount = (articlesList || []).filter(a => a.fake_news_label !== 'Fake').length;
    const fakeNewsPieData = [
        { name: 'Verified', value: realCount, fill: '#059669' },
        { name: 'Flagged', value: fakeCount, fill: '#dc2626' },
    ].filter(d => d.value > 0);

    // Entity type counts
    const entityGrouped = entities?.grouped || {};
    const entityTypeData = Object.entries(entityGrouped)
        .map(([type, items]) => ({ type, count: items?.length || 0 }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 8);

    // Unique source count
    const uniqueSources = Object.keys(sourceMap).length;

    // Domain/category diversity
    const activeSectors = (impacts || []).length;

    const tabs = [
        { id: 'overview', label: 'Overview', icon: <Eye size={15} /> },
        { id: 'events', label: 'Live Events', icon: <Zap size={15} />, badge: filteredEvents.length },
        { id: 'sectors', label: 'Sector Intel', icon: <Activity size={15} />, badge: filteredImpacts.length },
        { id: 'articles', label: 'News Feed', icon: <Newspaper size={15} />, badge: filteredArticles.length },
        { id: 'intel', label: 'Intel & Entities', icon: <Brain size={15} />, badge: (entities?.entities || []).length },
        { id: 'analytics', label: 'Analytics', icon: <BarChart2 size={15} /> },
    ];

    const entityIcon = (label) => {
        switch (label) {
            case 'ORG': return <Building size={14} />;
            case 'PERSON': return <Users size={14} />;
            case 'GPE': case 'LOC': return <MapPin size={14} />;
            case 'MONEY': return <DollarSign size={14} />;
            default: return <Sparkles size={14} />;
        }
    };

    // Use supabase results when searching, otherwise use API results
    const displayArticles = globalSearch.length >= 3 && supabaseResults.length > 0
        ? supabaseResults
        : filteredArticles;

    return (
        <ErrorBoundary>
            {/* Soft ambient background complementing the light theme */}
            <div className="dashboard-bg"></div>

            <Toaster position="bottom-right" />

            {loading ? (
                <div className="dribbble-loader-wrapper overlay-ui">
                    <div className="hud-loader-container">
                        <div className="hud-ring-outer"></div>
                        <div className="hud-ring-middle"></div>
                        <div className="hud-ring-inner">
                            <div className="hud-core-dot"></div>
                        </div>
                        <div className="hud-crosshair-x"></div>
                        <div className="hud-crosshair-y"></div>
                    </div>
                    <div className="loading-text">VEILORACLE</div>
                    <div className="loading-subtext">INITIALIZING CORE...</div>
                </div>
            ) : (
                <div className="app-container overlay-ui">
                    {/* ═══ HEADER ═══ */}
                    <header className="header">
                        <RouterLink to="/" className="title-container" title="Return to Landing Page" style={{ flexDirection: 'row', alignItems: 'center', gap: '12px' }}>
                            <img src={Logo} alt="VeilOracle Logo" style={{ width: 34, height: 34, borderRadius: '50%', objectFit: 'cover' }} />
                            <div>
                                <div className="oracle-title">VEILORACLE</div>
                                <div className="oracle-subtitle">AI Global Intelligence Network</div>
                            </div>
                        </RouterLink>
                        <div className="header-actions">
                            <div className="search-box">
                                <Search className="search-icon" size={16} color="var(--text-muted)" />
                                <input
                                    type="text"
                                    placeholder="Search news, sectors, events..."
                                    value={globalSearch}
                                    onChange={handleGlobalSearch}
                                />
                                {globalSearch && (
                                    <button onClick={clearSearch} style={{ background: 'none', border: 'none', cursor: 'pointer', padding: 0 }}>
                                        <X size={16} color="var(--text-muted)" />
                                    </button>
                                )}
                                {isSearchingSupabase && (
                                    <RefreshCw size={14} color="var(--accent-indigo)" style={{ animation: 'spin 1s linear infinite' }} />
                                )}
                            </div>
                            <div className="status-container">
                                <div className="status-indicator">
                                    <span className={`status-dot ${isLive ? 'status-live' : 'status-offline'}`}></span>
                                    <span className="status-text">{isLive ? 'LIVE' : 'OFFLINE'}</span>
                                </div>
                                <div className="update-time">
                                    {systemStatus.last_update ? new Date(systemStatus.last_update).toLocaleTimeString() : '--:--:--'}
                                </div>
                            </div>
                        </div>
                    </header>

                    {error ? (
                        <div className="error-banner">⚠️ {error}</div>
                    ) : (
                        <>
                            {/* ═══ Supabase Search Results Overlay ═══ */}
                            {globalSearch.length >= 3 && supabaseResults.length > 0 && (
                                <motion.div
                                    initial={{ opacity: 0, y: -10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    className="glass-panel"
                                    style={{ padding: '24px', marginBottom: '24px' }}
                                >
                                    <div className="section-title">
                                        <div className="section-title-icon"><Search size={16} /></div>
                                        Search Results from Archive
                                        <span className="section-title-count">({supabaseResults.length} found globally)</span>
                                    </div>
                                    <div className="events-list" style={{ maxHeight: '360px' }}>
                                        {supabaseResults.map((art, i) => (
                                            <a
                                                key={`sb-${art.id || i}`}
                                                className="article-feed-card glass-card"
                                                href={art.url || '#'}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                onClick={(e) => {
                                                    if (!art.url || !art.url.startsWith('http')) {
                                                        e.preventDefault();
                                                    }
                                                }}
                                            >
                                                <div className="article-feed-main">
                                                    <div className="article-feed-title">
                                                        <FileText size={16} color="var(--text-muted)" style={{ flexShrink: 0, marginTop: 4 }} />
                                                        {art.title}
                                                    </div>
                                                    <div className="article-feed-meta">
                                                        <span className="article-source-badge">{art.source}</span>
                                                        <span className={`badge badge-${(art.sentiment_label || 'neutral').toLowerCase()}`}>
                                                            {art.sentiment_label}
                                                        </span>
                                                        {art.published_at && (
                                                            <span style={{ fontSize: 'var(--font-xs)', color: 'var(--text-muted)', fontWeight: '600' }}>
                                                                {new Date(art.published_at).toLocaleDateString()}
                                                            </span>
                                                        )}
                                                    </div>
                                                </div>
                                                <ExternalLink size={16} color="var(--accent-indigo)" style={{ flexShrink: 0 }} />
                                            </a>
                                        ))}
                                    </div>
                                </motion.div>
                            )}

                            {/* ═══ Intelligence Overview ═══ */}
                            <div className="intelligence-overview">
                                <div className="overview-main glass-panel">
                                    <div className="stability-core">
                                        <div className="stability-meter">
                                            <svg viewBox="0 0 100 100" width="100%" height="100%">
                                                <circle cx="50" cy="50" r="42" fill="none" stroke="rgba(0,0,0,0.05)" strokeWidth="6" />
                                                <circle cx="50" cy="50" r="42" fill="none" stroke="var(--accent-indigo)" strokeWidth="6"
                                                    strokeDasharray={`${(stabilityScore === '--' ? 0 : stabilityScore) * 2.64} 264`}
                                                    strokeLinecap="round" transform="rotate(-90 50 50)" />
                                            </svg>
                                            <div className="stability-value">
                                                <span>{stabilityScore}%</span>
                                                <small>STABILITY</small>
                                            </div>
                                        </div>
                                        <div className="stability-info">
                                            <div className="briefing-tag">GLOBAL INTELLIGENCE STATUS</div>
                                            <div className="briefing-title">Neural Matrix: {isBullish ? 'Bullish' : 'Bearish'}</div>
                                            <div className="briefing-text">
                                                Analyzing <strong>{metrics.article_count.toLocaleString()}</strong> signals across global domains.
                                                Market sentiment is {isBullish ? 'predominantly positive' : 'trending negative'} over the recent interval.
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div className="overview-stats">
                                    <div className="stat-box glass-panel">
                                        <div className="stat-box-icon"><Globe size={18} /></div>
                                        <div className="stat-data">
                                            <div className="stat-val">{metrics.article_count.toLocaleString()}</div>
                                            <div className="stat-lbl">Signals Ingested</div>
                                        </div>
                                    </div>
                                    <div className="stat-box glass-panel">
                                        <div className="stat-box-icon"><Zap size={18} /></div>
                                        <div className="stat-data">
                                            <div className="stat-val">{metrics.event_count.toLocaleString()}</div>
                                            <div className="stat-lbl">Clusters Detected</div>
                                        </div>
                                    </div>
                                    <div className="stat-box glass-panel">
                                        <div className="stat-box-icon" style={{ color: 'var(--positive)', background: 'rgba(5,150,105,0.1)' }}>
                                            <TrendingUp size={18} />
                                        </div>
                                        <div className="stat-data">
                                            <div className="stat-val">{trends.rising?.length || 0}</div>
                                            <div className="stat-lbl">Rising Domains</div>
                                        </div>
                                    </div>
                                    <div className="stat-box glass-panel">
                                        <div className="stat-box-icon" style={{ color: 'var(--negative)', background: 'rgba(220,38,38,0.1)' }}>
                                            <AlertTriangle size={18} />
                                        </div>
                                        <div className="stat-data">
                                            <div className="stat-val">{anomalies.critical_count || 0}</div>
                                            <div className="stat-lbl">Critical Risks</div>
                                        </div>
                                    </div>
                                    <div className="stat-box glass-panel">
                                        <div className="stat-box-icon" style={{ color: 'var(--accent-cyan)', background: 'rgba(6,182,212,0.1)' }}>
                                            <Layers size={18} />
                                        </div>
                                        <div className="stat-data">
                                            <div className="stat-val">{uniqueSources}</div>
                                            <div className="stat-lbl">Active Sources</div>
                                        </div>
                                    </div>
                                    <div className="stat-box glass-panel">
                                        <div className="stat-box-icon" style={{ color: 'var(--accent-purple)', background: 'rgba(139,92,246,0.1)' }}>
                                            <Shield size={18} />
                                        </div>
                                        <div className="stat-data">
                                            <div className="stat-val">{activeSectors}</div>
                                            <div className="stat-lbl">Sectors Tracked</div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                            {/* ═══ Tab Navigation ═══ */}
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

                            {/* ═══ TAB: OVERVIEW ═══ */}
                            {activeTab === 'overview' && (
                                <div className="main-content">
                                    <div className="section">
                                        <div className="section-title">
                                            <div className="section-title-icon"><TrendingUp size={16} /></div>
                                            Domain Trends
                                        </div>
                                        <div className="shift-grid">
                                            {trends.rising?.slice(0, 4).map((t, i) => (
                                                <div key={i} className="shift-card glass-card">
                                                    <div className="shift-header">
                                                        <span className="shift-sector" title={t.sector}>{t.sector}</span>
                                                        <span className="shift-momentum rising">↑ {t.momentum?.toFixed(1)}</span>
                                                    </div>
                                                    <div className="shift-bar"><div className="shift-fill positive" style={{ width: `${(t.confidence || 0.5) * 100}%` }}></div></div>
                                                    <div className="shift-footer">CONFIDENCE: {((t.confidence || 0.5) * 100).toFixed(0)}%</div>
                                                </div>
                                            ))}
                                            {trends.falling?.slice(0, 4).map((t, i) => (
                                                <div key={`f-${i}`} className="shift-card glass-card">
                                                    <div className="shift-header">
                                                        <span className="shift-sector" title={t.sector}>{t.sector}</span>
                                                        <span className="shift-momentum falling">↓ {Math.abs(t.momentum?.toFixed(1) || t.momentum)}</span>
                                                    </div>
                                                    <div className="shift-bar"><div className="shift-fill negative" style={{ width: `${(t.confidence || 0.5) * 100}%` }}></div></div>
                                                    <div className="shift-footer">RISK: {((t.confidence || 0.5) * 100).toFixed(0)}%</div>
                                                </div>
                                            ))}
                                        </div>
                                    </div>

                                    <div className="section">
                                        <div className="section-title">
                                            <div className="section-title-icon"><AlertTriangle size={16} color="var(--accent-purple)" /></div>
                                            Global Anomaly Radar
                                        </div>
                                        <div className="impact-grid virtualized-scroll" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                                            {anomalies?.anomalies?.slice(0, 3).map((anomaly, i) => (
                                                <div key={i} className={`shift-card glass-card`} style={{ borderLeft: `3px solid ${anomaly.severity === 'Critical' ? '#ec4899' : '#f59e0b'}`, padding: '10px 14px' }}>
                                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '4px' }}>
                                                        <span style={{ fontFamily: 'Syne, sans-serif', fontWeight: 700, fontSize: '0.9rem', color: 'var(--text-primary)' }}>{anomaly.sector}</span>
                                                        <span className={`badge`} style={{ background: anomaly.severity === 'Critical' ? 'rgba(236, 72, 153, 0.1)' : 'rgba(245, 158, 11, 0.1)', color: anomaly.severity === 'Critical' ? '#ec4899' : '#f59e0b', fontSize: '0.7rem' }}>
                                                            {anomaly.severity.toUpperCase()}
                                                        </span>
                                                    </div>
                                                    <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                                                        {anomaly.reason} (Z-Score: {anomaly.z_score?.toFixed(2)})
                                                    </div>
                                                </div>
                                            ))}
                                            {(!anomalies?.anomalies || anomalies.anomalies.length === 0) && (
                                                <div className="empty-state glass-panel" style={{ minHeight: '120px', padding: '1rem', background: 'rgba(16, 185, 129, 0.05)' }}>
                                                    <Shield size={24} color="#10b981" style={{ marginBottom: '8px' }} />
                                                    <div style={{ fontFamily: 'Syne, sans-serif', fontWeight: '600', color: '#10b981', fontSize: '0.9rem' }}>All Neural Pathways Stable</div>
                                                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>No critical sector velocity spikes detected.</div>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* ═══ TAB: LIVE EVENTS ═══ */}
                            {activeTab === 'events' && (
                                <div className="main-content single-column">
                                    <div className="smart-event-list">
                                        {filteredEvents.length > 0 ? filteredEvents.map((ev, i) => (
                                            <div key={i} className={`smart-event-card glass-card ${expandedEvent === i ? 'expanded' : ''}`} onClick={() => setExpandedEvent(expandedEvent === i ? null : i)}>
                                                <div className="event-meta">
                                                    <div className="event-score" style={{ borderLeftColor: ev.sentiment_label === 'Positive' ? 'var(--positive)' : ev.sentiment_label === 'Negative' ? 'var(--negative)' : 'var(--neutral)' }}>
                                                        <div className="score-val">{ev.importance_score?.toFixed(0) || 50}</div>
                                                        <div className="score-lbl">Impact</div>
                                                    </div>
                                                    <div className="event-body">
                                                        <div className="event-title">{ev.label}</div>
                                                        <div className="event-footer">
                                                            <span className={`badge badge-${(ev.sentiment_label || 'neutral').toLowerCase()}`}>{ev.sentiment_label}</span>
                                                            <span className="badge" style={{ background: 'rgba(99,102,241,0.06)', color: 'var(--accent-indigo)', border: '1px solid rgba(99,102,241,0.1)' }}>
                                                                {(ev.lifecycle || 'emerging').toUpperCase()}
                                                            </span>
                                                            {ev.size > 1 && <span style={{ fontSize: 'var(--font-xs)', color: 'var(--text-muted)' }}>{ev.size} signals</span>}
                                                        </div>
                                                    </div>
                                                    <div className="event-chevron">
                                                        {expandedEvent === i ? <ChevronUp size={18} /> : <ChevronDown size={18} />}
                                                    </div>
                                                </div>
                                                {expandedEvent === i && (
                                                    <div className="event-expanded-content">
                                                        <div className="event-briefing glass-card">
                                                            <div className="briefing-header"><Sparkles size={14} /> AI Intelligence Brief</div>
                                                            <div className="briefing-text" style={{ fontSize: '0.9rem', color: 'var(--text-secondary)' }}>{ev.ai_summary || "Analyzing intelligence vectors for this event cluster..."}</div>
                                                        </div>
                                                        <div style={{ padding: '0 8px' }}>
                                                            {ev.articles && ev.articles.slice(0, 8).map((art, j) => (
                                                                <a
                                                                    key={j}
                                                                    href={art.url || '#'}
                                                                    target="_blank"
                                                                    rel="noopener noreferrer"
                                                                    className="article-link-item"
                                                                    onClick={(e) => {
                                                                        e.stopPropagation();
                                                                        if (!art.url || !art.url.startsWith('http')) e.preventDefault();
                                                                    }}
                                                                >
                                                                    <span className="title">{art.title}</span>
                                                                    <span className="source-meta">
                                                                        {art.source && <span>{art.source}</span>}
                                                                        <ExternalLink size={12} color="var(--accent-indigo)" />
                                                                    </span>
                                                                </a>
                                                            ))}
                                                        </div>
                                                    </div>
                                                )}
                                            </div>
                                        )) : (
                                            <div className="empty-state glass-panel">
                                                <div className="empty-state-icon"><Activity /></div>
                                                <div className="empty-state-text">No event clusters detected. The system is actively monitoring global pipelines.</div>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            )}

                            {/* ═══ TAB: SECTORS ═══ */}
                            {activeTab === 'sectors' && (
                                <div className="main-content">
                                    <div className="section">
                                        <div className="section-title">
                                            <div className="section-title-icon"><Activity size={16} /></div>
                                            Sector Intelligence
                                            <span className="section-title-count">({impacts.length} sectors)</span>
                                        </div>
                                        <div className="search-box" style={{ width: '100%', marginBottom: '16px', background: 'rgba(0,0,0,0.02)' }}>
                                            <Search size={16} color="var(--text-muted)" />
                                            <input
                                                type="text" placeholder="Filter sectors..."
                                                value={sectorSearch}
                                                onChange={handleSectorSearch}
                                            />
                                        </div>
                                        <div className="impact-grid virtualized-scroll" style={{ maxHeight: 'calc(100vh - 420px)' }}>
                                            {filteredImpacts.slice(0, 120).map((imp, i) => {
                                                let arr = "→", cl = "impact-mixed";
                                                if (imp.direction === "Bullish") { arr = "↑"; cl = "impact-bullish"; }
                                                else if (imp.direction === "Bearish") { arr = "↓"; cl = "impact-bearish"; }
                                                return (
                                                    <div key={i} className="mini-cell glass-card" onClick={() => { setSectorSearch(imp.sector); fetchSectorNews(imp.sector); }}>
                                                        <div className={`impact-direction ${cl}`}>{arr}</div>
                                                        <div className="impact-sector" title={imp.sector}>{imp.sector}</div>
                                                        <div className="impact-stats">
                                                            <span className="up">▲{imp.bullish}</span> • <span className="down">▼{imp.bearish}</span>
                                                        </div>
                                                    </div>
                                                );
                                            })}
                                        </div>
                                    </div>

                                    <div className="section">
                                        <div className="section-title">
                                            <div className="section-title-icon"><Globe size={16} /></div>
                                            Sector News
                                            {sectorSearch && <span className="section-title-count" style={{ color: 'var(--accent-indigo)' }}>— {sectorSearch}</span>}
                                        </div>
                                        <div className="events-list">
                                            {isSearchingSector ? (
                                                <div className="loading-container" style={{ minHeight: '200px' }}>
                                                    <div className="loading-spinner" style={{ width: 32, height: 32 }}></div>
                                                </div>
                                            ) : sectorNews.length > 0 ? sectorNews.map((art, i) => (
                                                <a
                                                    key={art.id || i}
                                                    className="article-feed-card glass-card"
                                                    href={art.url || '#'}
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                    onClick={(e) => { if (!art.url || !art.url.startsWith('http')) e.preventDefault(); }}
                                                >
                                                    <div className="article-feed-main">
                                                        <div className="article-feed-title">
                                                            <FileText size={16} color="var(--text-muted)" style={{ flexShrink: 0, marginTop: 2 }} />
                                                            {art.title}
                                                        </div>
                                                        <div className="article-feed-meta">
                                                            <span className="article-source-badge">{art.source}</span>
                                                            <span className={`badge badge-${(art.sentiment_label || 'neutral').toLowerCase()}`}>{art.sentiment_label}</span>
                                                            <span className={`badge ${art.fake_news_label === 'Fake' ? 'badge-negative' : 'badge-neutral'}`}>
                                                                {art.fake_news_label === 'Fake' ? '🚨 Flagged' : '✓ Verified'} ({(art.fake_news_score * 100 || 99).toFixed(0)}%)
                                                            </span>
                                                            {art.published_at && (
                                                                <span style={{ fontSize: 'var(--font-xs)', color: 'var(--text-muted)', fontWeight: '600' }}>
                                                                    {new Date(art.published_at).toLocaleDateString()}
                                                                </span>
                                                            )}
                                                        </div>
                                                    </div>
                                                    <ExternalLink size={18} color="var(--accent-indigo)" style={{ flexShrink: 0 }} className="external-link-icon" />
                                                </a>
                                            )) : (
                                                <div className="empty-state">
                                                    <div className="empty-state-icon"><Layers /></div>
                                                    <div className="empty-state-text">Select a sector to view related intelligence and analytics.</div>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* ═══ TAB: NEWS FEED ═══ */}
                            {activeTab === 'articles' && (
                                <div className="main-content single-column">
                                    {/* Top Picks */}
                                    {articlesList.length > 0 && !globalSearch && (
                                        <div className="section" style={{ minHeight: 'auto', marginBottom: '16px' }}>
                                            <div className="section-title">
                                                <div className="section-title-icon"><Star size={16} /></div>
                                                AI Top Picks
                                            </div>
                                            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '16px' }}>
                                                {[...articlesList]
                                                    .sort((a, b) => Math.abs(b.sentiment_score || 0) - Math.abs(a.sentiment_score || 0))
                                                    .slice(0, 3)
                                                    .map((art, i) => (
                                                        <a
                                                            key={`pick-${i}`}
                                                            href={art.url || '#'}
                                                            target="_blank"
                                                            rel="noopener noreferrer"
                                                            className="top-pick-card glass-card"
                                                            onClick={(e) => { if (!art.url || !art.url.startsWith('http')) e.preventDefault(); }}
                                                        >
                                                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                                                <span className="badge" style={{ background: 'rgba(99,102,241,0.06)', color: 'var(--accent-indigo)' }}>
                                                                    {['🔥 Trending Highlight', '💡 Strategic Insight', '📈 High Impact'][i]}
                                                                </span>
                                                                <ExternalLink size={14} color="var(--text-muted)" />
                                                            </div>
                                                            <div style={{ fontFamily: 'Outfit, sans-serif', fontSize: '1.15rem', fontWeight: '700', color: 'var(--text-primary)', lineHeight: '1.4' }}>{art.title}</div>
                                                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: 'auto' }}>
                                                                <span className={`badge badge-${(art.sentiment_label || '').toLowerCase()}`}>{art.sentiment_label}</span>
                                                                <span className="article-source-badge">{art.source}</span>
                                                            </div>
                                                        </a>
                                                    ))}
                                            </div>
                                        </div>
                                    )}

                                    {/* Full Feed */}
                                    <div className="section">
                                        <div className="section-title">
                                            <div className="section-title-icon"><Newspaper size={16} /></div>
                                            {globalSearch.length >= 3 ? `Search Results: "${globalSearch}"` : 'Live News Feed'}
                                            <span className="section-title-count">
                                                ({displayArticles.length} signals monitored)
                                            </span>
                                        </div>
                                        <div className="events-list">
                                            {displayArticles.length > 0 ? displayArticles.map((art, i) => (
                                                <a
                                                    key={art.id || i}
                                                    className="article-feed-card glass-card"
                                                    href={art.url || '#'}
                                                    target="_blank"
                                                    rel="noopener noreferrer"
                                                    onClick={(e) => { if (!art.url || !art.url.startsWith('http')) e.preventDefault(); }}
                                                >
                                                    <div className="article-feed-main">
                                                        <div className="article-feed-title">
                                                            <FileText size={16} color="var(--text-muted)" style={{ flexShrink: 0, marginTop: 2 }} />
                                                            {art.title}
                                                        </div>
                                                        <div className="article-feed-meta">
                                                            <span className="article-source-badge">{art.source}</span>
                                                            <span className={`badge badge-${(art.sentiment_label || 'neutral').toLowerCase()}`}>{art.sentiment_label}</span>
                                                            <span className={`badge ${art.fake_news_label === 'Fake' ? 'badge-negative' : 'badge-neutral'}`}>
                                                                {art.fake_news_label === 'Fake' ? '🚨 Flagged' : '✓ Verified'} ({(art.fake_news_score * 100).toFixed(0)}%)
                                                            </span>
                                                            {art.published_at && (
                                                                <span style={{ fontSize: 'var(--font-xs)', color: 'var(--text-muted)', fontWeight: '600' }}>
                                                                    {new Date(art.published_at).toLocaleDateString()}
                                                                </span>
                                                            )}
                                                        </div>
                                                    </div>
                                                    <ExternalLink size={18} color="var(--accent-indigo)" style={{ flexShrink: 0 }} />
                                                </a>
                                            )) : (
                                                <div className="empty-state">
                                                    <div className="empty-state-icon"><Newspaper /></div>
                                                    <div className="empty-state-text">
                                                        {globalSearch ? `No intelligence found for "${globalSearch}" in the global database.` : 'No signals ingested yet. System is awaiting pipeline execution.'}
                                                    </div>
                                                </div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* ═══ TAB: INTEL & ENTITIES ═══ */}
                            {activeTab === 'intel' && (
                                <div className="main-content">
                                    <div className="section">
                                        <div className="section-title">
                                            <div className="section-title-icon"><Users size={16} /></div>
                                            Named Entities Extracted
                                            <span className="section-title-count">({(entities?.entities || []).length} entities)</span>
                                        </div>
                                        <div className="events-list" style={{ maxHeight: 'calc(100vh - 380px)' }}>
                                            {(entities?.entities || []).length > 0 ? (entities.entities || []).slice(0, 60).map((ent, i) => (
                                                <div key={i} className="glass-card" style={{ padding: '14px 18px', display: 'flex', alignItems: 'center', gap: '14px' }}>
                                                    <div style={{ width: 36, height: 36, borderRadius: 10, display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'linear-gradient(135deg, rgba(99,102,241,0.1), rgba(6,182,212,0.08))', color: 'var(--accent-indigo)', flexShrink: 0 }}>
                                                        {entityIcon(ent.label)}
                                                    </div>
                                                    <div style={{ flex: 1 }}>
                                                        <div style={{ fontWeight: 700, fontSize: '1rem', color: 'var(--text-primary)' }}>{ent.text}</div>
                                                        <div style={{ fontSize: 'var(--font-xs)', color: 'var(--text-muted)', fontWeight: 600, textTransform: 'uppercase', marginTop: 2 }}>{ent.label} • {ent.count} mentions</div>
                                                    </div>
                                                    <span className="badge" style={{ background: 'rgba(99,102,241,0.06)', color: 'var(--accent-indigo)', border: '1px solid rgba(99,102,241,0.1)' }}>{ent.count}×</span>
                                                </div>
                                            )) : (
                                                <div className="empty-state"><div className="empty-state-icon"><Users /></div><div className="empty-state-text">No entities extracted yet. Run the pipeline to begin NER analysis.</div></div>
                                            )}
                                        </div>
                                    </div>
                                    <div className="section">
                                        <div className="section-title">
                                            <div className="section-title-icon"><AlertTriangle size={16} /></div>
                                            Anomaly Alerts
                                            <span className="section-title-count">({anomalies.critical_count || 0} critical, {anomalies.warning_count || 0} warnings)</span>
                                        </div>
                                        <div className="events-list" style={{ maxHeight: 'calc(100vh - 380px)' }}>
                                            {(anomalies?.anomalies || []).length > 0 ? (anomalies.anomalies || []).slice(0, 30).map((an, i) => (
                                                <div key={i} className="glass-card" style={{ padding: '16px 20px', borderLeft: `4px solid ${an.severity === 'critical' ? 'var(--negative)' : 'var(--warning)'}` }}>
                                                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 6 }}>
                                                        <span style={{ fontWeight: 700, fontSize: '1rem', color: 'var(--text-primary)' }}>{an.sector || an.metric || 'Unknown'}</span>
                                                        <span className={`badge ${an.severity === 'critical' ? 'badge-negative' : 'badge-neutral'}`}>{(an.severity || 'warning').toUpperCase()}</span>
                                                    </div>
                                                    <div style={{ fontSize: 'var(--font-sm)', color: 'var(--text-secondary)', lineHeight: 1.5 }}>{an.description || `Z-Score: ${an.z_score?.toFixed(2) || 'N/A'}`}</div>
                                                </div>
                                            )) : (
                                                <div className="empty-state"><div className="empty-state-icon"><Shield /></div><div className="empty-state-text">No anomalies detected. All signals within normal parameters.</div></div>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            )}

                            {/* ═══ TAB: ANALYTICS (REDESIGNED) ═══ */}
                            {activeTab === 'analytics' && (
                                <div className="analytics-dashboard">
                                    {/* Row 1: Sentiment & Verification (Donuts) */}
                                    <div className="analytics-row">
                                        <div className="section analytics-panel">
                                            <div className="section-title">
                                                <div className="section-title-icon"><PieChartIcon size={16} /></div>
                                                Global Sentiment Distribution
                                            </div>
                                            <div style={{ height: '260px', width: '100%', position: 'relative' }}>
                                                <ResponsiveContainer width="100%" height="100%">
                                                    <RePieChart>
                                                        <Pie data={sentimentPieData} cx="50%" cy="50%" innerRadius={70} outerRadius={100} paddingAngle={4} dataKey="value" stroke="none">
                                                            {sentimentPieData.map((entry, index) => <Cell key={`pie-${index}`} fill={entry.fill} />)}
                                                        </Pie>
                                                        <Tooltip contentStyle={{ background: '#fff', border: '1px solid rgba(0,0,0,0.08)', borderRadius: 12, boxShadow: 'var(--hover-shadow)' }} formatter={(value) => [`${value} Signals`, 'Volume']} />
                                                    </RePieChart>
                                                </ResponsiveContainer>
                                                <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', textAlign: 'center', pointerEvents: 'none' }}>
                                                    <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-primary)', fontFamily: 'Outfit, sans-serif' }}>{totalSentiment}</div>
                                                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>Total Rated</div>
                                                </div>
                                            </div>
                                            <div className="analytics-summary-row" style={{ borderTop: '1px solid rgba(0,0,0,0.05)', marginTop: '16px', paddingTop: '16px' }}>
                                                <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', width: '100%', flexWrap: 'wrap' }}>
                                                    {sentimentPieData.map(d => (
                                                        <div key={d.name} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                                                            <div style={{ width: 10, height: 10, borderRadius: '50%', backgroundColor: d.fill }}></div>
                                                            <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)' }}>{d.name}: <strong style={{ color: 'var(--text-primary)' }}>{d.value}</strong></span>
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        </div>

                                        <div className="section analytics-panel">
                                            <div className="section-title">
                                                <div className="section-title-icon"><Shield size={16} /></div>
                                                Intelligence Verification
                                            </div>
                                            <div style={{ height: '260px', width: '100%', position: 'relative' }}>
                                                <ResponsiveContainer width="100%" height="100%">
                                                    <RePieChart>
                                                        <Pie data={fakeNewsPieData} cx="50%" cy="50%" innerRadius={70} outerRadius={100} paddingAngle={4} dataKey="value" stroke="none">
                                                            {fakeNewsPieData.map((entry, index) => <Cell key={`fn-${index}`} fill={entry.fill} />)}
                                                        </Pie>
                                                        <Tooltip contentStyle={{ background: '#fff', border: '1px solid rgba(0,0,0,0.08)', borderRadius: 12, boxShadow: 'var(--hover-shadow)' }} formatter={(value) => [`${value} Signals`, 'Count']} />
                                                    </RePieChart>
                                                </ResponsiveContainer>
                                                <div style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)', textAlign: 'center', pointerEvents: 'none' }}>
                                                    <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--text-primary)', fontFamily: 'Outfit, sans-serif' }}>{(((realCount)/(fakeCount + realCount || 1)) * 100).toFixed(1)}%</div>
                                                    <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 700, textTransform: 'uppercase' }}>Authenticity</div>
                                                </div>
                                            </div>
                                            <div className="analytics-summary-row" style={{ borderTop: '1px solid rgba(0,0,0,0.05)', marginTop: '16px', paddingTop: '16px' }}>
                                                <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', width: '100%', flexWrap: 'wrap' }}>
                                                    {fakeNewsPieData.map(d => (
                                                        <div key={d.name} style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
                                                            <div style={{ width: 10, height: 10, borderRadius: '50%', backgroundColor: d.fill }}></div>
                                                            <span style={{ fontSize: '0.85rem', fontWeight: 600, color: 'var(--text-secondary)' }}>{d.name}: <strong style={{ color: 'var(--text-primary)' }}>{d.value}</strong></span>
                                                        </div>
                                                    ))}
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    {/* Row 2: Real-Time Trajectory Map (Center) */}
                                    <div className="analytics-row single-column">
                                        <div className="section analytics-panel" style={{ width: '100%' }}>
                                            <div className="section-title">
                                                <div className="section-title-icon"><BarChart2 size={16} /></div>
                                                Real-Time Trajectory Map
                                            </div>
                                            <div style={{ height: '360px', width: '100%' }}>
                                                <ResponsiveContainer width="100%" height="100%">
                                                    <AreaChart data={[
                                                        { point: 'T-4', bullish: Math.round(totalPositive * 0.1), bearish: Math.round(totalNegative * 0.2), neutral: Math.round(totalNeutral * 0.1) },
                                                        { point: 'T-3', bullish: Math.round(totalPositive * 0.3), bearish: Math.round(totalNegative * 0.4), neutral: Math.round(totalNeutral * 0.3) },
                                                        { point: 'T-2', bullish: Math.round(totalPositive * 0.6), bearish: Math.round(totalNegative * 0.6), neutral: Math.round(totalNeutral * 0.5) },
                                                        { point: 'T-1', bullish: Math.round(totalPositive * 0.8), bearish: Math.round(totalNegative * 0.7), neutral: Math.round(totalNeutral * 0.8) },
                                                        { point: 'Live', bullish: totalPositive, bearish: totalNegative, neutral: totalNeutral },
                                                    ]} margin={{ top: 20, right: 20, left: 10, bottom: 20 }}>
                                                        <defs>
                                                            <linearGradient id="colorBull" x1="0" y1="0" x2="0" y2="1">
                                                                <stop offset="5%" stopColor="var(--positive)" stopOpacity={0.5}/>
                                                                <stop offset="95%" stopColor="var(--positive)" stopOpacity={0}/>
                                                            </linearGradient>
                                                            <linearGradient id="colorBear" x1="0" y1="0" x2="0" y2="1">
                                                                <stop offset="5%" stopColor="var(--negative)" stopOpacity={0.5}/>
                                                                <stop offset="95%" stopColor="var(--negative)" stopOpacity={0}/>
                                                            </linearGradient>
                                                            <linearGradient id="colorNet" x1="0" y1="0" x2="0" y2="1">
                                                                <stop offset="5%" stopColor="var(--neutral)" stopOpacity={0.5}/>
                                                                <stop offset="95%" stopColor="var(--neutral)" stopOpacity={0}/>
                                                            </linearGradient>
                                                        </defs>
                                                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.05)" vertical={false} />
                                                        <XAxis dataKey="point" stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} dy={10} />
                                                        <YAxis stroke="var(--text-muted)" fontSize={12} tickLine={false} axisLine={false} />
                                                        <Tooltip contentStyle={{ background: '#fff', border: '1px solid rgba(0,0,0,0.08)', borderRadius: 12, boxShadow: 'var(--hover-shadow)' }} />
                                                        <Area type="monotone" dataKey="bullish" stroke="var(--positive)" strokeWidth={3} fillOpacity={1} fill="url(#colorBull)" activeDot={{ r: 6 }} name="Positive Velocity" />
                                                        <Area type="monotone" dataKey="bearish" stroke="var(--negative)" strokeWidth={3} fillOpacity={1} fill="url(#colorBear)" activeDot={{ r: 6 }} name="Negative Velocity" />
                                                        <Area type="monotone" dataKey="neutral" stroke="var(--neutral)" strokeWidth={3} fillOpacity={1} fill="url(#colorNet)" activeDot={{ r: 6 }} name="Neutral Baseline" />
                                                    </AreaChart>
                                                </ResponsiveContainer>
                                            </div>
                                            <div className="analytics-insight-bar" style={{ marginTop: '16px', background: 'rgba(0,0,0,0.02)' }}>
                                                <strong>AI Velocity Insight:</strong> {isBullish ? 'Bullish momentum is overriding downward bearish trends' : 'Bearish forces are currently surpassing positive recovery phases'} across analyzed epochs. Peak event density recorded at <strong>{metrics.article_count.toLocaleString()}</strong> signals.
                                            </div>
                                        </div>
                                    </div>

                                    {/* Row 3: Categorical Data (Horizontal Bars) */}
                                    <div className="analytics-row">
                                        <div className="section analytics-panel">
                                            <div className="section-title">
                                                <div className="section-title-icon"><Newspaper size={16} /></div>
                                                Source Volume Distribution
                                            </div>
                                            <div style={{ height: '320px', width: '100%' }}>
                                                <ResponsiveContainer width="100%" height="100%">
                                                    <ReBarChart data={sourceDistData} layout="vertical" margin={{ top: 10, right: 30, left: 10, bottom: 5 }}>
                                                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.05)" horizontal={true} vertical={false} />
                                                        <XAxis type="number" stroke="var(--text-muted)" fontSize={11} tickLine={false} axisLine={false} />
                                                        <YAxis dataKey="name" type="category" stroke="var(--text-primary)" fontSize={11} tickLine={false} axisLine={false} width={100} fontWeight={600} />
                                                        <Tooltip cursor={{ fill: 'rgba(99,102,241,0.05)' }} contentStyle={{ background: '#fff', border: '1px solid rgba(0,0,0,0.08)', borderRadius: 12, boxShadow: 'var(--hover-shadow)' }} />
                                                        <Bar dataKey="count" radius={[0, 4, 4, 0]} barSize={20}>
                                                            {sourceDistData.map((entry, index) => <Cell key={`cell-${index}`} fill={`hsl(234, 89%, ${60 + (index * 4)}%)`} />)}
                                                        </Bar>
                                                    </ReBarChart>
                                                </ResponsiveContainer>
                                            </div>
                                        </div>

                                        <div className="section analytics-panel">
                                            <div className="section-title">
                                                <div className="section-title-icon"><Users size={16} /></div>
                                                Detected Entity Classification
                                            </div>
                                            <div style={{ height: '320px', width: '100%' }}>
                                                <ResponsiveContainer width="100%" height="100%">
                                                    <ReBarChart data={entityTypeData} layout="vertical" margin={{ top: 10, right: 30, left: 10, bottom: 5 }}>
                                                        <CartesianGrid strokeDasharray="3 3" stroke="rgba(0,0,0,0.05)" horizontal={true} vertical={false} />
                                                        <XAxis type="number" stroke="var(--text-muted)" fontSize={11} tickLine={false} axisLine={false} />
                                                        <YAxis dataKey="type" type="category" stroke="var(--text-primary)" fontSize={11} tickLine={false} axisLine={false} width={100} fontWeight={600} />
                                                        <Tooltip cursor={{ fill: 'rgba(99,102,241,0.05)' }} contentStyle={{ background: '#fff', border: '1px solid rgba(0,0,0,0.08)', borderRadius: 12, boxShadow: 'var(--hover-shadow)' }} />
                                                        <Bar dataKey="count" radius={[0, 4, 4, 0]} barSize={20}>
                                                            {entityTypeData.map((entry, index) => <Cell key={`ent-${index}`} fill={['#06b6d4', '#8b5cf6', '#6366f1', '#059669', '#d97706', '#dc2626', '#2563eb', '#ec4899'][index % 8]} />)}
                                                        </Bar>
                                                    </ReBarChart>
                                                </ResponsiveContainer>
                                            </div>
                                        </div>
                                    </div>
                                    
                                    {/* Row 4: Trending Anomalies & Forecast Highlights */}
                                    <div className="analytics-row">
                                        <div className="section analytics-panel">
                                            <div className="section-title">
                                                <div className="section-title-icon" style={{ background: 'rgba(5,150,105,0.1)', color: 'var(--positive)' }}><TrendingUp size={16} /></div>
                                                Emerging Sector Strengths
                                            </div>
                                            <div className="trend-cards-list">
                                                {(trends.rising || []).slice(0, 5).map((t, i) => (
                                                    <div key={`r-${i}`} className="glass-card" style={{ padding: '14px 18px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                                                        <div>
                                                            <div style={{ fontWeight: 700, color: 'var(--text-primary)', fontSize: '0.95rem' }}>{t.sector}</div>
                                                            <div style={{ fontSize: 'var(--font-xs)', color: 'var(--text-muted)', fontWeight: 600, marginTop: 2 }}>STABILITY: {((t.confidence || 0.5) * 100).toFixed(0)}%</div>
                                                        </div>
                                                        <span className="shift-momentum rising" style={{ fontSize: '1.05rem', background: 'rgba(5,150,105,0.1)', padding: '4px 10px', borderRadius: 8 }}>↑ {t.momentum?.toFixed(1)}</span>
                                                    </div>
                                                ))}
                                                {(trends.rising || []).length === 0 && <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)', fontWeight: 500 }}>Awaiting market shift data...</div>}
                                            </div>
                                        </div>
                                        
                                        <div className="section analytics-panel">
                                            <div className="section-title">
                                                <div className="section-title-icon" style={{ background: 'rgba(220,38,38,0.1)', color: 'var(--negative)' }}><TrendingDown size={16} /></div>
                                                Sector Vulnerabilities
                                            </div>
                                            <div className="trend-cards-list">
                                                {(trends.falling || []).slice(0, 5).map((t, i) => (
                                                    <div key={`f-${i}`} className="glass-card" style={{ padding: '14px 18px', display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '10px' }}>
                                                        <div>
                                                            <div style={{ fontWeight: 700, color: 'var(--text-primary)', fontSize: '0.95rem' }}>{t.sector}</div>
                                                            <div style={{ fontSize: 'var(--font-xs)', color: 'var(--text-muted)', fontWeight: 600, marginTop: 2 }}>RISK EXPOSURE: {((t.confidence || 0.5) * 100).toFixed(0)}%</div>
                                                        </div>
                                                        <span className="shift-momentum falling" style={{ fontSize: '1.05rem', background: 'rgba(220,38,38,0.1)', padding: '4px 10px', borderRadius: 8 }}>↓ {Math.abs(t.momentum || 0).toFixed(1)}</span>
                                                    </div>
                                                ))}
                                                {(trends.falling || []).length === 0 && <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-muted)', fontWeight: 500 }}>Awaiting risk detection data...</div>}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            )}
                        </>
                    )}
                </div>
            )}
        </ErrorBoundary>
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
