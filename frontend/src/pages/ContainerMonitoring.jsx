import React, { useState } from 'react';
import { Search, Filter, AlertTriangle, ShieldCheck, DoorOpen, BatteryCharging } from 'lucide-react';

export default function ContainerMonitoring({ containers }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCommodity, setSelectedCommodity] = useState('ALL');

  const filtered = (containers || []).filter(item => {
    const matchesSearch = item.container_id.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          item.shipment_id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesCommodity = selectedCommodity === 'ALL' || item.commodity.toUpperCase() === selectedCommodity.toUpperCase();
    return matchesSearch && matchesCommodity;
  });

  return (
    <div className="space-y-4">
      {/* Search and Filters Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 glass-panel p-4 rounded-xl">
        <div className="relative w-full sm:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search Container ID or Shipment..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-2 rounded-lg bg-slate-900/80 border border-slate-700/80 text-xs text-white placeholder-slate-400 focus:outline-none focus:border-cyan-500"
          />
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto justify-end">
          <span className="text-xs text-slate-400">Commodity:</span>
          <select
            value={selectedCommodity}
            onChange={(e) => setSelectedCommodity(e.target.value)}
            className="px-3 py-2 rounded-lg bg-slate-900/80 border border-slate-700/80 text-xs text-white focus:outline-none focus:border-cyan-500"
          >
            <option value="ALL">All Perishables</option>
            <option value="Avocados">Avocados</option>
            <option value="Strawberries">Strawberries</option>
            <option value="Bananas">Bananas</option>
            <option value="Blueberries">Blueberries</option>
            <option value="Table Grapes">Table Grapes</option>
            <option value="Leafy Greens">Leafy Greens</option>
          </select>
        </div>
      </div>

      {/* Containers Grid / Table */}
      <div className="glass-panel rounded-2xl overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead className="bg-slate-900/90 text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-800">
              <tr>
                <th className="p-3.5">Container / Shipment</th>
                <th className="p-3.5">Commodity</th>
                <th className="p-3.5">Temp (°C)</th>
                <th className="p-3.5">Humidity (%)</th>
                <th className="p-3.5">Spoilage Risk</th>
                <th className="p-3.5">RSL (Hours)</th>
                <th className="p-3.5">Sensors</th>
                <th className="p-3.5">Destination</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-slate-200">
              {filtered.map((item, idx) => {
                const isCritical = item.spoilage_risk_score_pct >= 50.0 || item.door_open;
                return (
                  <tr key={idx} className="hover:bg-slate-800/40 transition-colors">
                    <td className="p-3.5">
                      <div className="font-bold text-white">{item.container_id}</div>
                      <div className="text-[10px] text-slate-400">{item.shipment_id}</div>
                    </td>
                    <td className="p-3.5">
                      <span className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 font-medium">
                        {item.commodity}
                      </span>
                    </td>
                    <td className="p-3.5">
                      <span className={`font-bold ${item.temperature > 7.0 ? 'text-rose-400' : 'text-emerald-400'}`}>
                        {item.temperature}°C
                      </span>
                    </td>
                    <td className="p-3.5">{item.humidity}%</td>
                    <td className="p-3.5">
                      <div className="flex items-center gap-2">
                        <div className="w-16 bg-slate-800 h-2 rounded-full overflow-hidden">
                          <div
                            className={`h-full ${item.spoilage_risk_score_pct >= 50 ? 'bg-rose-500' : 'bg-emerald-400'}`}
                            style={{ width: `${Math.min(100, item.spoilage_risk_score_pct)}%` }}
                          />
                        </div>
                        <span className="font-semibold">{item.spoilage_risk_score_pct}%</span>
                      </div>
                    </td>
                    <td className="p-3.5 font-bold text-cyan-400">
                      {item.remaining_shelf_life_hours || 180} hrs
                    </td>
                    <td className="p-3.5">
                      <div className="flex items-center gap-1.5">
                        {item.door_open ? (
                          <span className="px-1.5 py-0.5 rounded bg-rose-950 text-rose-400 border border-rose-800 text-[10px] flex items-center gap-1">
                            <DoorOpen className="w-3 h-3" /> Unlatched
                          </span>
                        ) : (
                          <span className="px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] flex items-center gap-1">
                            <ShieldCheck className="w-3 h-3" /> Sealed
                          </span>
                        )}
                      </div>
                    </td>
                    <td className="p-3.5 text-slate-300">{item.destination}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
