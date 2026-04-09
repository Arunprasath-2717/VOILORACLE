import { useState, useEffect } from 'react';
import { ExternalLink, AlertCircle, CheckCircle, Clock, AlertTriangle, Info, Shield, Users } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

const sentimentStyles = {
  Positive: { color: '#10b981', bg: 'rgba(16, 185, 129, 0.1)' },
  Negative: { color: '#ef4444', bg: 'rgba(239, 68, 68, 0.1)' },
  Neutral:  { color: '#6b7280', bg: 'rgba(107, 114, 128, 0.1)' },
};

const SEVERITY_CONFIG = {
  Critical: { icon: AlertTriangle, color: '#dc2626' },
  High:     { icon: AlertCircle, color: '#f97316' },
  Medium:   { icon: Info, color: '#f59e0b' },
  Low:      { icon: Shield, color: '#10b981' },
};

const EventCard = ({ event, isNew = false }) => {
  const [tick, setTick] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => setTick(t => t + 1), 5000);
    return () => clearInterval(interval);
  }, []);

  const isAlert = !!event.severity;
  const sentiment = sentimentStyles[event.sentiment_label || event.sentiment] || sentimentStyles.Neutral;
  
  let timeAgo = '';
  try {
    const dateStr = isAlert ? event.timestamp : event.published_at;
    if (dateStr) {
      timeAgo = formatDistanceToNow(new Date(dateStr), { addSuffix: true, includeSeconds: true });
    }
  } catch {
    timeAgo = '';
  }

  const isFake = event.fake_news_label === 'Fake';

  // For alerts, override border/glow
  const cardStyle = isAlert ? {
    borderLeft: `3px solid ${SEVERITY_CONFIG[event.severity]?.color || '#f59e0b'}`,
    background: 'var(--color-bg-elevated)'
  } : {};

  return (
    <div className={`vo-feed-card ${isNew ? 'vo-feed-card--new' : ''}`} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', width: '100%', ...cardStyle }}>
      
      {/* HEADER ROW: Title + Badges */}
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.5rem', width: '100%', marginBottom: '0.5rem' }}>
        {isAlert && SEVERITY_CONFIG[event.severity] && (
          <div style={{ 
            display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '4px', 
            background: `${SEVERITY_CONFIG[event.severity].color}1A`, 
            color: SEVERITY_CONFIG[event.severity].color, 
            padding: '3px 8px', borderRadius: '4px', fontSize: '0.65rem', fontWeight: 800, textTransform: 'uppercase', flexShrink: 0 
          }}>
            <AlertTriangle size={12} /> {event.severity} ALERT
          </div>
        )}
        <h3 className="vo-feed-card-title" style={{ margin: 0, textAlign: 'center', width: '100%' }}>{event.title}</h3>
      </div>

      {isAlert && event.description && !event.description.split(/\s+/).some(word => word.length > 40) && (
        <p style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)', margin: '0 0 0.8rem 0', lineHeight: 1.5, textAlign: 'center', wordBreak: 'break-word' }}>
          {event.description}
        </p>
      )}

      {/* META ROW */}
      <div className="vo-feed-card-meta" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem', width: '100%' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem', flexWrap: 'wrap', width: '100%' }}>
          {/* Source / Source Count */}
          {isAlert ? (
            <span className="vo-feed-meta-source" style={{ fontWeight: '600', display: 'flex', alignItems: 'center', gap: '4px' }}>
              <Users size={12} /> {event.source_count} Sources Confirmed
            </span>
          ) : (
            event.source && <span className="vo-feed-meta-source" style={{ fontWeight: '600' }}>{event.source}</span>
          )}

          {timeAgo && (
            <span className="vo-feed-meta-time" style={{ color: 'var(--color-text-dim)', fontSize: '0.75rem' }}>
              <Clock size={11} style={{ display: 'inline', marginRight: '4px' }} />{timeAgo}
            </span>
          )}
        </div>

        {/* Sentiment Badge */}
        <div style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '0.4rem', padding: '0.2rem 0.6rem', background: sentiment.bg, borderRadius: '4px', border: `1px solid ${sentiment.color}20` }}>
          <span style={{ fontSize: '0.65rem', fontWeight: 600, color: 'var(--color-text-secondary)', textTransform: 'uppercase' }}>Sentiment:</span>
          <span style={{ color: sentiment.color, fontWeight: '700', fontSize: '0.75rem' }}>
            {event.sentiment_label || event.sentiment}
          </span>
        </div>
      </div>

      {/* FOOTER ROW */}
      <div className="vo-feed-card-footer" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%', gap: '0.75rem', borderTop: '1px solid var(--color-border)', paddingTop: '0.75rem' }}>
        
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem', flexWrap: 'wrap', width: '100%' }}>
          {!isAlert && (
            isFake ? (
              <span className="vo-feed-integrity vo-feed-integrity--fake">
                <AlertCircle size={12} /> Suspicious
              </span>
            ) : (
              <span className="vo-feed-integrity vo-feed-integrity--real">
                <CheckCircle size={12} /> Verified
              </span>
            )
          )}

          {isAlert && event.keywords && (
             <div style={{ display: 'flex', justifyContent: 'center', gap: '4px', flexWrap: 'wrap' }}>
               {event.keywords.slice(0, 3).map(kw => (
                  <span key={kw} style={{ fontSize: '0.6rem', background: 'var(--color-bg-surface)', padding: '2px 6px', borderRadius: '4px', color: 'var(--color-text-dim)' }}>#{kw}</span>
               ))}
             </div>
          )}

          {event.url && (
            <a
              href={event.url}
              target="_blank"
              rel="noopener noreferrer"
              className="vo-feed-card-link"
              title="Open source"
              style={{ 
                display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '6px', 
                fontSize: '0.75rem', color: 'var(--color-primary)', 
                textDecoration: 'none', fontWeight: 600
              }}
            >
              Read Source <ExternalLink size={12} />
            </a>
          )}
        </div>
      </div>
    </div>
  );
};

export default EventCard;
