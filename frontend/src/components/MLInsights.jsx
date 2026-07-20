import React, { useState } from 'react';

export default function MLInsights() {
  const globalImportance = [
    { feature: 'Arrhenius Quality Decay Ratio', importance: 34.0, category: 'Kinetics', color: '#3B82F6' },
    { feature: 'Temperature Excursion Delta (°C)', importance: 28.0, category: 'Thermal', color: '#EF4444' },
    { feature: 'Door Breach Status', importance: 16.0, category: 'Security', color: '#F59E0B' },
    { feature: 'Humidity Drift (%)', importance: 11.0, category: 'Environment', color: '#06B6D4' },
    { feature: 'Elapsed Route Duration (hrs)', importance: 7.0, category: 'Transit', color: '#8B5CF6' },
    { feature: 'Ambient External Temperature', importance: 4.0, category: 'Weather', color: '#10B981' }
  ];

  const shapWaterfall = [
    { feature: "Base Fleet Average Risk", shap_value: 15.0, is_base: true },
    { feature: "Thermal Excursion Impact", shap_value: 28.5, contribution: "INCREASES_RISK" },
    { feature: "Arrhenius Kinetic Acceleration", shap_value: 22.0, contribution: "INCREASES_RISK" },
    { feature: "Door Breach Penalty", shap_value: 22.5, contribution: "INCREASES_RISK" },
    { feature: "Humidity Instability", shap_value: 4.5, contribution: "INCREASES_RISK" }
  ];

  return (
    <div style={{ padding: '32px' }}>
      <div className="equal-two-col">
        {/* Global SHAP Feature Importance */}
        <div className="glass-card">
          <h3 style={{ marginBottom: '8px', fontSize: '1.1rem', color: '#F8FAFC' }}>
            🧠 Global XGBoost Feature Importance
          </h3>
          <p style={{ color: '#94A3B8', fontSize: '0.85rem', marginBottom: '20px' }}>
            Relative predictive weight across 45,000 historical cold-chain shipment records (AUC: 0.942).
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            {globalImportance.map(item => (
              <div key={item.feature}>
                <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px', fontSize: '0.85rem' }}>
                  <span style={{ fontWeight: 600, color: '#F8FAFC' }}>{item.feature}</span>
                  <span style={{ fontFamily: 'var(--font-mono)', fontWeight: 700, color: item.color }}>
                    {item.importance}%
                  </span>
                </div>
                <div style={{ width: '100%', height: '8px', background: 'rgba(255,255,255,0.06)', borderRadius: '4px', overflow: 'hidden' }}>
                  <div style={{ width: `${item.importance}%`, height: '100%', background: item.color, borderRadius: '4px' }}></div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Local SHAP Waterfall Prediction Explanation */}
        <div className="glass-card">
          <h3 style={{ marginBottom: '8px', fontSize: '1.1rem', color: '#F8FAFC' }}>
            📊 Local SHAP Waterfall Attribution (CONT-1002)
          </h3>
          <p style={{ color: '#94A3B8', fontSize: '0.85rem', marginBottom: '20px' }}>
            Deconstructing local prediction drivers for 92.5% Spoilage Risk score.
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {shapWaterfall.map((s, idx) => (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  justify: 'space-between',
                  alignItems: 'center',
                  padding: '10px 14px',
                  background: s.is_base ? 'rgba(59, 130, 246, 0.12)' : 'rgba(255, 255, 255, 0.03)',
                  border: s.is_base ? '1px solid rgba(59, 130, 246, 0.3)' : '1px solid rgba(255, 255, 255, 0.05)',
                  borderRadius: '8px'
                }}
              >
                <span style={{ fontSize: '0.875rem', fontWeight: s.is_base ? 700 : 500 }}>{s.feature}</span>
                <span
                  style={{
                    fontFamily: 'var(--font-mono)',
                    fontWeight: 700,
                    color: s.is_base ? '#60A5FA' : '#F87171'
                  }}
                >
                  +{s.shap_value}%
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
