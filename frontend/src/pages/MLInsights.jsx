import React from 'react';
import { BrainCircuit, CheckCircle2, BarChart2 } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';

const shapImportanceData = [
  { feature: 'Container Temp (°C)', shapValue: 0.342 },
  { feature: 'Door Open Breach', shapValue: 0.221 },
  { feature: 'Thermal Drift (°C)', shapValue: 0.184 },
  { feature: 'Ambient Temp (°C)', shapValue: 0.125 },
  { feature: 'Humidity (%)', shapValue: 0.078 },
  { feature: 'Battery Level (%)', shapValue: 0.050 }
];

export default function MLInsights() {
  return (
    <div className="space-y-6">
      {/* Model Performance Overview */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="glass-panel p-4 rounded-xl">
          <span className="text-xs text-slate-400">ROC-AUC Score</span>
          <div className="text-2xl font-black text-cyan-400 mt-1">0.9842</div>
        </div>
        <div className="glass-panel p-4 rounded-xl">
          <span className="text-xs text-slate-400">Precision</span>
          <div className="text-2xl font-black text-emerald-400 mt-1">96.5%</div>
        </div>
        <div className="glass-panel p-4 rounded-xl">
          <span className="text-xs text-slate-400">Recall</span>
          <div className="text-2xl font-black text-indigo-400 mt-1">94.8%</div>
        </div>
        <div className="glass-panel p-4 rounded-xl">
          <span className="text-xs text-slate-400">5-Fold CV Accuracy</span>
          <div className="text-2xl font-black text-amber-400 mt-1">97.2%</div>
        </div>
      </div>

      {/* SHAP Feature Importance */}
      <div className="glass-panel p-5 rounded-2xl">
        <h3 className="text-sm font-bold text-white mb-1 flex items-center gap-2">
          <BrainCircuit className="w-4 h-4 text-cyan-400" />
          XGBoost Global SHAP Feature Importance Attribution
        </h3>
        <p className="text-xs text-slate-400 mb-4">Quantifies marginal contribution score of each sensor signal</p>

        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={shapImportanceData} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis type="number" stroke="#64748b" fontSize={11} />
              <YAxis dataKey="feature" type="category" stroke="#64748b" fontSize={11} width={130} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
              <Bar dataKey="shapValue" name="SHAP Importance" fill="#06b6d4" radius={[0, 4, 4, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
