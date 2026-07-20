import React from 'react';
import { Search, Download, ShieldCheck, RefreshCw } from 'lucide-react';

export default function Header({ activeTab, onRefresh }) {
  return (
    <header className="h-16 glass-panel border-b border-slate-800 px-6 flex items-center justify-between sticky top-0 z-30">
      <div className="flex items-center gap-4">
        <h2 className="text-base font-bold text-white tracking-wide capitalize">
          {activeTab.replace('_', ' ')}
        </h2>
        <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-cyan-950 text-cyan-400 border border-cyan-800/60 uppercase">
          Production Mode
        </span>
      </div>

      <div className="flex items-center gap-3">
        {/* Global Action Refresh */}
        <button
          onClick={onRefresh}
          className="p-2 rounded-lg bg-slate-800/60 hover:bg-slate-700/60 text-slate-300 border border-slate-700/60 text-xs flex items-center gap-1.5 transition-colors"
          title="Refresh Data Snapshot"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Sync Ticks</span>
        </button>

        {/* User Profile Badge */}
        <div className="flex items-center gap-2 pl-3 border-l border-slate-800">
          <div className="w-7 h-7 rounded-full bg-gradient-to-r from-blue-600 to-indigo-600 flex items-center justify-center text-white text-xs font-bold shadow-sm">
            DE
          </div>
          <div className="hidden sm:block text-left text-xs">
            <p className="font-semibold text-slate-200 leading-tight">Principal Architect</p>
            <p className="text-[10px] text-slate-400 leading-tight">Snowflake & Kafka Engine</p>
          </div>
        </div>
      </div>
    </header>
  );
}
