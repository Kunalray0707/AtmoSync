import React from 'react';

export default function Navbar({ activeTab, setActiveTab, liveStatus }) {
  const tabs = [
    { id: 'overview', label: 'Executive Overview', icon: '📊' },
    { id: 'fleet', label: 'Container Fleet Map', icon: '🌍' },
    { id: 'spoilage', label: 'Spoilage & Kinetics', icon: '🌡️' },
    { id: 'arbitrage', label: 'Arbitrage Rerouting', icon: '📈' },
    { id: 'ml', label: 'ML & SHAP Explainability', icon: '🧠' },
    { id: 'inspector', label: 'Dataset Inspector', icon: '🔍' },
    { id: 'reports', label: 'Reports & Export', icon: '📁' }
  ];

  return (
    <header className="navbar">
      <div className="brand-logo">
        <span>⚡ AtmoSync</span>
        <span className="brand-badge">ENTERPRISE v1.0</span>
      </div>

      <nav className="nav-tabs">
        {tabs.map(t => (
          <button
            key={t.id}
            className={`nav-tab ${activeTab === t.id ? 'active' : ''}`}
            onClick={() => setActiveTab(t.id)}
          >
            <span>{t.icon}</span>
            <span>{t.label}</span>
          </button>
        ))}
      </nav>

      <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
        <span className="badge badge-optimal">
          <span style={{ width: 8, height: 8, borderRadius: '50%', background: '#34D399', display: 'inline-block' }}></span>
          STREAMING LIVE
        </span>
      </div>
    </header>
  );
}
