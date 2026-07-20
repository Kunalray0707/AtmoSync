import React from 'react';

export default function ReportsExport() {
  const handleDownload = (format) => {
    const backendUrl = `http://localhost:8000/api/export/${format}`;
    window.open(backendUrl, '_blank');
  };

  return (
    <div style={{ padding: '32px' }}>
      <div className="glass-card" style={{ marginBottom: '24px' }}>
        <h3 style={{ marginBottom: '8px', fontSize: '1.2rem', color: '#F8FAFC' }}>
          📁 Board Reports & Compliance Export Engine
        </h3>
        <p style={{ color: '#94A3B8', fontSize: '0.9rem', marginBottom: '24px' }}>
          Generate enterprise executive summaries, audit logs, and presentation decks across PDF, Excel, PPTX, and CSV formats.
        </p>

        <div className="dashboard-grid">
          <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <span style={{ fontSize: '2rem' }}>📄</span>
            <h4 style={{ color: '#60A5FA' }}>Executive PDF Report</h4>
            <p style={{ fontSize: '0.85rem', color: '#94A3B8' }}>
              Includes fleet spoilage summary, financial losses prevented, and high-risk container alerts.
            </p>
            <button className="btn-primary" onClick={() => handleDownload('pdf')} style={{ marginTop: 'auto' }}>
              Download PDF Report
            </button>
          </div>

          <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <span style={{ fontSize: '2rem' }}>📊</span>
            <h4 style={{ color: '#34D399' }}>Telemetry Excel Sheet</h4>
            <p style={{ fontSize: '0.85rem', color: '#94A3B8' }}>
              Raw high-frequency telemetry readings, temperature drift histories, and GPS tracks.
            </p>
            <button className="btn-primary" onClick={() => handleDownload('csv')} style={{ marginTop: 'auto' }}>
              Download Excel / CSV
            </button>
          </div>

          <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <span style={{ fontSize: '2rem' }}>💻</span>
            <h4 style={{ color: '#A78BFA' }}>Board PPTX Deck</h4>
            <p style={{ fontSize: '0.85rem', color: '#94A3B8' }}>
              Pre-built PowerPoint presentation slides for executive operations reviews.
            </p>
            <button className="btn-primary" onClick={() => handleDownload('pptx')} style={{ marginTop: 'auto' }}>
              Download PPTX Deck
            </button>
          </div>

          <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            <span style={{ fontSize: '2rem' }}>🔗</span>
            <h4 style={{ color: '#38BDF8' }}>JSON REST API Feed</h4>
            <p style={{ fontSize: '0.85rem', color: '#94A3B8' }}>
              Full raw JSON export formatted for Snowflake / Databricks pipeline ingestion.
            </p>
            <button className="btn-primary" onClick={() => handleDownload('json')} style={{ marginTop: 'auto' }}>
              Download JSON Feed
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
