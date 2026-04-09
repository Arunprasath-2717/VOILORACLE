import React from 'react';
import AnalyticsCharts from './AnalyticsCharts';
import SectorGrid from './SectorGrid';
import { Layers } from 'lucide-react';

const AnalyticsIntelPanel = () => {
  return (
    <div className="vo-analytics-intel-panel">
      <div className="vo-panel-header" style={{ marginBottom: '1.5rem', textAlign: 'center', padding: '1rem', background: 'var(--color-bg-card)', borderRadius: 'var(--radius-lg)', border: '1px solid var(--color-border-card)', backdropFilter: 'blur(12px)' }}>
        <h1 style={{ fontSize: '1.6rem', color: 'var(--color-primary)', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.6rem', margin: 0 }}>
          <Layers size={24} />
          Advanced Analytics & Sector Intelligence
        </h1>
        <p style={{ color: 'var(--color-text-dim)', fontSize: '0.9rem', marginTop: '0.4rem', marginBottom: 0 }}>
          Real-time aggregated global metrics and AI-driven predictive deep sector analysis
        </p>
      </div>

      <div className="vo-analytics-intel-content" style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>
        <div className="vo-analytics-section">
          <AnalyticsCharts />
        </div>
        
        <div className="vo-intel-section" style={{ borderTop: '1px solid var(--color-border)', paddingTop: '1.5rem' }}>
          <SectorGrid />
        </div>
      </div>
    </div>
  );
};

export default AnalyticsIntelPanel;
