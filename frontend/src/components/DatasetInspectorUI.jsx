import React, { useState } from 'react';

export default function DatasetInspectorUI() {
  const [profile, setProfile] = useState({
    source_file: "sample_reefer_telemetry.csv",
    summary: { row_count: 12500, column_count: 8, memory_usage_mb: 2.4, duplicate_rows: 0 },
    semantic_mapping: {
      timestamp: "recorded_at",
      container_id: "reefer_id",
      temperature: "temp_c",
      humidity: "rh_pct",
      commodity: "cargo_type",
      latitude: "geo_lat",
      longitude: "geo_lon",
      market_price: "spot_price"
    },
    quality_alerts: [
      { severity: "WARNING", message: "Column 'rh_pct' has 4.2% missing values. Auto-imputation enabled." }
    ]
  });

  return (
    <div style={{ padding: '32px' }}>
      <div className="glass-card" style={{ marginBottom: '24px' }}>
        <h3 style={{ marginBottom: '8px', fontSize: '1.2rem', color: '#F8FAFC' }}>
          🔍 Dynamic Adaptive Dataset Inspector & Schema Profiler
        </h3>
        <p style={{ color: '#94A3B8', fontSize: '0.9rem', marginBottom: '20px' }}>
          Upload custom logistics CSV / Parquet datasets to automatically inspect data types, infer telemetry semantics, and generate ingestion pipeline specs.
        </p>

        <div style={{ border: '2px dashed var(--border-glass-bright)', padding: '32px', borderRadius: '12px', textAlign: 'center', background: 'rgba(59, 130, 246, 0.04)', marginBottom: '24px' }}>
          <div style={{ fontSize: '2rem', marginBottom: '12px' }}>📁</div>
          <p style={{ fontWeight: 600, color: '#F8FAFC' }}>Drag & Drop Custom Dataset (CSV or Parquet)</p>
          <p style={{ color: '#94A3B8', fontSize: '0.85rem', marginTop: '4px' }}>Max file size 250MB • Automated Column Profiling & Semantic Auto-Mapping</p>
          <button className="btn-primary" style={{ marginTop: '16px' }}>Browse Local Files</button>
        </div>

        {profile && (
          <div>
            <h4 style={{ marginBottom: '12px', color: '#60A5FA' }}>
              Dataset Profiling Summary ({profile.source_file})
            </h4>
            <div className="dashboard-grid" style={{ marginBottom: '20px' }}>
              <div className="glass-card kpi-card" style={{ padding: '16px' }}>
                <span className="kpi-label">Row Count</span>
                <span className="kpi-val" style={{ fontSize: '1.5rem', color: '#F8FAFC' }}>{profile.summary.row_count?.toLocaleString()}</span>
              </div>
              <div className="glass-card kpi-card" style={{ padding: '16px' }}>
                <span className="kpi-label">Columns</span>
                <span className="kpi-val" style={{ fontSize: '1.5rem', color: '#60A5FA' }}>{profile.summary.column_count}</span>
              </div>
              <div className="glass-card kpi-card" style={{ padding: '16px' }}>
                <span className="kpi-label">Memory Footprint</span>
                <span className="kpi-val" style={{ fontSize: '1.5rem', color: '#38BDF8' }}>{profile.summary.memory_usage_mb} MB</span>
              </div>
              <div className="glass-card kpi-card" style={{ padding: '16px' }}>
                <span className="kpi-label">Duplicate Rows</span>
                <span className="kpi-val" style={{ fontSize: '1.5rem', color: '#34D399' }}>{profile.summary.duplicate_rows}</span>
              </div>
            </div>

            <h4 style={{ marginBottom: '12px', color: '#F8FAFC' }}>Inferred Telemetry Semantic Mapping</h4>
            <table className="data-table">
              <thead>
                <tr>
                  <th>Telemetry Semantic Role</th>
                  <th>Mapped Dataset Column</th>
                  <th>Inference Confidence</th>
                  <th>Status</th>
                </tr>
              </thead>
              <tbody>
                {Object.entries(profile.semantic_mapping).map(([role, col]) => (
                  <tr key={role}>
                    <td style={{ fontWeight: 600, color: '#60A5FA' }}>{role}</td>
                    <td style={{ fontFamily: 'var(--font-mono)' }}>{col || 'UNMAPPED'}</td>
                    <td><span style={{ color: '#34D399', fontWeight: 700 }}>98.5%</span></td>
                    <td><span className="badge badge-optimal">AUTO-MAPPED</span></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
}
