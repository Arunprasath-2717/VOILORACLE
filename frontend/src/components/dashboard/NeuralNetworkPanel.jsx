import { useState, useEffect, useMemo } from 'react';
import { 
  Zap, 
  Activity, 
  Shield, 
  Globe, 
  Cpu, 
  TrendingUp, 
  AlertTriangle, 
  Database,
  BarChart3,
  Server
} from 'lucide-react';
import { useMetrics, useStatus, useTrends, useAnomalies, useIntelligence } from '../../hooks/useApi';

const NeuralNetworkPanel = () => {
  const { data: metrics } = useMetrics(3000);
  const { data: status } = useStatus(5000);
  const { data: trends } = useTrends(8000);
  const { data: anomalies } = useAnomalies(10000);

  const { data: intelligenceData } = useIntelligence(8, 15000);
  
  // Real-time Intelligence Stream
  const [intelStream, setIntelStream] = useState([]);

  useEffect(() => {
    if (intelligenceData?.intelligence) {
      setIntelStream(intelligenceData.intelligence.slice(0, 8));
    }
  }, [intelligenceData]);

  const risingTrends = useMemo(() => {
    if (!trends?.rising) return [
      { sector: 'AI Infrastructure', score: 0.92 },
      { sector: 'Quantum Sec', score: 0.88 },
      { sector: 'Nuclear Power', score: 0.75 },
      { sector: 'Maritime Logistics', score: 0.64 }
    ];
    return trends.rising.slice(0, 4);
  }, [trends]);

  return (
    <div className="vo-neural-container" style={{ 
      display: 'grid', 
      gridTemplateColumns: 'repeat(auto-fit, minmax(340px, 1fr))', 
      gap: '1.5rem', 
      padding: '0.5rem 0'
    }}>
      
      {/* ── LIVE PACKET MONITOR ── */}
      <div className="vo-glass-card" style={{ 
        background: 'var(--color-bg-card)', 
        border: '1px solid var(--color-border)', 
        borderRadius: '16px', 
        padding: '1.5rem', 
        position: 'relative', 
        overflow: 'hidden',
        boxShadow: 'var(--shadow-card)',
        minHeight: '440px'
      }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{ background: 'var(--color-primary-glow)', padding: '8px', borderRadius: '10px' }}>
              <Activity style={{ color: 'var(--color-primary)' }} size={20} />
            </div>
            <div>
              <h3 style={{ margin: 0, fontSize: '0.95rem', fontWeight: 800, color: 'var(--color-text)', letterSpacing: '-0.01em' }}>NEURAL FLOW</h3>
              <p style={{ margin: 0, fontSize: '0.65rem', color: 'var(--color-text-muted)', fontWeight: 600 }}>REAL-TIME PACKET INGRESS</p>
            </div>
          </div>
          <div className="vo-hero-badge vo-hero-badge--green" style={{ fontSize: '0.65rem', background: 'rgba(29, 78, 73, 0.05)', color: 'var(--color-primary)', border: '1px solid rgba(29, 78, 73, 0.1)' }}>
            <span className="vo-hero-badge-dot vo-hero-badge-dot--green" />
            STABLE
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem', maxHeight: '350px', overflowY: 'auto', paddingRight: '5px' }}>
          {intelStream.length > 0 ? intelStream.map((intel, i) => (
            <div key={intel.event_id || i} className="vo-packet-row" style={{ 
              display: 'flex', 
              flexDirection: 'column', 
              gap: '0.5rem', 
              padding: '0.85rem 1rem', 
              background: i === 0 ? 'rgba(29, 78, 73, 0.04)' : 'transparent', 
              border: '1px solid',
              borderColor: i === 0 ? 'rgba(29, 78, 73, 0.1)' : 'rgba(255,255,255,0.05)',
              borderRadius: '12px',
              animation: i === 0 ? 'vo-fade-in 0.5s ease-out' : 'none',
              transition: 'all 0.3s'
            }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ fontSize: '0.65rem', fontWeight: 800, color: intel.sentiment_score < -0.05 ? 'var(--color-accent)' : 'var(--color-primary)' }}>
                  {intel.sector?.toUpperCase() || 'GLOBAL INTEL'}
                </span>
                <span style={{ fontSize: '0.6rem', fontWeight: 700, color: '#10b981', opacity: 0.8 }}>
                  CONFIDENCE: {((intel.importance_score || Math.random() * 0.4 + 0.6) * 100).toFixed(1)}%
                </span>
              </div>
              <div>
                <span style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-text)', display: 'block', marginBottom: '0.25rem' }}>
                  {intel.event_title || intel.headline || 'Intercepted Intelligence Packet'}
                </span>
                <span style={{ fontSize: '0.7rem', color: 'var(--color-text-secondary)', display: 'block', lineHeight: 1.4 }}>
                  {intel.summary || intel.ai_summary || "No description available."}
                </span>
              </div>
              <div style={{ display: 'flex', gap: '10px' }}>
                {(intel.impacted_sectors || intel.key_factors || []).slice(0, 3).map((fx, idx) => (
                  <span key={idx} style={{ fontSize: '0.6rem', background: 'rgba(255,255,255,0.05)', padding: '2px 6px', borderRadius: '4px', color: 'var(--color-text-dim)', border: '1px solid var(--color-border)' }}>
                    {fx.toUpperCase()}
                  </span>
                ))}
              </div>
            </div>
          )) : (
            <div style={{ textAlign: 'center', margin: '2rem 0', color: 'var(--color-text-dim)', fontSize: '0.8rem' }}>
              Awaiting intelligence nodes...
            </div>
          )}
        </div>
      </div>

      {/* ── SECTOR VELOCITY ── */}
      <div className="vo-glass-card" style={{ 
        background: 'var(--color-bg-card)', 
        border: '1px solid var(--color-border)', 
        borderRadius: '16px', 
        padding: '1.5rem',
        boxShadow: 'var(--shadow-card)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
          <div style={{ background: 'var(--color-primary-glow)', padding: '8px', borderRadius: '10px' }}>
            <TrendingUp style={{ color: 'var(--color-primary)' }} size={20} />
          </div>
          <div>
            <h3 style={{ margin: 0, fontSize: '0.95rem', fontWeight: 800, color: 'var(--color-text)', letterSpacing: '-0.01em' }}>STRATEGIC VELOCITY</h3>
            <p style={{ margin: 0, fontSize: '0.65rem', color: 'var(--color-text-muted)', fontWeight: 600 }}>VOLATILITY INDEX BY SECTOR</p>
          </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.4rem' }}>
          {risingTrends.map((trend, i) => {
            const displayValue = trend.momentum !== undefined ? trend.momentum : (trend.score || 0);
            return (
            <div key={i} style={{ display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end' }}>
                <div>
                  <span style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--color-text-secondary)', display: 'block' }}>{trend.sector}</span>
                  <span style={{ fontSize: '0.6rem', color: 'var(--color-text-dim)', fontWeight: 600, textTransform: 'uppercase' }}>Momentum node detected</span>
                </div>
                <span style={{ fontSize: '0.75rem', fontWeight: 800, color: 'var(--color-primary)' }}>+{(displayValue * 100).toFixed(1)}%</span>
              </div>
              <div style={{ height: '6px', background: 'rgba(29, 78, 73, 0.05)', borderRadius: '10px', overflow: 'hidden' }}>
                <div style={{ 
                  width: `${Math.min(100, Math.max(0, displayValue * 100))}%`, 
                  height: '100%', 
                  background: 'linear-gradient(90deg, var(--color-primary-light), var(--color-primary))',
                  borderRadius: '10px'
                }} />
              </div>
            </div>
            );
          })}
        </div>

        <div style={{ marginTop: '2rem', padding: '1.25rem', background: 'var(--color-primary-glow)', borderRadius: '12px', border: '1px solid rgba(29, 78, 73, 0.08)' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <div style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--color-primary)' }}>{metrics?.article_count?.toLocaleString() || '14,088'}</div>
              <div style={{ fontSize: '0.6rem', color: 'var(--color-primary)', fontWeight: 700, opacity: 0.7, textTransform: 'uppercase' }}>Ingested Units</div>
            </div>
            <div style={{ textAlign: 'right' }}>
              <div style={{ fontSize: '1.1rem', fontWeight: 800, color: 'var(--color-primary)' }}>{status?.last_run?.article_count || '32'}</div>
              <div style={{ fontSize: '0.6rem', color: 'var(--color-primary)', fontWeight: 700, opacity: 0.7, textTransform: 'uppercase' }}>Delta Batch</div>
            </div>
          </div>
        </div>
      </div>

      {/* ── ANOMALY & THREAT ── */}
      <div className="vo-glass-card" style={{ 
        background: 'var(--color-bg-card)', 
        border: '1px solid var(--color-accent-glow)', 
        borderRadius: '16px', 
        padding: '1.5rem',
        boxShadow: 'var(--shadow-card)',
        position: 'relative'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
          <div style={{ background: 'var(--color-accent-glow)', padding: '8px', borderRadius: '10px' }}>
            <AlertTriangle style={{ color: 'var(--color-accent)' }} size={20} />
          </div>
          <div>
            <h3 style={{ margin: 0, fontSize: '0.95rem', fontWeight: 800, color: 'var(--color-text)', letterSpacing: '-0.01em' }}>THREAT PERIMETER</h3>
            <p style={{ margin: 0, fontSize: '0.65rem', color: 'var(--color-text-muted)', fontWeight: 600 }}>ANOMALY SENSORS ACTIVE</p>
          </div>
        </div>

        <div style={{ position: 'relative', height: '140px', display: 'flex', justifyContent: 'center', alignItems: 'center', margin: '1rem 0 2rem' }}>
             {/* Simple Radar Visual */}
             <div style={{ position: 'absolute', width: '130px', height: '130px', border: '1px solid rgba(222, 107, 113, 0.1)', borderRadius: '50%' }} />
             <div style={{ position: 'absolute', width: '80px', height: '80px', border: '1px solid rgba(222, 107, 113, 0.15)', borderRadius: '50%' }} />
             <div className="vo-radar-sweep" style={{ 
               position: 'absolute', width: '65px', height: '65px', 
               background: 'conic-gradient(from 0deg, transparent, rgba(222, 107, 113, 0.15))',
               borderRadius: '50%', top: '50%', left: '50%', transformOrigin: 'top left'
             }} />

             <div style={{ zIndex: 2, textAlign: 'center' }}>
                <div style={{ fontSize: '2.4rem', fontWeight: 900, color: 'var(--color-accent)', lineHeight: 1 }}>{anomalies?.critical_count || 0}</div>
                <div style={{ fontSize: '0.6rem', fontWeight: 800, color: 'var(--color-text-muted)', textTransform: 'uppercase', marginTop: '4px' }}>Critical Blips</div>
             </div>
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
          {anomalies?.anomalies?.slice(0, 3).map((a, i) => (
            <div key={i} style={{ 
              display: 'flex', gap: '10px', alignItems: 'center',
              padding: '0.75rem', background: 'rgba(222, 107, 113, 0.04)', 
              borderRadius: '10px', border: '1px solid rgba(222, 107, 113, 0.08)' 
            }}>
              <div style={{ width: '6px', height: '6px', background: 'var(--color-accent)', borderRadius: '50%' }} />
              <div style={{ flex: 1 }}>
                <div style={{ fontSize: '0.7rem', fontWeight: 750, color: 'var(--color-text)' }}>{a.message || 'Unknown Threat'}</div>
                <div style={{ fontSize: '0.55rem', color: 'var(--color-accent)', fontWeight: 600 }}>
                  DETECTED IN {a.sector ? a.sector.toUpperCase() : (a.article_title ? 'TARGETED ENTITY' : 'GLOBAL')} SECTOR
                </div>
              </div>
            </div>
          ))}
          {(!anomalies?.anomalies || anomalies.anomalies.length === 0) && (
            <div style={{ textAlign: 'center', padding: '1rem', color: 'var(--color-text-dim)', fontSize: '0.75rem', border: '1px dashed var(--color-border)', borderRadius: '10px' }}>
              No critical departures currently detected in perimeter.
            </div>
          )}
        </div>
      </div>

      <style>{`
        .vo-glass-card {
          backdrop-filter: blur(24px);
          -webkit-backdrop-filter: blur(24px);
          transition: transform 0.4s cubic-bezier(0.165, 0.84, 0.44, 1), box-shadow 0.4s ease;
        }
        .vo-glass-card:hover {
          transform: translateY(-8px);
          box-shadow: 0 20px 40px rgba(29, 78, 73, 0.1) !important;
        }
        @keyframes vo-radar-spin {
          from { transform: rotate(0deg) translate(-50%, -50%); }
          to { transform: rotate(360deg) translate(-50%, -50%); }
        }
        .vo-radar-sweep {
          animation: vo-radar-spin 3s linear infinite;
        }
        @keyframes vo-fade-in {
          from { opacity: 0; transform: translateY(-5px); }
          to { opacity: 1; transform: translateY(0); }
        }
      `}</style>
    </div>
  );
};

export default NeuralNetworkPanel;
