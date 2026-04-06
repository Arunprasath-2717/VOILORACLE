import { Activity, Newspaper, TrendingUp, Shield, Zap, BarChart2 } from 'lucide-react';
import { useMetrics, useAISummary, useEvents } from '../../hooks/useApi';
import AnimatedNumber from '../AnimatedNumber';

/* ── Skeleton Loader ─────────────────────────────────── */
const Skeleton = ({ width, height }) => (
  <div className="vo-skeleton" style={{ width: width || '100%', height: height || '1rem' }} />
);

/* ── Stat Card ───────────────────────────────────────── */
const StatCard = ({ icon: Icon, label, value, subtitle, color, loading }) => (
  <div className="vo-stat-card" style={{ '--accent': color }}>
    <div className="vo-stat-header">
      <div className="vo-stat-icon" style={{ background: `${color}18`, color }}>
        <Icon size={16} strokeWidth={1.5} />
      </div>
    </div>
    <div className="vo-stat-body">
      {loading ? (
        <Skeleton width="60%" height="2rem" />
      ) : (
        <span className="vo-stat-value">
          <AnimatedNumber end={value} />
        </span>
      )}
      <span className="vo-stat-label">{label}</span>
      {subtitle && <span className="vo-stat-subtitle">{subtitle}</span>}
    </div>
  </div>
);

/* ── AI Summary Card ─────────────────────────────────── */
const AISummaryCard = ({ summary, loading }) => {
  if (loading) {
    return (
      <div className="vo-ai-summary-card">
        <Skeleton height="1rem" />
        <Skeleton width="80%" height="1rem" />
        <Skeleton width="60%" height="1rem" />
      </div>
    );
  }

  if (!summary) return null;

  const moodColor = {
    'Strongly Bullish': '#10b981',
    'Moderately Bullish': '#34d399',
    'Strongly Bearish': '#ef4444',
    'Moderately Bearish': '#f97316',
    'Mixed / Uncertain': '#eab308',
  }[summary.market_mood] || '#6b7280';

  return (
    <div className="vo-ai-summary-card">
      <div className="vo-ai-summary-header">
        <Zap size={14} strokeWidth={1.5} style={{ color: '#818cf8' }} />
        <span className="vo-ai-summary-title">AI Intelligence Summary</span>
      </div>
      <p className="vo-ai-summary-text">{summary.summary}</p>
      <div className="vo-ai-summary-metrics">
        <div className="vo-ai-metric">
          <span className="vo-ai-metric-label">Market Mood</span>
          <span className="vo-ai-metric-value" style={{ color: moodColor }}>
            {summary.market_mood}
          </span>
        </div>
        <div className="vo-ai-metric">
          <span className="vo-ai-metric-label">Stability</span>
          <span className="vo-ai-metric-value">{summary.global_stability_score}%</span>
        </div>
        <div className="vo-ai-metric">
          <span className="vo-ai-metric-label">Confidence</span>
          <span className="vo-ai-metric-value">{(summary.confidence * 100).toFixed(0)}%</span>
        </div>
      </div>
      <div className="vo-ai-sentiment-bar">
        <div
          className="vo-ai-sentiment-segment vo-ai-sentiment-pos"
          style={{ width: `${summary.positive_pct}%` }}
          title={`Positive: ${summary.positive_pct}%`}
        />
        <div
          className="vo-ai-sentiment-segment vo-ai-sentiment-neg"
          style={{ width: `${summary.negative_pct}%` }}
          title={`Negative: ${summary.negative_pct}%`}
        />
        <div
          className="vo-ai-sentiment-segment vo-ai-sentiment-neu"
          style={{ width: `${100 - summary.positive_pct - summary.negative_pct}%` }}
          title="Neutral"
        />
      </div>
    </div>
  );
};

