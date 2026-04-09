import { BarChart3, Globe2, Radio, TrendingUp, Grid3X3 } from 'lucide-react';

const tabs = [
  { id: 'overview', label: 'Overview', icon: BarChart3 },
  { id: 'geo-news', label: 'Geo Intelligence', icon: Globe2 },
  { id: 'live-feeds', label: 'Live Feed', icon: Radio },
  { id: 'sectors', label: 'Sector Intel', icon: Grid3X3 },
  { id: 'analytics', label: 'Analytics', icon: TrendingUp },
];

const TabNavigation = ({ activeTab, onTabChange }) => (
  <nav className="vo-tab-bar">
    <div className="vo-tab-bar-inner">
      <div className="vo-tabs">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            className={`vo-tab ${activeTab === tab.id ? 'vo-tab--active' : ''}`}
            onClick={() => onTabChange(tab.id)}
          >
            <tab.icon size={16} />
            <span className="vo-tab-label">{tab.label}</span>
            {activeTab === tab.id && <div className="vo-tab-indicator" />}
          </button>
        ))}
      </div>
    </div>
  </nav>
);

export default TabNavigation;
