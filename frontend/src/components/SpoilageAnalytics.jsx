import React from 'react';

export default function SpoilageAnalytics({ containers }) {
  return (
    <div style={{ padding: '32px' }}>
      <div className="glass-card" style={{ marginBottom: '24px' }}>
        <h3 style={{ marginBottom: '8px', fontSize: '1.2rem', color: '#F8FAFC' }}>
          🧪 Arrhenius Micro-Climate Decay & Thermal Kinetics
        </h3>
        <p style={{ color: '#94A3B8', fontSize: '0.9rem', marginBottom: '20px' }}>
          Calculates dynamic quality loss based on activation energy (Ea), thermal integral history, and humidity drift.
        </p>

        <table className="data-table">
          <thead>
            <tr>
              <th>Container ID</th>
              <th>Commodity</th>
              <th>Temp (°C)</th>
              <th>Arrhenius Ratio</th>
              <th>RSL (Hours)</th>
              <th>RSL (Days)</th>
              <th>Freshness Score</th>
              <th>Risk Assessment</th>
            </tr>
          </thead>
          <tbody>
            {containers.map(c => {
              const metrics = c.spoilage_metrics || {};
              const rslHours = metrics.remaining_shelf_life_hours || 140.0;
              const rslDays = metrics.remaining_shelf_life_days || 5.8;
              const ratio = metrics.arrhenius_decay_ratio || 1.1;
              const freshness = metrics.freshness_index_pct || 88.0;

              return (
                <tr key={c.container_id}>
                  <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 600 }}>{c.container_id}</td>
                  <td>{c.commodity}</td>
                  <td style={{ fontWeight: 700, color: c.temperature > 8 ? '#EF4444' : '#34D399' }}>
                    {c.temperature}°C
                  </td>
                  <td style={{ fontFamily: 'var(--font-mono)', color: ratio > 1.5 ? '#F87171' : '#60A5FA' }}>
                    {ratio}x base
                  </td>
                  <td style={{ fontWeight: 700 }}>{rslHours} hrs</td>
                  <td>{rslDays} days</td>
                  <td>
                    <span style={{ fontWeight: 700, color: freshness < 50 ? '#EF4444' : '#10B981' }}>
                      {freshness}%
                    </span>
                  </td>
                  <td>
                    <span className={`badge ${freshness < 50 ? 'badge-critical' : 'badge-optimal'}`}>
                      {freshness < 50 ? 'HIGH DECAY' : 'OPTIMAL'}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