/* ── Top Events Preview ──────────────────────────────── */
const TopEventsPreview = ({ events, loading }) => {
  if (loading) {
    return (
      <div className="vo-top-events">
        <h3 className="vo-section-title">
          <Shield size={14} strokeWidth={1.5} /> Top Priority Events
        </h3>
        {[1, 2, 3].map((i) => (
          <div key={i} className="vo-event-skeleton">
            <Skeleton height="3.5rem" />
          </div>
        ))}
      </div>
    );
  }

  const topEvents = (events || [])
    .sort((a, b) => (b.importance_score || 0) - (a.importance_score || 0))
    .slice(0, 5);

  const riskColor = (score) => {
    if (score >= 0.7) return '#ef4444';
    if (score >= 0.4) return '#f59e0b';
    return '#10b981';
  };

  return (
    <div className="vo-top-events">
      <h3 className="vo-section-title">
        <Shield size={14} strokeWidth={1.5} /> Top Priority Events
      </h3>
      <div className="vo-events-list">
        {topEvents.map((ev) => (
          <div key={ev.id} className="vo-event-item">
            <div className="vo-event-dot" style={{ backgroundColor: riskColor(ev.risk_score || 0) }} />
            <div className="vo-event-content">
              <span className="vo-event-label">{ev.label}</span>
              <div className="vo-event-meta">
                <span>{ev.size} article{ev.size !== 1 ? 's' : ''}</span>
                <span className="vo-event-sentiment">{ev.sentiment_label}</span>
                {ev.lifecycle && (
                  <span className="vo-event-lifecycle">{ev.lifecycle}</span>
                )}
              </div>
            </div>
            <div className="vo-event-scores">
              <span className="vo-event-risk" style={{ color: riskColor(ev.risk_score || 0) }}>
                Risk: {((ev.risk_score || 0) * 100).toFixed(0)}%
              </span>
            </div>
          </div>
        ))}
        {topEvents.length === 0 && (
          <p className="vo-empty-state">No events detected yet. The pipeline is processing data...</p>
        )}
      </div>
    </div>
  );
};

/* ── Overview Panel (Main) ───────────────────────────── */
const OverviewPanel = () => {
  const { data: metrics, loading: metricsLoading } = useMetrics(15000);
  const { data: summary, loading: summaryLoading } = useAISummary(30000);
  const { data: events, loading: eventsLoading } = useEvents(25, 10000);

  const sentimentDist = metrics?.sentiment_distribution || {};
  const totalSentiment =
    (sentimentDist.Positive || 0) + (sentimentDist.Negative || 0) + (sentimentDist.Neutral || 0);

  return (
    <div className="vo-overview">
      {/* Stats Grid */}
      <div className="vo-stats-grid">
        <StatCard
          icon={Newspaper}
          label="Total Articles"
          value={metrics?.article_count || 0}
          color="#3b82f6"
          loading={metricsLoading}
        />
        <StatCard
          icon={Activity}
          label="Active Events"
          value={metrics?.event_count || 0}
          color="#8b5cf6"
          loading={metricsLoading}
        />
        <StatCard
          icon={TrendingUp}
          label="Positive Signals"
          value={sentimentDist.Positive || 0}
          subtitle={totalSentiment > 0 ? `${((sentimentDist.Positive / totalSentiment) * 100).toFixed(1)}%` : ''}
          color="#10b981"
          loading={metricsLoading}
        />
        <StatCard
          icon={BarChart2}
          label="Risk Signals"
          value={sentimentDist.Negative || 0}
          subtitle={totalSentiment > 0 ? `${((sentimentDist.Negative / totalSentiment) * 100).toFixed(1)}%` : ''}
          color="#ef4444"
          loading={metricsLoading}
        />
      </div>

      {/* AI Summary */}
      <AISummaryCard summary={summary} loading={summaryLoading} />

      {/* Top Events */}
      <TopEventsPreview events={events} loading={eventsLoading} />
    </div>
  );
};

export default OverviewPanel;
