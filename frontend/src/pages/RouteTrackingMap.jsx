import React from 'react';
import { MapContainer, TileLayer, Marker, Popup, Polyline } from 'react-leaflet';
import { MapPin, Navigation, Thermometer } from 'lucide-react';

const containerPositions = [
  { container_id: 'CONT-1001', lat: 51.95, lon: 4.14, commodity: 'Avocados', temp: 5.2, risk: 12.0, origin: 'Guayaquil', dest: 'Rotterdam' },
  { container_id: 'CONT-1002', lat: 36.67, lon: -121.65, commodity: 'Strawberries', temp: 8.5, risk: 68.0, origin: 'Salinas', dest: 'Chicago' },
  { container_id: 'CONT-1003', lat: 36.13, lon: -5.44, commodity: 'Bananas', temp: 13.8, risk: 15.0, origin: 'Algeciras', dest: 'London' },
  { container_id: 'CONT-1004', lat: 16.94, lon: 54.00, commodity: 'Blueberries', temp: 1.2, risk: 8.0, origin: 'Salalah', dest: 'Singapore' }
];

export default function RouteTrackingMap() {
  return (
    <div className="space-y-4">
      <div className="glass-panel p-4 rounded-2xl flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Navigation className="w-4 h-4 text-cyan-400" />
            Live Global Container GPS Tracking & Route Map
          </h3>
          <p className="text-xs text-slate-400">Mapbox / Leaflet live position vectors and weather overlays</p>
        </div>
        <div className="flex gap-2">
          <span className="px-2.5 py-1 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
            4 Ships Underway
          </span>
        </div>
      </div>

      <div className="glass-panel rounded-2xl overflow-hidden h-[500px] border border-slate-800 relative">
        <MapContainer center={[30.0, 0.0]} zoom={2} style={{ width: '100%', height: '100%' }}>
          <TileLayer
            url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
            attribution='&copy; <a href="https://carto.com/">CARTO</a>'
          />
          {containerPositions.map((c, idx) => (
            <Marker key={idx} position={[c.lat, c.lon]}>
              <Popup>
                <div className="text-xs p-1 text-slate-900">
                  <strong>{c.container_id}</strong> ({c.commodity})<br />
                  Temp: <strong>{c.temp}°C</strong> | Risk: <strong>{c.risk}%</strong><br />
                  Route: {c.origin} &rarr; {c.dest}
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      </div>
    </div>
  );
}
