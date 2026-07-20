import React from 'react';
import { Thermometer, Zap, ShieldAlert, Clock } from 'lucide-react';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const mockKineticsData = [
  { hour: '0h', optimumTemp: 5.0, containerTemp: 5.2, ArrheniusDecay: 1.0 },
  { hour: '12h', optimumTemp: 5.0, containerTemp: 5.8, ArrheniusDecay: 1.15 },
  { hour: '24h', optimumTemp: 5.0, containerTemp: 7.4, ArrheniusDecay: 1.48 },
  { hour: '36h', optimumTemp: 5.0, containerTemp: 9.1, ArrheniusDecay: 1.95 },
  { hour: '48h', optimumTemp: 5.0, containerTemp: 8.5, ArrheniusDecay: 1.72 },
  { hour: '60h', optimumTemp: 5.0, containerTemp: 6.2, ArrheniusDecay: 1.25 }
];

export default function SpoilageAnalytics() {
  return (
    <div className="space-y-6">
      <div className="glass-panel p-5 rounded-2xl">
        <div className="flex items-center justify-between mb-4">
          <div>
            <h3 className="text-sm font-bold text-white">Arrhenius Thermal Kinetics & Quality Decay Model</h3>
            <p className="text-xs text-slate-400">Scientific chemical reaction rate curve $k = A e^{{-E_a / RT}}$</p>
          </div>
          <span className="px-3 py-1 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800 text-xs font-bold">
            Arrhenius Engine Active
          </span>
        </div>

        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={mockKineticsData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="hour" stroke="#64748b" fontSize={11} />
              <YAxis stroke="#64748b" fontSize={11} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
              <Area type="monotone" dataKey="containerTemp" name="Container Micro-climate Temp (°C)" stroke="#f43f5e" fill="#f43f5e" fillOpacity={0.2} />
              <Area type="monotone" dataKey="optimumTemp" name="Optimum Target Temp (°C)" stroke="#10b981" fill="#10b981" fillOpacity={0.1} />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
