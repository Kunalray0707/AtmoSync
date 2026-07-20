import React from 'react';
import KPICard from '../components/KPICard';
import { Truck, ThermometerSnowflake, DollarSign, TrendingUp, AlertTriangle, ShieldCheck } from 'lucide-react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, BarChart, Bar, CartesianGrid, Legend } from 'recharts';

const mockTrendData = [
  { time: '10:00', spoilageAvg: 12, financialLoss: 1400, arbitrageOpportunity: 3200 },
  { time: '10:05', spoilageAvg: 15, financialLoss: 2100, arbitrageOpportunity: 4800 },
  { time: '10:10', spoilageAvg: 18, financialLoss: 2800, arbitrageOpportunity: 6200 },
  { time: '10:15', spoilageAvg: 24, financialLoss: 4500, arbitrageOpportunity: 9400 },
  { time: '10:20', spoilageAvg: 29, financialLoss: 6200, arbitrageOpportunity: 12800 },
  { time: '10:25', spoilageAvg: 22, financialLoss: 4100, arbitrageOpportunity: 10500 },
  { time: '10:30', spoilageAvg: 19, financialLoss: 3200, arbitrageOpportunity: 8900 }
];

const commodityDistribution = [
  { commodity: 'Avocados', containers: 6, riskCount: 1 },
  { commodity: 'Strawberries', containers: 4, riskCount: 2 },
  { commodity: 'Bananas', containers: 4, riskCount: 0 },
  { commodity: 'Blueberries', containers: 3, riskCount: 1 },
  { commodity: 'Table Grapes', containers: 2, riskCount: 0 },
  { commodity: 'Leafy Greens', containers: 1, riskCount: 0 }
];

export default function ExecutiveDashboard({ summary }) {
  return (
    <div className="space-y-6">
      {/* Executive KPI Overview Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <KPICard
          title="Active Reefer Fleet"
          value={summary?.active_containers || 20}
          subtext="IoT Sensors Operational"
          icon={Truck}
          color="cyan"
          trend="+100% Online"
        />
        <KPICard
          title="High Spoilage Risk"
          value={summary?.high_spoilage_risk_containers || 3}
          subtext="Requires Immediate Action"
          icon={ThermometerSnowflake}
          color="rose"
          trend="Action Required"
        />
        <KPICard
          title="Arbitrage Profit Delta"
          value={`$${(summary?.identified_arbitrage_gain_usd || 18450).toLocaleString()}`}
          subtext="Identified Rerouting Gain"
          icon={TrendingUp}
          color="emerald"
          trend="+$18,450 Net"
        />
        <KPICard
          title="Projected Cargo Loss"
          value={`$${(summary?.total_projected_financial_loss_usd || 6200).toLocaleString()}`}
          subtext="Thermal Degradation Loss"
          icon={DollarSign}
          color="amber"
          trend="At Risk"
        />
      </div>

      {/* Primary Analytics Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Real-time Spoilage & Financial Loss Trend */}
        <div className="lg:col-span-2 glass-panel p-5 rounded-2xl">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-sm font-bold text-white">Live Spoilage Risk & Arbitrage Opportunity Trend</h3>
              <p className="text-xs text-slate-400">Continuous 1-second telemetry processing</p>
            </div>
            <span className="px-2.5 py-1 rounded-full text-[10px] bg-emerald-950 text-emerald-400 border border-emerald-800">
              Streaming Active
            </span>
          </div>

          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={mockTrendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis dataKey="time" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip
                  contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155', borderRadius: '8px' }}
                  labelStyle={{ color: '#f8fafc' }}
                />
                <Legend wrapperStyle={{ fontSize: '12px', paddingTop: '10px' }} />
                <Line type="monotone" dataKey="arbitrageOpportunity" name="Arbitrage Opportunity ($)" stroke="#10b981" strokeWidth={3} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="financialLoss" name="Financial Loss ($)" stroke="#f43f5e" strokeWidth={2} strokeDasharray="4 4" />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Commodity Distribution & Risk Breakdown */}
        <div className="glass-panel p-5 rounded-2xl">
          <h3 className="text-sm font-bold text-white mb-1">Commodity Fleet Breakdown</h3>
          <p className="text-xs text-slate-400 mb-4">Distribution by perishable type</p>

          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={commodityDistribution} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                <XAxis type="number" stroke="#64748b" fontSize={11} />
                <YAxis dataKey="commodity" type="category" stroke="#64748b" fontSize={11} width={85} />
                <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
                <Bar dataKey="containers" name="Active Reefers" fill="#06b6d4" radius={[0, 4, 4, 0]} />
                <Bar dataKey="riskCount" name="High Risk" fill="#f43f5e" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
