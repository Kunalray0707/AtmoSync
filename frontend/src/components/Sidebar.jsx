import React from 'react';
import { 
  LayoutDashboard, 
  Truck, 
  ThermometerSnowflake, 
  TrendingUp, 
  Map, 
  LineChart, 
  BrainCircuit, 
  FileSpreadsheet, 
  Download, 
  Bell, 
  Layers
} from 'lucide-react';

const navItems = [
  { id: 'dashboard', label: 'Executive Dashboard', icon: LayoutDashboard },
  { id: 'containers', label: 'Container Monitoring', icon: Truck },
  { id: 'spoilage', label: 'Spoilage Analytics', icon: ThermometerSnowflake },
  { id: 'arbitrage', label: 'Arbitrage Rerouting', icon: TrendingUp },
  { id: 'map', label: 'Route Map Tracking', icon: Map },
  { id: 'forecast', label: 'Market Price Forecast', icon: LineChart },
  { id: 'ml', label: 'ML & SHAP Explainability', icon: BrainCircuit },
  { id: 'inspector', label: 'Dataset Inspector', icon: Layers },
  { id: 'reports', label: 'Reports & Export', icon: Download },
  { id: 'alerts', label: 'Alert Center', icon: Bell }
];

export default function Sidebar({ activeTab, setActiveTab }) {
  return (
    <aside className="w-64 glass-panel border-r border-slate-800 flex flex-col justify-between h-screen sticky top-0 z-40">
      <div>
        {/* Brand Logo Header */}
        <div className="p-5 flex items-center gap-3 border-b border-slate-800/80">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-cyan-500 to-blue-600 flex items-center justify-center text-slate-950 font-black text-xl shadow-lg shadow-cyan-500/20">
            A
          </div>
          <div>
            <h1 className="text-lg font-bold tracking-tight text-white flex items-center gap-1.5">
              Atmo<span className="text-cyan-400">Sync</span>
            </h1>
            <p className="text-[10px] font-medium text-slate-400 uppercase tracking-wider">Cold-Chain Arbitrage</p>
          </div>
        </div>

        {/* Navigation Menu */}
        <nav className="p-3 space-y-1 mt-2">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3 px-3.5 py-2.5 rounded-lg text-xs font-semibold transition-all duration-200 ${
                  isActive
                    ? 'bg-gradient-to-r from-cyan-500/20 to-blue-500/10 text-cyan-400 border border-cyan-500/30 shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/50'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-cyan-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Footer System Status */}
      <div className="p-4 border-t border-slate-800/80 m-3 rounded-xl bg-slate-900/60 text-xs text-slate-400">
        <div className="flex items-center gap-2 mb-1">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span className="font-semibold text-slate-200">Kafka Live Stream</span>
        </div>
        <p className="text-[10px] text-slate-400">30 Containers Active • 1-sec Ticks</p>
      </div>
    </aside>
  );
}
