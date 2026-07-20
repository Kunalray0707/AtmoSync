import React from 'react';

export default function ExecutiveOverview({ containers, summary }) {
  const totalSaved = summary?.total_loss_prevented_usd || 452800;
  const criticalCount = containers.filter(c => c.spoilage_metrics?.spoilage_category === 'CRITICAL_SPOILAGE_RISK').length;

  return (
    <div style={{ padding: '32px' }}>
      <div className="dashboard-grid">
        <div className="glass-card kpi-card">
          <span className="kpi-label">Active Monitored Fleet</span>
          <span className="kpi-val" style={{ color: '#60A5FA' }}>{containers.length || 10} Reefers</span>
          <span className="kpi-sub">🟢 100% Telemetry Online</span>
        </div>

        <div className="glass-card kpi-card">
          <span className="kpi-label">Potential Loss Prevented</span>
          <span className="kpi-val" style={{ color: '#34D399' }}>${totalSaved.toLocaleString()}</span>
          <span className="kpi-sub">📈 +18.4% Arbitrage Margin Delta</span>
        </div>

        <div className="glass-card kpi-card">
          <span className="kpi-label">Critical Spoilage Alerts</span>
          <span className="kpi-val" style={{ color: criticalCount > 0 ? '#F87171' : '#34D399' }}>
            {criticalCount} Active
          </span>
          <span className="kpi-sub">⚠️ Excursion Threshold Alerts</span>
        </div>

        <div className="glass-card kpi-card">
          <span className="kpi-label">Avg Fleet Freshness Index</span>
          <span className="kpi-val" style={{ color: '#FBBF24' }}>88.4%</span>
          <span className="kpi-sub">⏳ Baseline Arrhenius Decay</span>
        </div>
      </div>

      <div className="two-col-grid">
        <div className="glass-card">
          <h3 style={{ marginBottom: '16px', fontSize: '1.1rem', color: '#F8FAFC' }}>
            🚨 Live Cold-Chain Excursion Stream
          </h3>
          <table className="data-table">
            <thead>
              <tr>
                <th>Container ID</th>
                <th>Commodity</th>
                <th>Temp (°C)</th>
                <th>Humidity (%)</th>
                <th>Freshness Index</th>
                <th>Risk Category</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {containers.slice(0, 6).map(c => {
                const metric = c.spoilage_metrics || {};
                const cat = metric.spoilage_category || 'OPTIMAL';
                const badgeClass = cat === 'CRITICAL_SPOILAGE_RISK' ? 'badge-critical' : (cat === 'HIGH_RISK' ? 'badge-moderate' : 'badge-optimal');

                return (
                  <tr key={c.container_id}>
                    <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 600 }}>{c.container_id}</td>
                    <td>{c.commodity}</td>
                    <td style={{ fontWeight: 700, color: c.temperature > 8 ? '#F87171' : '#F8FAFC' }}>
                      {c.temperature}°C
                    </td>
                    <td>{c.humidity}%</td>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                        <div style={{ flex: 1, height: 6, background: 'rgba(255,255,255,0.1)', borderRadius: 3, overflow: 'hidden' }}>
                          <div style={{ width: `${metric.freshness_index_pct || 85}%`, height: '100%', background: (metric.freshness_index_pct || 85) < 50 ? '#EF4444' : '#10B981' }}></div>
                        </div>
                        <span>{metric.freshness_index_pct || 85}%</span>
                      </div>
                    </td>
                    <td><span className={`badge ${badgeClass}`}>{cat.replace('_', ' ')}</span></td>
                    <td>
                      <button className="btn-outline" style={{ padding: '4px 10px', fontSize: '0.75rem' }}>
                        Inspect
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        <div className="glass-card">
          <h3 style={{ marginBottom: '16px', fontSize: '1.1rem', color: '#F8FAFC' }}>
            💡 Recommended Arbitrage Actions
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <div style={{ background: 'rgba(59, 130, 246, 0.1)', border: '1px solid rgba(59, 130, 246, 0.25)', padding: '16px', borderRadius: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ fontWeight: 700, color: '#60A5FA' }}>Reroute CONT-1002 (Strawberries)</span>
                <span className="badge badge-optimal">+$22,400 Gain</span>
              </div>
              <p style={{ fontSize: '0.85rem', color: '#94A3B8', lineHeight: 1.4 }}>
                Reroute from Rotterdam to Hamburg port due to temp spike (+4.2°C). Hamburg spot market price is $5,100/ton vs Rotterdam $4,800/ton.
              </p>
            </div>

            <div style={{ background: 'rgba(16, 185, 129, 0.1)', border: '1px solid rgba(16, 185, 129, 0.25)', padding: '16px', borderRadius: '12px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '8px' }}>
                <span style={{ fontWeight: 700, color: '#34D399' }}>Reroute CONT-1005 (Salmon)</span>
                <span className="badge badge-optimal">+$14,200 Gain</span>
              </div>
              <p style={{ fontSize: '0.85rem', color: '#94A3B8', lineHeight: 1.4 }}>
                Remaining shelf life: 3.2 days. Redirecting to Le Havre saves cargo before total freshness degradation.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
