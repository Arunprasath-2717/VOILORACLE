import React from 'react';

const Logo = ({ height = '40px', className = '', style = {} }) => {
  return (
    <div 
      className={`atlox-logo-container ${className}`}
      style={{ 
        display: 'flex', 
        alignItems: 'center', 
        gap: '12px',
        height: height,
        ...style 
      }}
    >
      <div className="atlox-logo-atom-wrapper">
        <svg 
          viewBox="0 0 100 100" 
          width={height} 
          height={height}
          fill="none" 
          xmlns="http://www.w3.org/2000/svg"
        >
          <defs>
            {/* Matt Finish Dark Gradient */}
            <linearGradient id="matt-dark-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#1e293b" />
              <stop offset="100%" stopColor="#0f172a" />
            </linearGradient>
            
            <linearGradient id="atom-grad" x1="0%" y1="0%" x2="100%" y2="100%">
              <stop offset="0%" stopColor="#38bdf8" />
              <stop offset="100%" stopColor="#818cf8" />
            </linearGradient>
          </defs>
          
          {/* Rotating Nucleus (Matt Finish) */}
          <g className="logo-nucleus-group">
            <circle 
              cx="50" cy="50" r="14" 
              fill="url(#matt-dark-grad)" 
              stroke="#334155"
              strokeWidth="1.5"
            />
            {/* Added details to nucleus to make rotation visible */}
            <path d="M44,50 L56,50 M50,44 L50,56" stroke="rgba(255,255,255,0.05)" strokeWidth="1" />
          </g>
          
          {/* Dark Transparent Orbital Lines */}
          <ellipse 
            cx="50" cy="50" rx="42" ry="16" 
            stroke="rgba(15, 23, 42, 0.3)" 
            strokeWidth="1.2" 
            className="logo-orbit"
          />
          <ellipse 
            cx="50" cy="50" rx="42" ry="16" 
            stroke="rgba(15, 23, 42, 0.3)" 
            strokeWidth="1.2" 
            transform="rotate(60 50 50)"
            className="logo-orbit"
          />
          <ellipse 
            cx="50" cy="50" rx="42" ry="16" 
            stroke="rgba(15, 23, 42, 0.3)" 
            strokeWidth="1.2" 
            transform="rotate(120 50 50)"
            className="logo-orbit"
          />
          
          {/* Electrons (Atoms) */}
          <circle r="3.5" fill="url(#atom-grad)" className="logo-electron logo-electron-1" />
          <circle r="3.5" fill="url(#atom-grad)" className="logo-electron logo-electron-2" />
          <circle r="3.5" fill="url(#atom-grad)" className="logo-electron logo-electron-3" />
        </svg>
      </div>
      
      <div className="atlox-logo-text-wrap">
        <span className="atlox-text-brand">ATLOX</span>
        <span className="atlox-text-tag">INTELLIGENCE</span>
      </div>

      <style dangerouslySetInnerHTML={{ __html: `
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@700;900&display=swap');

        .atlox-logo-container {
          cursor: pointer;
          user-select: none;
        }
        
        .atlox-logo-text-wrap {
          display: flex;
          flex-direction: column;
          justify-content: center;
        }
        
        .atlox-text-brand {
          font-family: 'Outfit', sans-serif;
          font-weight: 900;
          font-size: 1.6rem;
          letter-spacing: -0.02em;
          background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
          -webkit-background-clip: text;
          background-clip: text;
          color: transparent;
          line-height: 0.9;
        }
        
        .atlox-text-tag {
          font-family: 'Outfit', sans-serif;
          font-weight: 700;
          font-size: 0.55rem;
          letter-spacing: 0.5em;
          color: #334155;
          text-transform: uppercase;
          opacity: 0.6;
          margin-top: 2px;
        }
        
        .logo-nucleus-group {
          transform-origin: 50% 50%;
          animation: nucleus-rotate 8s linear infinite;
        }
        
        @keyframes nucleus-rotate {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }

        .logo-electron {
          animation: electron-orbit 3s linear infinite;
        }

        .logo-electron-1 {
          offset-path: path('M 8,50 A 42,16 0 1,0 92,50 A 42,16 0 1,0 8,50');
          animation-duration: 3s;
        }

        .logo-electron-2 {
          offset-path: path('M 29,21.7 A 42,16 60 1,0 71,78.3 A 42,16 60 1,0 29,21.7');
          animation-duration: 4s;
          animation-delay: -1s;
        }

        .logo-electron-3 {
          offset-path: path('M 71,21.7 A 42,16 120 1,0 29,78.3 A 42,16 120 1,0 71,21.7');
          animation-duration: 5s;
          animation-delay: -2s;
        }

        @keyframes electron-orbit {
          from { offset-distance: 0%; }
          to { offset-distance: 100%; }
        }

        .atlox-logo-atom-wrapper svg {
          overflow: visible;
        }
      `}} />
    </div>
  );
};

export default Logo;
