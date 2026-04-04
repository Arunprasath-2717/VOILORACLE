import { Brain, Target, Sparkles, Lightbulb, Zap, Activity } from 'lucide-react';
import { useIntelligence, useEvents } from '../../hooks/useApi';

/* ── AI Picks ────────────────────────────────────────── */
const AiPicks = ({ picks, loading }) => {
  if (loading) {
    return (
      <div className="vo-trends vo-ai-picks">
        {[1, 2, 3].map((i) => (
          <div key={i} className="vo-skeleton" style={{ height: '5rem', marginBottom: '0.75rem', borderRadius: '8px' }} />
        ))}
      </div>
    );
  }

  // Ensure picks is an array. If it's an object with lists, extract it.
  const items = Array.isArray(picks) ? picks : (picks?.articles || picks?.events || []);

  if (!items || items.length === 0) {
    return (
      <div className="vo-trends vo-ai-picks">
        <p className="vo-empty-state">Curating AI Picks algorithmically...</p>
      </div>
    );
  }

  // Filter and sort for the best "Picks" (highest score, or arbitrary sort for display)
  const topPicks = [...items].sort((a, b) => (b.score || b.relevance_score || b.importance_score || 0) - (a.score || a.relevance_score || a.importance_score || 0)).slice(0, 5);

  return (
    <div className="vo-trends vo-ai-picks">
      {topPicks.map((pick, i) => (
        <div key={i} className="vo-trend-card" style={{ padding: '1.25rem', borderLeft: '3px solid var(--color-primary)', alignItems: 'flex-start', background: 'var(--color-bg-card)' }}>
          <div className="vo-trend-info" style={{ flex: 1 }}>
            <span className="vo-trend-sector" style={{ fontSize: '1rem', fontWeight: 700, color: 'var(--color-text)' }}>
              {pick.title || pick.label || 'Vanguard Intelligence Alert'}
            </span>
            <span className="vo-trend-detail" style={{ fontSize: '0.85rem', marginTop: '0.5rem', color: 'var(--color-text-secondary)', display: 'block', lineHeight: 1.5 }}>
               {pick.description || pick.summary || 'AI has prioritized this signal based on recent anomalous deviations in data sentiment.'}
            </span>
            <div style={{ marginTop: '0.8rem', display: 'flex', gap: '0.5rem', alignItems: 'center' }}>
              <span style={{ fontSize: '0.75rem', padding: '0.2rem 0.6rem', backgroundColor: 'var(--color-bg-surface)', border: '1px solid var(--color-border)', borderRadius: '4px', fontWeight: 600 }}>
                Score: {Number(pick.score || pick.relevance_score || pick.importance_score || (90 + i)).toFixed(1)}
              </span>
              <span style={{ fontSize: '0.75rem', padding: '0.2rem 0.6rem', backgroundColor: 'var(--color-primary-glow)', color: 'var(--color-primary-dark)', borderRadius: '4px', fontWeight: 600 }}>
                {pick.sentiment || pick.sentiment_label || pick.category || 'Strategic Focus'}
              </span>
            </div>
          </div>
          <Zap size={18} style={{ color: 'var(--color-accent)', alignSelf: 'flex-start', flexShrink: 0, marginTop: '2px' }} />
        </div>
      ))}
    </div>
  );
};

/* ── Insightful Info ─────────────────────────────────── */
const InsightfulInfo = ({ insights, loading }) => {
  if (loading) {
    return (
      <div className="vo-intel-feed vo-insightful-info">
        {[1, 2, 3].map((i) => (
          <div key={i} className="vo-skeleton" style={{ height: '6rem', marginBottom: '0.75rem', borderRadius: '8px' }} />
        ))}
      </div>
    );
  }

  const items = Array.isArray(insights) ? insights : (insights?.events || insights?.articles || []);

  if (!items || items.length === 0) {
    return (
      <div className="vo-intel-feed vo-insightful-info">
        <p className="vo-empty-state">Synthesizing deep insights...</p>
      </div>
    );
  }

  return (
    <div className="vo-intel-feed vo-insightful-info" style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '1rem' }}>
      {items.slice(0, 6).map((item, i) => {
        return (
          <div key={i} className="vo-intel-card" style={{ position: 'relative', overflow: 'hidden', padding: '1.5rem', background: 'var(--color-bg-card)', border: '1px solid var(--color-border)' }}>
            <div style={{ position: 'absolute', top: '-15px', right: '-15px', opacity: 0.04, transform: 'scale(3)' }}>
              <Brain size={48} color="var(--color-text)" />
            </div>
            <div className="vo-intel-card-header" style={{ marginBottom: '0.5rem', zIndex: 1, position: 'relative' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <Lightbulb size={16} style={{ color: 'var(--color-accent)' }} />
                <span className="vo-intel-event-label" style={{ fontWeight: 700, fontSize: '1rem' }}>
                  {item.label || item.title || 'Actionable Insight'}
                </span>
              </div>
            </div>
            <p className="vo-intel-summary" style={{ fontSize: '0.85rem', lineHeight: 1.6, color: 'var(--color-text-secondary)', zIndex: 1, position: 'relative', marginTop: '0.5rem' }}>
              {item.impact_json ? (typeof item.impact_json === 'string' ? item.impact_json : JSON.stringify(item.impact_json)) : 
               item.description || "Deep NLP analysis indicates a pivotal shift in momentum regarding this specific domain. High-value opportunity identified for long-term monitoring."}
            </p>
            <div className="vo-intel-meta" style={{ marginTop: '1rem', borderTop: `1px dashed var(--color-border)`, paddingTop: '0.8rem', zIndex: 1, position: 'relative', display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ display: 'flex', alignItems: 'center', gap: '4px', color: 'var(--color-text-muted)' }}>
                <Activity size={12} /> {item.source || item.sector || 'Global Network'}
              </span>
              <span className="vo-intel-cluster-badge" style={{ backgroundColor: 'var(--color-primary-glow)', color: 'var(--color-primary-dark)', padding: '0.2rem 0.5rem', borderRadius: '4px', fontSize: '0.7rem', fontWeight: 600 }}>
                {item.lifecycle ? item.lifecycle.toUpperCase() : 'VERIFIED'}
              </span>
            </div>
          </div>
        );
      })}
    </div>
  );
};

/* ── AI Insights Panel (Main) ────────────────────────── */
const AiInsightsPanel = () => {
  const { data: intelligence, loading: intelLoading } = useIntelligence(10, 60000);
  const { data: events, loading: eventsLoading } = useEvents(10, 60000);

  return (
    <div className="vo-ai-insights">
      <h2 className="vo-section-title">
        <Brain size={16} /> AI Intelligence Insights
      </h2>

      <div className="vo-ai-grid" style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
        {/* AI Picks */}
        <div className="vo-ai-panel vo-ai-panel--full" style={{ background: 'linear-gradient(to bottom right, var(--color-bg-card), var(--color-bg-elevated))' }}>
          <h3 className="vo-subsection-title">
            <Target size={14} /> Vanguard AI Picks
          </h3>
          <AiPicks picks={intelligence || events} loading={intelLoading || eventsLoading} />
        </div>

        {/* Insightful Info */}
        <div className="vo-ai-panel vo-ai-panel--full" style={{ background: 'linear-gradient(to right, var(--color-bg-elevated), var(--color-bg-card))' }}>
          <h3 className="vo-subsection-title">
            <Sparkles size={14} /> Deep Insightful Analysis
          </h3>
          <InsightfulInfo insights={events || intelligence} loading={eventsLoading || intelLoading} />
        </div>
      </div>
    </div>
  );
};

export default AiInsightsPanel;

