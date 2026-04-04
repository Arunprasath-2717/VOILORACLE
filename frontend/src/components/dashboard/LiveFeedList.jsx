import { useState } from 'react';
import { Radio, Filter } from 'lucide-react';
import { useArticles } from '../../hooks/useApi';
import EventCard from './EventCard';

const LiveFeedList = () => {
  const { data: articles, loading, error } = useArticles(100, 10000);
  const [filter, setFilter] = useState('all');

  const filteredArticles = (articles || []).filter((a) => {
    if (filter === 'all') return true;
    return a.sentiment_label === filter;
  });

  return (
    <div className="vo-live-feed">
      {/* Header */}
      <div className="vo-live-feed-header">
        <div className="vo-live-feed-title-row">
          <h2 className="vo-section-title">
            <Radio size={16} /> Live Intelligence Feed
          </h2>
          <div className="vo-live-indicator">
            <span className="vo-live-dot" />
            <span className="vo-live-count">
              {filteredArticles.length} signal{filteredArticles.length !== 1 ? 's' : ''} · Auto-updating
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
      {loading && !articles && (
        <div className="vo-feed-loading">
          {[1, 2, 3, 4, 5].map((i) => (
            <div key={i} className="vo-skeleton" style={{ height: '5rem', marginBottom: '0.5rem' }} />
          ))}
        </div>
      )}

      {/* Feed Cards */}
      <div className="vo-feed-list">
        {filteredArticles.map((article, i) => (
          <EventCard
            key={article.id || i}
            event={article}
            isNew={i < 3 && !loading}
          />
        ))}
        {!loading && filteredArticles.length === 0 && (
          <p className="vo-empty-state">
            No articles match the current filter. Try selecting "All" or wait for new data.
          </p>
        )}
      </div>
    </div>
  );
};

export default LiveFeedList;
