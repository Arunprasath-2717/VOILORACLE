import { Search, Wifi, WifiOff } from 'lucide-react';
import { useState, useEffect } from 'react';
import { useLiveUpdates, useStatus } from '../../hooks/useApi';
import Logo from '../Logo';
import AnimatedNumber from '../AnimatedNumber';

const Header = ({ onLogoClick }) => {
  const [time, setTime] = useState(new Date());
  const [searchQuery, setSearchQuery] = useState('');
  const { connected, liveData } = useLiveUpdates();
  const { data: status } = useStatus(10000);

  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);

  const formattedTime = time.toLocaleTimeString('en-US', {
    hour: 'numeric',
    minute: '2-digit',
    hour12: true,
  });

  const formattedDate = time.toLocaleDateString('en-US', {
    weekday: 'short',
    month: 'short',
    day: 'numeric',
  });

  const systemStatus = status?.status || 'initializing';
  const statusColor = {
    healthy: 'var(--color-success)',
    degraded: 'var(--color-warning)',
    initializing: 'var(--color-muted-fg)',
  }[systemStatus] || 'var(--color-muted-fg)';

  return (
    <header className="vo-header">
      <div className="vo-header-inner">
        <div className="vo-header-brand" onClick={onLogoClick} style={{ cursor: 'pointer', display: 'flex', alignItems: 'center' }}>
          <Logo height="38px" />
        </div>

        {/* Center — Search */}
        <div className="vo-header-search-wrap">
          <div className="vo-header-search">
            <Search className="vo-search-icon" size={15} />
            <input
              type="text"
              placeholder="Search intelligence..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="vo-search-input"
            />
          </div>
        </div>

        {/* Right — Status */}
        <div className="vo-header-right">
          <div className="vo-header-status">
            {connected ? (
              <Wifi size={14} style={{ color: 'var(--color-success)' }} />
            ) : (
              <WifiOff size={14} style={{ color: 'var(--color-destructive)' }} />
            )}
            <span className="vo-status-dot" style={{ backgroundColor: statusColor }}>
              {connected && <span className="vo-status-ping" style={{ backgroundColor: statusColor }} />}
            </span>
            <span className="vo-status-label">
              {connected ? 'LIVE' : 'OFFLINE'}
            </span>
          </div>
          {liveData?.article_count != null && (
            <span className="vo-header-article-count">
              <AnimatedNumber end={liveData.article_count} suffix=" articles" />
            </span>
          )}
          <div className="vo-header-time">
            <span className="vo-time-date">{formattedDate}</span>
            <span className="vo-time-clock">{formattedTime}</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
