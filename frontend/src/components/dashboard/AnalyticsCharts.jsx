import { TrendingUp } from 'lucide-react';
import {
  AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend,
} from 'recharts';
import { useMetrics, useEvents, useImpacts, useArticles } from '../../hooks/useApi';
import { useMemo } from 'react';

const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#f97316', '#6b7280', '#06b6d4'];

/* ── Custom Tooltip ──────────────────────────────────── */
const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="vo-chart-tooltip">
      <p className="vo-chart-tooltip-label">{label}</p>
      {payload.map((p, i) => (
        <p key={i} style={{ color: p.color }}>
          {p.name}: <strong>{p.value}</strong>
        </p>
      ))}
    </div>
  );
};

/* ── Chart Card ──────────────────────────────────────── */
const ChartCard = ({ title, children, loading }) => (
  <div className="vo-chart-card">
    <h3 className="vo-chart-title">{title}</h3>
    <div className="vo-chart-body">
      {loading ? (
        <div className="vo-skeleton" style={{ height: '100%', borderRadius: '0.5rem' }} />
      ) : (
        children
      )}
    </div>
  </div>
);

/* ── Analytics Panel ─────────────────────────────────── */
const AnalyticsCharts = () => {
  const { data: metrics, loading: metricsLoading } = useMetrics(15000);
  const { data: events, loading: eventsLoading } = useEvents(50, 15000);
  const { data: impacts, loading: impactsLoading } = useImpacts(30000);
  const { data: articles, loading: articlesLoading } = useArticles(100, 15000);

  /* Compute sentiment distribution pie data */
  const sentimentPieData = useMemo(() => {
    if (!metrics?.sentiment_distribution) return [];
    const sd = metrics.sentiment_distribution;
    return [
      { name: 'Positive', value: sd.Positive || 0 },
      { name: 'Neutral', value: sd.Neutral || 0 },
      { name: 'Negative', value: sd.Negative || 0 },
    ].filter(d => d.value > 0);
  }, [metrics]);

  /* Compute sector impact bar data */
  const sectorBarData = useMemo(() => {
    if (!impacts) return [];
    return impacts
      .map((imp) => ({
        name: imp.sector,
        bullish: imp.bullish || 0,
        bearish: imp.bearish || 0,
        total: (imp.bullish || 0) + (imp.bearish || 0)
      }))
      .sort((a, b) => b.total - a.total)
      .slice(0, 10); // Show top 10 sectors to avoid clutter
  }, [impacts]);

  /* Compute event size distribution */
  const eventSizeData = useMemo(() => {
    if (!events) return [];
    return events
      .sort((a, b) => b.size - a.size)
      .slice(0, 10)
      .map((ev) => ({
        name: ev.label?.substring(0, 25) || 'Event',
        size: ev.size,
        importance: ((ev.importance_score || 0) * 100).toFixed(0),
      }));
  }, [events]);

  /* Compute article source distribution */
  const sourceData = useMemo(() => {
    if (!articles) return [];
    const counts = {};
    articles.forEach((a) => {
      const src = a.source || 'Unknown';
      counts[src] = (counts[src] || 0) + 1;
    });
    return Object.entries(counts)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 8)
      .map(([name, value]) => ({ name, value }));
  }, [articles]);

  const sentimentColors = ['#10b981', '#6b7280', '#ef4444'];

  return (
    <div className="vo-analytics">
      <h2 className="vo-section-title">
        <TrendingUp size={16} /> Analytics Dashboard
      </h2>

      <div className="vo-charts-grid">
        {/* Sentiment Distribution Pie */}
        <ChartCard title="Sentiment Distribution" loading={metricsLoading}>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={sentimentPieData}
                cx="50%"
                cy="50%"
                innerRadius={50}
                outerRadius={80}
                dataKey="value"
                nameKey="name"
                paddingAngle={4}
                stroke="none"
                isAnimationActive={true}
                animationBegin={0}
                animationDuration={1500}
                animationEasing="ease-out"
              >
                {sentimentPieData.map((_, i) => (
                  <Cell key={i} fill={sentimentColors[i]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend verticalAlign="bottom" iconType="circle" />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>

        {/* Sector Impact Bar */}
        <ChartCard title="Sector Impact Analysis" loading={impactsLoading}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={sectorBarData} layout="vertical" margin={{ top: 10, right: 30, left: 20, bottom: 5 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.15)" horizontal={true} vertical={false} />
              <XAxis type="number" tick={{ fontSize: 11, fill: '#94a3b8' }} axisLine={false} tickLine={false} />
              <YAxis dataKey="name" type="category" width={110} tick={{ fontSize: 11, fill: '#94a3b8', fontWeight: 500 }} tickFormatter={(val) => val.length > 16 ? val.substring(0, 16) + '...' : val} interval={0} axisLine={false} tickLine={false} />
              <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(148,163,184,0.05)' }} />
              <Bar dataKey="bullish" name="Bullish" fill="#10b981" radius={[0, 4, 4, 0]} isAnimationActive={true} animationBegin={0} animationDuration={1500} animationEasing="ease-out" />
              <Bar dataKey="bearish" name="Bearish" fill="#ef4444" radius={[0, 4, 4, 0]} isAnimationActive={true} animationBegin={0} animationDuration={1500} animationEasing="ease-out" />
              <Legend iconType="circle" wrapperStyle={{ paddingTop: '10px' }} />
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        {/* Event Clusters Bar */}
        <ChartCard title="Top Event Clusters" loading={eventsLoading}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={eventSizeData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(148,163,184,0.15)" />
              <XAxis dataKey="name" tick={{ fontSize: 9, fill: '#94a3b8' }} angle={-25} textAnchor="end" height={60} />
              <YAxis tick={{ fontSize: 11, fill: '#94a3b8' }} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="size" name="Articles" radius={[6, 6, 0, 0]} isAnimationActive={true} animationBegin={0} animationDuration={1500} animationEasing="ease-out">
                {eventSizeData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </ChartCard>

        {/* Source Distribution */}
        <ChartCard title="Source Distribution" loading={articlesLoading}>
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={sourceData}
                cx="50%"
                cy="50%"
                outerRadius={80}
                dataKey="value"
                nameKey="name"
                paddingAngle={2}
                stroke="none"
                isAnimationActive={true}
                animationBegin={0}
                animationDuration={1500}
                animationEasing="ease-out"
              >
                {sourceData.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip content={<CustomTooltip />} />
              <Legend verticalAlign="bottom" iconType="circle" />
            </PieChart>
          </ResponsiveContainer>
        </ChartCard>
      </div>
    </div>
  );
};

export default AnalyticsCharts;
