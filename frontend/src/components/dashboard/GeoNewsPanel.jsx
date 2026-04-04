import { useState, useMemo } from 'react';
import { Globe, MapPin, Map, Tag, ChevronRight, Activity, Zap, Server, Search } from 'lucide-react';
import { useGeoNews } from '../../hooks/useApi';
import './GeoNewsPanel.css';

const GeoNewsPanel = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchTrigger, setSearchTrigger] = useState(null);
  const { data, loading, error } = useGeoNews(searchTrigger, 10000);
  
  const [selectedCountry, setSelectedCountry] = useState(null);
  const [selectedState, setSelectedState] = useState(null);
  const [selectedDistrict, setSelectedDistrict] = useState(null);
  const [activeKeywords, setActiveKeywords] = useState([]);
  const [showAllKeywords, setShowAllKeywords] = useState(false);

  // Auto-select first active country if none selected
  if (data?.regions && Array.isArray(data.regions) && data.regions.length > 0 && !selectedCountry && !loading) {
    // If we're searching and have a global hub, use that. Otherwise use the first region with news.
    const autoSelectRegion = data.regions.find(r => r.news?.length > 0) || data.regions[0];
    setSelectedCountry(autoSelectRegion.id);
  }

  const handleSearch = (e) => {
    e.preventDefault();
    setSearchTrigger(searchQuery || null);
    setSelectedCountry(null);
    setSelectedState(null);
    setSelectedDistrict(null);
    setActiveKeywords([]);
  };

  const toggleKeyword = (kw) => {
    setActiveKeywords(prev => 
      prev.includes(kw) ? prev.filter(k => k !== kw) : [...prev, kw]
    );
  };

  const currentCountry = useMemo(() => 
    data?.regions?.find(r => r.id === selectedCountry),
  [data, selectedCountry]);

  const currentState = useMemo(() => 
    currentCountry?.states?.find(s => s.id === selectedState),
  [currentCountry, selectedState]);

  const currentDistrict = useMemo(() => 
    currentState?.districts?.find(d => d.id === selectedDistrict),
  [currentState, selectedDistrict]);

  // Aggregate news based on selection level with proper cascade fallback
  const displayedNews = useMemo(() => {
    let rawNews = [];

    if (currentDistrict) {
      // First try district-specific news
      rawNews = currentDistrict.news || [];
      // If no district-specific news, fall back to state news filtered by district keywords
      if (rawNews.length === 0 && currentState?.news?.length > 0) {
        const distKeywords = currentDistrict.keywords || [];
        rawNews = currentState.news.filter(n => {
          const text = ((n.title || '') + ' ' + (n.summary || '') + ' ' + (n.description || '')).toLowerCase();
          return distKeywords.some(kw => text.includes(kw));
        });
      }
      // Still empty? Fall back to all state-level news
      if (rawNews.length === 0 && currentState?.news?.length > 0) {
        rawNews = currentState.news;
      }
    } else if (currentState) {
      // First try state-specific news
      rawNews = currentState.news || [];
      // If no state-specific news, fall back to country news filtered by state keywords
      if (rawNews.length === 0 && currentCountry?.news?.length > 0) {
        const stateKeywords = currentState.keywords || [];
        rawNews = currentCountry.news.filter(n => {
          const text = ((n.title || '') + ' ' + (n.summary || '') + ' ' + (n.description || '')).toLowerCase();
          return stateKeywords.some(kw => text.includes(kw));
        });
      }
      // Still empty? Fall back to all country-level news
      if (rawNews.length === 0 && currentCountry?.news?.length > 0) {
        rawNews = currentCountry.news;
      }
    } else if (currentCountry) {
      rawNews = currentCountry.news || [];
    } else {
      rawNews = data?.regions?.flatMap(r => r.news || []) || [];
    }

    if (activeKeywords.length > 0) {
      const filtered = rawNews.filter(n => (n.keywords || []).some(k => activeKeywords.includes(k)));
      // If keyword filter yields nothing, show all news for the region instead of empty
      return filtered.length > 0 ? filtered : rawNews;
    }
    return rawNews;
  }, [currentCountry, currentState, currentDistrict, activeKeywords, data]);

  const groupedNews = useMemo(() => {
    const groups = {};
    displayedNews.forEach(news => {
      const cat = news.category || 'General';
      if (!groups[cat]) groups[cat] = [];
      groups[cat].push(news);
    });
    // Sort groups by the number of events (descending)
    return Object.fromEntries(
      Object.entries(groups).sort((a, b) => b[1].length - a[1].length)
    );
  }, [displayedNews]);

  if (loading && !data) {
    return (
      <div className="vo-geonews-loading">
        <Server className="vo-spinner" />
        <span>Initializing Geographic Neural Network...</span>
      </div>
    );
  }

  if (error) {
    return <div className="vo-error-state">Failed to load geographic nodes: {error}</div>;
  }

  return (
    <div className="vo-geonews-container">
      {/* Top Keywords Filter Rail */}
      <div className="vo-geonews-keywords-wrapper">
        <div className="vo-geonews-keywords-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%', flexWrap: 'wrap', gap: '0.75rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <Tag size={16} /> <span className="vo-section-title" style={{marginBottom: 0}}>Quick Filters</span>
          </div>
          <div style={{ display: 'flex', gap: '0.5rem', alignItems: 'center', flexWrap: 'wrap' }}>
            {activeKeywords.length > 0 && (
              <button 
                onClick={() => setActiveKeywords([])}
                style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.2)', color: '#ef4444', padding: '0.25rem 0.6rem', borderRadius: '4px', cursor: 'pointer', fontSize: '0.7rem', fontWeight: 600 }}
              >Clear ({activeKeywords.length})</button>
            )}
            <form onSubmit={handleSearch} style={{ display: 'flex', alignItems: 'center', background: 'rgba(255,255,255,0.05)', borderRadius: '6px', padding: '0.2rem 0.5rem', border: '1px solid var(--color-border)' }}>
              <Search size={14} style={{ color: 'var(--color-text-secondary)' }} />
              <input 
                type="text" 
                placeholder="Search intel..." 
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                style={{ background: 'transparent', border: 'none', color: 'var(--color-text)', padding: '0.3rem 0.6rem', outline: 'none', fontSize: '0.8rem', minWidth: '140px', maxWidth: '220px', width: '100%' }}
              />
              <button type="submit" style={{ background: '#52525B', border: 'none', color: '#fff', padding: '0.3rem 0.8rem', borderRadius: '4px', cursor: 'pointer', fontSize: '0.75rem', fontWeight: 600 }}>Scan</button>
            </form>
          </div>
        </div>
        <div className="vo-geonews-keywords-scroll">
          {(data?.keywords?.slice(0, 12) || []).map(kw => (
            <button 
              key={kw} 
              onClick={() => toggleKeyword(kw)}
              className={`vo-geonews-keyword-btn ${activeKeywords.includes(kw) ? 'active' : ''}`}
            >
              {kw}
            </button>
          ))}
        </div>
      </div>

      <div className="vo-geonews-layout">
        
        {/* Left Column: Countries */}
        <div className="vo-geonews-col vo-geonews-countries">
          <div className="vo-geonews-col-header">
            <Globe className="vo-geonews-col-icon" />
            <h3>Global Sectors</h3>
          </div>
          <div className="vo-geonews-list">
            {(data?.regions || []).map(region => {
              const newsCount = region.news?.length || 0;
              return (
                <div 
                  key={region.id}
                  onClick={() => {
                    setSelectedCountry(region.id);
                    setSelectedState(null);
                    setSelectedDistrict(null);
                    setActiveKeywords([]);
                  }}
                  className={`vo-geonews-card vo-geonews-3d-card ${selectedCountry === region.id ? 'active' : ''}`}
                >
                  <div className="vo-geonews-card-inner">
                    <span className="vo-geonews-card-title">{region.name}</span>
                    <div className="vo-geonews-card-meta">
                      <Zap size={12} className={newsCount > 0 ? "vo-geonews-pulse" : ""} style={{ opacity: newsCount > 0 ? 1 : 0.3 }} />
                      <span style={{ color: newsCount > 0 ? 'inherit' : 'var(--color-text-dim)' }}>
                        {newsCount} alerts
                      </span>
                    </div>
                  </div>
                  <ChevronRight className="vo-geonews-chevron" />
                  <div className="vo-geonews-card-glow" />
                </div>
              );
            })}
          </div>
        </div>

        {/* Middle Column: States & Districts */}
        <div className="vo-geonews-col vo-geonews-regions">
          <div className="vo-geonews-col-header">
            <Map className="vo-geonews-col-icon" />
            <h3>Regional Nodes</h3>
          </div>
          {currentCountry ? (
            <div className="vo-geonews-list">
              {currentCountry.states?.map(state => (
                <div key={state.id} className="vo-geonews-region-group">
                  <div 
                    onClick={() => {
                      setSelectedState(state.id === selectedState ? null : state.id);
                      setSelectedDistrict(null);
                    }}
                    className={`vo-geonews-card vo-geonews-state-card \${selectedState === state.id ? 'active' : ''}`}
                  >
                    <div className="vo-geonews-card-inner">
                      <span className="vo-geonews-card-title">{state.name}</span>
                      <span className="vo-geonews-badge">{state.news?.length || 0}</span>
                    </div>
                  </div>
                  
                  {/* Expandable Districts */}
                  <div className={`vo-geonews-districts \${selectedState === state.id ? 'expanded' : ''}`}>
                    {state.districts?.map(district => (
                      <div 
                        key={district.id}
                        onClick={() => setSelectedDistrict(district.id)}
                        className={`vo-geonews-card vo-geonews-district-card \${selectedDistrict === district.id ? 'active' : ''}`}
                      >
                        <MapPin size={12} />
                        <span>{district.name}</span>
                        <span className="vo-geonews-badge small">{district.news?.length || 0}</span>
                      </div>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="vo-empty-state">Select a Global Sector to view regional nodes.</div>
          )}
        </div>

        {/* Right Column: Live Feed for Selection */}
        <div className="vo-geonews-col vo-geonews-feed">
          <div className="vo-geonews-col-header" style={{ justifyContent: 'space-between' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <Activity className="vo-geonews-col-icon vo-geonews-pulse" />
              <h3>Intelligence Feed</h3>
            </div>
            <div className="vo-geonews-context-label">
              {currentDistrict?.name || currentState?.name || currentCountry?.name || "Global"}
            </div>
          </div>
          
          <div className="vo-geonews-feed-list">
            {Object.keys(groupedNews).length > 0 ? (
              Object.entries(groupedNews).map(([category, items]) => (
                <div key={category} className="vo-geonews-category-group" style={{ marginBottom: '1.5rem' }}>
                  <div className="vo-geonews-category-header" style={{
                    display: 'flex', alignItems: 'center', gap: '0.5rem',
                    padding: '0.6rem 0.8rem', background: 'rgba(255,255,255,0.03)',
                    borderLeft: `3px solid \${items[0]?.category_color || 'var(--color-primary)'}`,
                    borderRadius: '4px', marginBottom: '0.8rem',
                    color: items[0]?.category_color || 'var(--color-primary)'
                  }}>
                    <span style={{ fontSize: '1.2rem' }}>{items[0]?.category_icon || '📰'}</span>
                    <h4 style={{ margin: 0, fontSize: '0.95rem', fontWeight: 600 }}>{category}</h4>
                    <span style={{ fontSize: '0.75rem', color: 'var(--color-text-dim)', marginLeft: 'auto', background: 'rgba(255,255,255,0.05)', padding: '0.2rem 0.5rem', borderRadius: '12px' }}>
                      {items.length} event{items.length !== 1 ? 's' : ''}
                    </span>
                  </div>
                  
                  <div className="vo-geonews-category-items" style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                    {items.map((news, i) => (
                      <div key={news.id} className="vo-feed-card vo-geonews-feed-card" style={{animationDelay: `\${i * 0.05}s`, marginBottom: 0}}>
                        <div className="vo-feed-card-header">
                          <h4 className="vo-geonews-feed-title">{news.title}</h4>
                          <div className={`vo-geonews-sentiment \${(news.sentiment || 'neutral').toLowerCase()}`}>
                            {news.sentiment} {news.score ? `(\${news.score})` : ''}
                          </div>
                        </div>
                        <p className="vo-geonews-feed-summary">{news.summary}</p>
                        <div className="vo-geonews-feed-meta">
                          <div className="vo-geonews-feed-tags">
                            {(news.keywords || []).map((kw, idx) => (
                              <span key={`\${news.id}-kw-\${idx}`} className="vo-geonews-feed-tag">{kw}</span>
                            ))}
                          </div>
                          <span className="vo-time-date">{(news.time ? new Date(news.time) : new Date()).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              ))
            ) : (
               <div className="vo-empty-state">No anomalous activity detected matching current parameters.</div>
            )}
          </div>
        </div>

      </div>
    </div>
  );
};

export default GeoNewsPanel;
