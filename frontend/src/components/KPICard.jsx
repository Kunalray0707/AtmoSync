import React from 'react';

export default function KPICard({ title, value, subtext, icon: Icon, color = 'cyan', trend }) {
  const colorStyles = {
    cyan: 'from-cyan-500/10 to-blue-500/5 border-cyan-500/30 text-cyan-400',
    rose: 'from-rose-500/10 to-red-500/5 border-rose-500/30 text-rose-400',
    emerald: 'from-emerald-500/10 to-teal-500/5 border-emerald-500/30 text-emerald-400',
    amber: 'from-amber-500/10 to-orange-500/5 border-amber-500/30 text-amber-400',
    indigo: 'from-indigo-500/10 to-purple-500/5 border-indigo-500/30 text-indigo-400'
  };

  return (
    <div className={`p-4 rounded-xl glass-card bg-gradient-to-br ${colorStyles[color]} relative overflow-hidden`}>
      <div className="flex items-center justify-between mb-2">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{title}</span>
        {Icon && <Icon className={`w-5 h-5 ${colorStyles[color].split(' ').pop()}`} />}
      </div>
      <div className="text-2xl font-black text-white tracking-tight mb-1">
        {value}
      </div>
      <div className="flex items-center justify-between text-[11px] text-slate-400">
        <span>{subtext}</span>
        {trend && (
          <span className={`font-semibold ${trend.startsWith('+') ? 'text-emerald-400' : 'text-rose-400'}`}>
            {trend}
          </span>
        )}
      </div>
    </div>
  );
}
