import { useState } from 'react';
import Header from '../components/dashboard/Header';

// Static asset from the public folder (no import needed)
const heroVideo = '/3.mp4';

import TabNavigation from '../components/dashboard/TabNavigation';
import OverviewPanel from '../components/dashboard/OverviewPanel';
import GeoNewsPanel from '../components/dashboard/GeoNewsPanel';
import LiveFeedList from '../components/dashboard/LiveFeedList';
import SectorGrid from '../components/dashboard/SectorGrid';
import AnalyticsCharts from '../components/dashboard/AnalyticsCharts';
import NeuralNetworkPanel from '../components/dashboard/NeuralNetworkPanel';

const panels = {
  overview: OverviewPanel,
  'geo-news': GeoNewsPanel,
  'live-feeds': LiveFeedList,
  sectors: SectorGrid,
  analytics: AnalyticsCharts,
  'ai-insights': NeuralNetworkPanel,
};

const TICKER_ITEMS = [
  '⚡ GEOPOLITICAL: South China Sea tensions — Elevated threat level',
  '🛡️ CYBER: Critical infrastructure alert across 12 nations',
  '📊 MARKETS: Emerging markets volatility index surged +3.2%',
  '🌍 CLIMATE: Category 4 cyclone forming in Indian Ocean basin',
  '🔬 TECH: EU AI regulation framework — Vote pending',
  '💰 ECONOMIC: Central bank policy divergence — 3 nations',
];

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const Panel = panels[activeTab];

  return (
    <div className="vo-dashboard">
      <Header onLogoClick={() => { setActiveTab('overview'); window.scrollTo({ top: 0, behavior: 'smooth' }); }} />
      <TabNavigation activeTab={activeTab} onTabChange={setActiveTab} />
      <main className="vo-main">
        <div className="vo-main-inner">
          {activeTab === 'overview' && (
            <div className="vo-hero-wrap">

              {/* ── VIDEO ── */}
              <video 
                autoPlay 
                loop 
                muted 
                playsInline 
                src={heroVideo}
                className="vo-hero-video"
              />

              {/* ── Vignette ── */}
              <div className="vo-hero-vignette" />

              {/* ── Scan-line ── */}
              <div className="vo-hero-scanline" />

              {/* ── CONTENT ── */}
              <div className="vo-hero-content">

                {/* Live status */}
                <div className="vo-hero-badge-row">
                  <span className="vo-hero-badge vo-hero-badge--green">
                    <span className="vo-hero-badge-dot vo-hero-badge-dot--green" />
                    Neural Network Online
                  </span>
                  <span className="vo-hero-badge vo-hero-badge--amber">
                    <span className="vo-hero-badge-dot vo-hero-badge-dot--amber" />
                    Live Threat Scanning
                  </span>
                </div>

                {/* Main heading */}
                <h1 className="vo-hero-title">
                  Global Intelligence{' '}
                  <span className="vo-hero-title-gradient">Command Center</span>
                </h1>

                {/* Tagline */}
                <p className="vo-hero-desc">
                  Real-time AI-powered geopolitical surveillance, global financial analytics &amp; neural threat intelligence mapping.
                </p>
                
                {/* Stats */}
                <div className="vo-hero-stats">
                  <div className="vo-hero-stat">
                    <div className="vo-hero-stat-value">3.2B</div>
                    <div className="vo-hero-stat-label">Global Entities</div>
                  </div>
                  <div className="vo-hero-stat">
                    <div className="vo-hero-stat-value" style={{color: '#f59e0b'}}>Active</div>
                    <div className="vo-hero-stat-label">Global Monitoring</div>
                  </div>
                  <div className="vo-hero-stat">
                    <div className="vo-hero-stat-value" style={{color: '#3b82f6'}}>8ms</div>
                    <div className="vo-hero-stat-label">Avg Latency</div>
                  </div>
                  <div className="vo-hero-stat">
                    <div className="vo-hero-stat-value">94%</div>
                    <div className="vo-hero-stat-label">AI Confidence</div>
                  </div>
                </div>

              </div>

              {/* ── BOTTOM: Intel Ticker ── */}
              <div className="vo-hero-ticker-wrap">
                <div className="vo-hero-ticker">
                  {[...TICKER_ITEMS, ...TICKER_ITEMS].map((item, i) => (
                    <span key={i} className="vo-hero-ticker-item">{item}</span>
                  ))}
                </div>
              </div>

              {/* ── Corner brackets ── */}
              {['top-left','top-right','bottom-left','bottom-right'].map(pos => {
                const isTop = pos.includes('top');
                const isLeft = pos.includes('left');
                return (
                  <div key={pos} className="vo-hero-corner" style={{
                    [isTop ? 'top' : 'bottom']: '0.75rem',
                    [isLeft ? 'left' : 'right']: '0.75rem',
                    borderTop: isTop ? '2px solid rgba(16,185,129,0.3)' : 'none',
                    borderBottom: !isTop ? '2px solid rgba(16,185,129,0.3)' : 'none',
                    borderLeft: isLeft ? '2px solid rgba(16,185,129,0.3)' : 'none',
                    borderRight: !isLeft ? '2px solid rgba(16,185,129,0.3)' : 'none',
                  }} />
                );
              })}
            </div>
          )}
          <Panel />
        </div>
      </main>
      <footer className="vo-footer">
        <p>KRONAXIS AI Intelligence Platform · Real-time Global Monitoring</p>
      </footer>
    </div>
  );
};

export default Dashboard;
