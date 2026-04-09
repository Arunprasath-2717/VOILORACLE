import { useState, useMemo } from 'react';
import { Radio, Filter } from 'lucide-react';
import { useArticles, useAlerts } from '../../hooks/useApi';
import EventCard from './EventCard';

const LiveFeedList = () => {
  const { data: articles, loading: articlesLoading, error } = useArticles(100, 10000);
  const { data: alerts, loading: alertsLoading } = useAlerts(12, 30000);
  const [filter, setFilter] = useState('all');

  // Combine, sort, and deduplicate feed
  const combinedFeed = useMemo(() => {
    const rawArticles = articles || [];
    const rawAlerts = Array.isArray(alerts) ? alerts : [];

    // Filter articles based on user selection
    const filteredArticles = rawArticles.filter((a) => {
      if (filter === 'all') return true;
      return a.sentiment_label === filter;
    });

    // We only show alerts when viewing "all" or if the alert heavily matches the filter
    const filteredAlerts = rawAlerts.filter((a) => {
      if (filter === 'all') return true;
      return a.sentiment === filter || a.sentiment_label === filter;
    });

    // Merge them into one array
    const merged = [...filteredAlerts, ...filteredArticles];

    // Deduplicate by normalized title prefix (fuzzy matching for recurring templated news)
    const seenMap = new Map();
    merged.forEach((item) => {
      if (!item || !item.title) return;
      
      // Strip everything except letters, push to lowercase, and take first 40 chars.
      // This clusters recurring articles like "Morning News Broadcast - March 6" and "Morning News Broadcast - March 11"
      const fuzzyKey = item.title.toLowerCase().replace(/[^a-z]/g, '').substring(0, 40);
      
      if (seenMap.has(fuzzyKey)) {
        // If we already have this pattern, override it ONLY if the new one is an alert
        const existing = seenMap.get(fuzzyKey);
        if (item.severity && !existing.severity) {
          seenMap.set(fuzzyKey, item);
        }
      } else {
        seenMap.set(fuzzyKey, item);
      }
    });

    const deduped = Array.from(seenMap.values());

    // Sort by whichever timestamp exists (descending)
    deduped.sort((a, b) => {
      const dateA = new Date(a.timestamp || a.published_at || Date.now()).getTime();
      const dateB = new Date(b.timestamp || b.published_at || Date.now()).getTime();
      return dateB - dateA;
    });

    return deduped;
  }, [articles, alerts, filter]);

  const loading = articlesLoading || alertsLoading;

  return (
    <div className="vo-live-feed">
      {/* Header */}
      <div className="vo-live-feed-header">
        <div className="vo-live-feed-title-row">
          <h2 className="vo-section-title">
            <Radio size={16} /> Live Intelligence & Alerts Feed
          </h2>
          <div className="vo-live-indicator">
            <span className="vo-live-dot" />
            <span className="vo-live-count">
              {combinedFeed.length} signals · Auto-updating
            </span>
          </div>
        </div>

        {/* Filter Buttons */}
        <div className="vo-feed-filters">
          <Filter size={14} />
          {['all', 'Positive', 'Neutral', 'Negative'].map((f) => (
            <button
              key={f}
              onClick={() => setFilter(f)}
              className={`vo-feed-filter-btn ${filter === f ? 'vo-feed-filter-btn--active' : ''}`}
            >
              {f === 'all' ? 'All' : f}
            </button>
          ))}
        </div>
      </div>

      {/* Error State */}
      {error && (
        <div className="vo-feed-error">
          Unable to load feed: {error}. Retrying...
        </div>
      )}

      {/* Loading State */}
      {loading && combinedFeed.length === 0 && (
        <div className="vo-feed-loading">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="vo-skeleton" style={{ height: '5rem', marginBottom: '0.5rem' }} />
          ))}
        </div>
      )}

      <div className="vo-feed-list" style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
        {/* Unified Stream of Alerts and Articles */}
        {combinedFeed.map((item, i) => (
          <EventCard
            key={`${item.severity ? 'alert' : 'article'}-${item.id || i}`}
            event={item}
            isNew={i < 3 && !loading}
          />
        ))}

        {/* Empty State */}
        {!loading && combinedFeed.length === 0 && (
          <p className="vo-empty-state">
            No intelligence matches the current filter. Try selecting "All" or wait for new data.
          </p>
        )}
      </div>
    </div>
  );
};

export default LiveFeedList;
