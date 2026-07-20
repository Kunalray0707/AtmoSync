import React, { useState } from 'react';

export default function ContainerFleetMap({ containers }) {
  const [selectedContainer, setSelectedContainer] = useState(containers[0] || null);

  return (
    <div style={{ padding: '32px' }}>
      <div className="two-col-grid">
        {/* Fleet List Panel */}
        <div className="glass-card">
          <h3 style={{ marginBottom: '16px', fontSize: '1.1rem', color: '#F8FAFC' }}>
            🌍 Fleet Geo-Location & Route Monitor
          </h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', maxHeight: '550px', overflowY: 'auto' }}>
            {containers.map(c => {
              const isSelected = selectedContainer?.container_id === c.container_id;
              return (
                <div
                  key={c.container_id}
                  onClick={() => setSelectedContainer(c)}
                  style={{
                    background: isSelected ? 'rgba(59, 130, 246, 0.15)' : 'rgba(255, 255, 255, 0.03)',
                    border: isSelected ? '1px solid #3B82F6' : '1px solid rgba(255, 255, 255, 0.08)',
                    borderRadius: '12px',
                    padding: '16px',
                    cursor: 'pointer',
                    transition: 'all 0.2s ease'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '6px' }}>
                    <span style={{ fontWeight: 700, fontFamily: 'var(--font-mono)' }}>{c.container_id} ({c.commodity})</span>
                    <span className={`badge ${c.temperature > 8 ? 'badge-critical' : 'badge-optimal'}`}>
                      {c.temperature}°C
                    </span>
                  </div>
                  <div style={{ fontSize: '0.85rem', color: '#94A3B8', display: 'flex', justifyContent: 'space-between' }}>
                    <span>📍 {c.origin} ➔ {c.destination}</span>
                    <span>🏎️ {c.gps_speed_kmh} km/h</span>
                  </div>
                  <div style={{ marginTop: '8px', fontSize: '0.8rem', color: '#64748B', display: 'flex', justifyContent: 'space-between' }}>
                    <span>Lat: {c.latitude?.toFixed(4)}, Lon: {c.longitude?.toFixed(4)}</span>
                    <span>ETA: {c.remaining_distance_km} km remaining</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Selected Detail Panel */}
        <div className="glass-card">
          {selectedContainer ? (
            <div>
              <h3 style={{ marginBottom: '16px', color: '#60A5FA', fontFamily: 'var(--font-mono)' }}>
                {selectedContainer.container_id} Route Telemetry
              </h3>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                <div style={{ padding: '12px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px' }}>
                  <span style={{ color: '#94A3B8', fontSize: '0.8rem' }}>CARGO COMMODITY</span>
                  <div style={{ fontWeight: 700, fontSize: '1.1rem' }}>{selectedContainer.commodity}</div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px' }}>
                  <div style={{ padding: '12px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px' }}>
                    <span style={{ color: '#94A3B8', fontSize: '0.8rem' }}>MICRO-CLIMATE TEMP</span>
                    <div style={{ fontWeight: 700, fontSize: '1.2rem', color: selectedContainer.temperature > 8 ? '#EF4444' : '#10B981' }}>
                      {selectedContainer.temperature}°C
                    </div>
                  </div>
                  <div style={{ padding: '12px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px' }}>
                    <span style={{ color: '#94A3B8', fontSize: '0.8rem' }}>HUMIDITY</span>
                    <div style={{ fontWeight: 700, fontSize: '1.2rem', color: '#38BDF8' }}>
                      {selectedContainer.humidity}%
                    </div>
                  </div>
                </div>

                <div style={{ padding: '12px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px' }}>
                  <span style={{ color: '#94A3B8', fontSize: '0.8rem' }}>DOOR STATUS</span>
                  <div style={{ fontWeight: 700, color: selectedContainer.door_open ? '#EF4444' : '#10B981' }}>
                    {selectedContainer.door_open ? '⚠️ BREACH / OPEN' : '🔒 SEALED / CLOSED'}
                  </div>
                </div>

                <div style={{ padding: '12px', background: 'rgba(0,0,0,0.3)', borderRadius: '8px' }}>
                  <span style={{ color: '#94A3B8', fontSize: '0.8rem' }}>AMBIENT WEATHER</span>
                  <div style={{ fontWeight: 600 }}>{selectedContainer.ambient_weather}</div>
                </div>

                <button className="btn-primary" style={{ width: '100%', justifyContent: 'center', marginTop: '12px' }}>
                  ⚡ Trigger Instant Reroute Simulation
                </button>
              </div>
            </div>
          ) : (
            <p style={{ color: '#94A3B8' }}>Select a container from the list to view route telemetry.</p>
          )}
        </div>
      </div>
    </div>
  );
}
