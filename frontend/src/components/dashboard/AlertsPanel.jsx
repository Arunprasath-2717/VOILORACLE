import { Shield, AlertTriangle, AlertCircle, Info, Clock, Users, Zap } from 'lucide-react';
import { useAlerts } from '../../hooks/useApi';

const SEVERITY_CONFIG = {
  Critical: { icon: AlertTriangle, color: '#dc2626', bg: 'rgba(220,38,38,0.08)', border: 'rgba(220,38,38,0.25)' },
  High:     { icon: AlertCircle, color: '#f97316', bg: 'rgba(249,115,22,0.08)', border: 'rgba(249,115,22,0.25)' },
  Medium:   { icon: Info, color: '#f59e0b', bg: 'rgba(245,158,11,0.08)', border: 'rgba(245,158,11,0.25)' },
  Low:      { icon: Shield, color: '#10b981', bg: 'rgba(16,185,129,0.08)', border: 'rgba(16,185,129,0.25)' },
};

const AlertsPanel = () => {
  const { data: alerts, loading, error } = useAlerts(12, 60000);

  if (loading && !alerts) {
    return (
      <div className="vo-geonews-loading">
        <Shield className="vo-spinner" />
        <span>Scanning multi-source consensus alerts...</span>
      </div>
    );
  }

  const alertList = Array.isArray(alerts) ? alerts : [];

  return (
    <div style={{ maxWidth: '64rem', margin: '0 auto' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.25rem' }}>
        <Shield size={18} />
        <h3 className="vo-section-title" style={{ marginBottom: 0 }}>Validated Intelligence Alerts</h3>
        <span style={{ fontSize: '0.65rem', color: 'var(--color-text-dim)', background: 'rgba(0,0,0,0.04)', padding: '0.2rem 0.5rem', borderRadius: '12px', marginLeft: 'auto' }}>
          Multi-source consensus required
        </span>
      </div>

      <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '1.25rem', flexWrap: 'wrap' }}>
        {Object.entries(SEVERITY_CONFIG).map(([severity, conf]) => {
          const count = alertList.filter(a => a.severity === severity).length;
          const Icon = conf.icon;
          return (
            <div key={severity} className="vo-stat-card" style={{
              flex: '1 1 120px', minWidth: '120px', padding: '0.875rem',
              borderLeft: `3px solid ${conf.color}`,
            }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.4rem' }}>
                <Icon size={14} style={{ color: conf.color }} />
                <span style={{ fontSize: '0.7rem', fontWeight: 600, color: conf.color, textTransform: 'uppercase', letterSpacing: '0.05em' }}>{severity}</span>
              </div>
              <div style={{ fontSize: '1.5rem', fontWeight: 800, fontFamily: 'var(--font-heading)' }}>{count}</div>
            </div>
          );
        })}
      </div>

      {alertList.length === 0 ? (
        <div className="vo-empty-state" style={{ padding: '3rem' }}>
          <Shield size={40} style={{ color: 'var(--color-success)', marginBottom: '1rem', opacity: 0.5 }} />
          <p>No validated alerts at this time. The multi-source consensus engine requires 2+ independent sources to confirm an event before flagging it.</p>
        </div>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
          {alertList.map((alert, i) => {
            const conf = SEVERITY_CONFIG[alert.severity] || SEVERITY_CONFIG.Low;
            const Icon = conf.icon;
            return (
              <div key={alert.id || i} className="vo-feed-card" style={{
                borderLeft: `3px solid ${conf.color}`,
                background: conf.bg,
                border: `1px solid ${conf.border}`,
                borderLeftWidth: '3px',
                borderLeftColor: conf.color,
                animationDelay: `${i * 0.06}s`,
              }}>
                <div style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem' }}>
                  <div style={{
                    width: '2rem', height: '2rem', borderRadius: '50%',
                    background: conf.bg, display: 'flex', alignItems: 'center', justifyContent: 'center',
                    flexShrink: 0, marginTop: '0.15rem'
                  }}>
                    <Icon size={16} style={{ color: conf.color }} />
                  </div>
                  <div style={{ flex: 1, minWidth: 0 }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '0.35rem' }}>
                      <span style={{
                        fontSize: '0.6rem', fontWeight: 700, color: conf.color,
                        background: `${conf.color}15`, padding: '0.15rem 0.45rem', borderRadius: '4px',
                        textTransform: 'uppercase', letterSpacing: '0.06em'
                      }}>{alert.severity}</span>
                      <span style={{
                        fontSize: '0.6rem', fontWeight: 600, color: 'var(--color-text-dim)',
                        display: 'flex', alignItems: 'center', gap: '0.25rem'
                      }}>
                        <Users size={10} /> {alert.source_count} sources
                      </span>
                      <span style={{
                        fontSize: '0.6rem', color: alert.sentiment === 'Negative' ? '#ef4444' : alert.sentiment === 'Positive' ? '#10b981' : '#f59e0b',
                        fontWeight: 600
                      }}>{alert.sentiment}</span>
                    </div>
                    <h4 style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--color-text)', margin: '0 0 0.35rem', lineHeight: 1.4 }}>
                      {alert.title}
                    </h4>
                    {alert.description && (
                      <p style={{ fontSize: '0.78rem', color: 'var(--color-text-muted)', lineHeight: 1.6, margin: '0 0 0.5rem' }}>
                        {alert.description}
                      </p>
                    )}
                    <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', alignItems: 'center' }}>
                      {(alert.keywords || []).map((kw, j) => (
                        <span key={j} style={{
                          fontSize: '0.6rem', padding: '0.15rem 0.4rem', borderRadius: '4px',
                          background: 'rgba(0,0,0,0.04)', color: 'var(--color-text-dim)', fontWeight: 500
                        }}>{kw}</span>
                      ))}
                      <span style={{ fontSize: '0.62rem', color: 'var(--color-text-dim)', marginLeft: 'auto', display: 'flex', alignItems: 'center', gap: '0.25rem' }}>
                        <Clock size={10} />
                        {alert.timestamp ? new Date(alert.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }) : '—'}
                      </span>
                    </div>
                    {alert.sources && alert.sources.length > 0 && (
                      <div style={{ marginTop: '0.5rem', display: 'flex', gap: '0.35rem', flexWrap: 'wrap' }}>
                        {alert.sources.map((s, j) => (
                          <span key={j} style={{
                            fontSize: '0.58rem', padding: '0.1rem 0.35rem', borderRadius: '3px',
                            background: 'rgba(0,31,84,0.06)', color: 'var(--color-primary)', fontWeight: 500
                          }}>{s}</span>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};

export default AlertsPanel;
