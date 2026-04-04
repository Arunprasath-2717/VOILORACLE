import { useState, useEffect } from 'react';
import { ExternalLink, AlertCircle, CheckCircle, Clock } from 'lucide-react';
import { formatDistanceToNow } from 'date-fns';

const sentimentStyles = {
  Positive: { color: '#10b981', bg: 'rgba(16, 185, 129, 0.1)' },
  Negative: { color: '#ef4444', bg: 'rgba(239, 68, 68, 0.1)' },
  Neutral:  { color: '#6b7280', bg: 'rgba(107, 114, 128, 0.1)' },
};

const EventCard = ({ event, isNew = false }) => {
  const [tick, setTick] = useState(0);

  useEffect(() => {
    // Force re-render every 5 seconds to keep the "includeSeconds" timer live and lively.
    const interval = setInterval(() => setTick(t => t + 1), 5000);
    return () => clearInterval(interval);
  }, []);

  const sentiment = sentimentStyles[event.sentiment_label] || sentimentStyles.Neutral;
  let timeAgo = '';
  try {
    if (event.published_at) {
      timeAgo = formatDistanceToNow(new Date(event.published_at), { addSuffix: true, includeSeconds: true });
    }
  } catch {
    timeAgo = '';
  }

  const isFake = event.fake_news_label === 'Fake';

  return (
    <div className={`vo-feed-card ${isNew ? 'vo-feed-card--new' : ''}`} style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', textAlign: 'center', width: '100%' }}>
      <div className="vo-feed-card-header" style={{ width: '100%', textAlign: 'center' }}>
        <h3 className="vo-feed-card-title" style={{ textAlign: 'center', width: '100%', margin: '0 auto' }}>{event.title}</h3>
      </div>

      <div className="vo-feed-card-meta" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '0.65rem', marginBottom: '0.75rem', width: '100%' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '0.65rem', flexWrap: 'wrap', width: '100%' }}>
          {event.source && <span className="vo-feed-meta-source" style={{ fontWeight: '600' }}>{event.source}</span>}
          {timeAgo && (
            <span className="vo-feed-meta-time" style={{ color: 'var(--color-text-dim)', fontSize: '0.75rem' }}>
              <Clock size={11} style={{ display: 'inline', marginRight: '4px' }} />{timeAgo}
            </span>
          )}
        </div>

        {event.url && (
          <a
            href={event.url}
            target="_blank"
            rel="noopener noreferrer"
            className="vo-feed-card-link"
            title="Open source"
            style={{ 
              display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '6px', 
              fontSize: '0.8rem', color: 'var(--color-primary)', 
              textDecoration: 'underline', width: 'fit-content' 
            }}
          >
            <ExternalLink size={14} /> Full Article Analysis
          </a>
        )}

        <div style={{ display: 'inline-flex', alignItems: 'center', justifyContent: 'center', gap: '0.75rem', padding: '0.55rem 0.8rem', background: sentiment.bg, borderRadius: '6px', border: `1px solid ${sentiment.color}30`, alignSelf: 'center' }}>
          <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-text-secondary)' }}>Sentiment:</span>
          <span
            className="vo-feed-meta-sentiment"
            style={{ color: sentiment.color, fontWeight: '700', fontSize: '0.8rem' }}
          >
            {event.sentiment_label}
          </span>
          {event.sentiment_score != null && (
            <span className="vo-feed-meta-score" style={{ color: sentiment.color, opacity: 0.8, fontSize: '0.75rem' }}>
              (Score: {event.sentiment_score > 0 ? '+' : ''}{event.sentiment_score.toFixed(3)})
            </span>
          )}
        </div>
      </div>

      <div className="vo-feed-card-footer" style={{ display: 'flex', justifyContent: 'center', width: '100%', gap: '0.5rem', marginTop: '0.5rem' }}>
        {isFake ? (
          <span className="vo-feed-integrity vo-feed-integrity--fake">
            <AlertCircle size={12} /> Suspicious
          </span>
        ) : (
          <span className="vo-feed-integrity vo-feed-integrity--real">
            <CheckCircle size={12} /> Verified
          </span>
        )}
        {event.language && event.language !== 'en' && (
          <span className="vo-feed-meta-lang">{event.language.toUpperCase()}</span>
        )}
      </div>
    </div>
  );
};

export default EventCard;
