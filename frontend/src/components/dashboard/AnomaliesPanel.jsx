import { AlertTriangle, ShieldAlert, Activity, Clock } from 'lucide-react';
import { useAnomalies, usePipelineRuns } from '../../hooks/useApi';
import AnimatedNumber from '../AnimatedNumber';

/* ── Pipeline Status ─────────────────────────────────── */
const PipelineStatus = ({ runs, loading }) => {
  if (loading) {
    return (
      <div className="vo-pipeline-status">
        {[1, 2, 3].map((i) => (
          <div key={i} className="vo-skeleton" style={{ height: '3rem', marginBottom: '0.5rem' }} />
        ))}
      </div>
    );
  }

  if (!runs || runs.length === 0) {
    return (
      <div className="vo-pipeline-status">
        <p className="vo-empty-state">No pipeline runs recorded yet.</p>
      </div>
    );
  }

  const statusColor = {
    success: '#10b981',
    error: '#ef4444',
    running: '#3b82f6',
  };

  return (
    <div className="vo-pipeline-status">
      {runs.map((run, i) => (
        <div key={i} className="vo-pipeline-run">
          <div className="vo-pipeline-run-dot" style={{ backgroundColor: statusColor[run.status] || '#6b7280' }} />
          <div className="vo-pipeline-run-info">
            <span className="vo-pipeline-run-status">{run.status}</span>
            <span className="vo-pipeline-run-time">
              <Clock size={11} />
              {run.started_at ? new Date(run.started_at).toLocaleString() : 'Unknown'}
            </span>
          </div>
          {run.articles_fetched != null && (
            <span className="vo-pipeline-run-stat">
              <AnimatedNumber end={run.articles_fetched} suffix=" fetched" />
            </span>
          )}
          {run.events_detected != null && (
            <span className="vo-pipeline-run-stat">
              <AnimatedNumber end={run.events_detected} suffix=" events" />
            </span>
          )}
        </div>
      ))}
    </div>
  );
};

/* ── Anomalies Panel (Main) ──────────────────────────── */
const AnomaliesPanel = () => {
  const { data: anomalies, loading: anomLoading } = useAnomalies(30000);
  const { data: pipelineRuns, loading: pipeLoading } = usePipelineRuns(5, 15000);

  const anomalyList = Array.isArray(anomalies) ? anomalies : anomalies?.anomalies || [];

  return (
    <div className="vo-anomalies">
      <h2 className="vo-section-title">
        <AlertTriangle size={16} /> Anomaly Detection & Pipeline Health
      </h2>

      <div className="vo-anomaly-grid">
        {/* Anomalies */}
        <div className="vo-ai-panel">
          <h3 className="vo-subsection-title">
            <ShieldAlert size={14} /> Detected Anomalies
          </h3>
          {anomLoading ? (
            <div>
              {[1, 2, 3].map((i) => (
                <div key={i} className="vo-skeleton" style={{ height: '4rem', marginBottom: '0.5rem' }} />
              ))}
            </div>
          ) : anomalyList.length === 0 ? (
            <div className="vo-anomaly-clear">
              <div className="vo-anomaly-clear-icon">✓</div>
              <p className="vo-anomaly-clear-text">No anomalies detected</p>
              <p className="vo-anomaly-clear-sub">All signals are within expected parameters.</p>
            </div>
          ) : (
            <div className="vo-anomaly-list">
              {anomalyList.map((anom, i) => {
                const severity = anom.severity || anom.score || 0;
                const severityColor = severity > 0.7 ? '#ef4444' : severity > 0.4 ? '#f59e0b' : '#10b981';

                return (
                  <div key={i} className="vo-anomaly-card">
                    <div className="vo-anomaly-severity" style={{ backgroundColor: severityColor }}>
                      {(severity * 100).toFixed(0)}%
                    </div>
                    <div className="vo-anomaly-info">
                      <span className="vo-anomaly-title">
                        {anom.title || anom.description || anom.type || 'Anomaly Detected'}
                      </span>
                      <span className="vo-anomaly-detail">
                        {anom.sector && `Sector: ${anom.sector}`}
                        {anom.type && ` · Type: ${anom.type}`}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Pipeline Health */}
        <div className="vo-ai-panel">
          <h3 className="vo-subsection-title">
            <Activity size={14} /> Pipeline Run History
          </h3>
          <PipelineStatus runs={pipelineRuns} loading={pipeLoading} />
        </div>
      </div>
    </div>
  );
};

export default AnomaliesPanel;
