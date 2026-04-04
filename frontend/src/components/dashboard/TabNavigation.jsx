import { BarChart3, Radio, Grid3X3, TrendingUp, Zap, Globe2 } from 'lucide-react';

const tabs = [
  { id: 'overview', label: 'Overview', icon: BarChart3 },
  { id: 'geo-news', label: 'Geo Intelligence', icon: Globe2 },
  { id: 'live-feeds', label: 'Live Feed', icon: Radio },
  { id: 'sectors', label: 'Sectors', icon: Grid3X3 },
  { id: 'analytics', label: 'Analytics', icon: TrendingUp },
  { id: 'ai-insights', label: 'Neural Intelligence', icon: Zap },
];

const TabNavigation = ({ activeTab, onTabChange }) => (
  <div className="vo-tab-bar">
    <div className="vo-tab-bar-inner">
      <nav className="vo-tabs">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const isActive = activeTab === tab.id;
          return (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`vo-tab ${isActive ? 'vo-tab--active' : ''}`}
            >
              <Icon size={16} />
              <span className="vo-tab-label">{tab.label}</span>
              {isActive && <div className="vo-tab-indicator" />}
            </button>
          );
        })}
      </nav>
    </div>
  </div>
);

export default TabNavigation;
