import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';

const mockPriceForecast = [
  { day: 'Day 1', Avocados: 3.40, Strawberries: 5.80, Blueberries: 7.20 },
  { day: 'Day 2', Avocados: 3.48, Strawberries: 5.92, Blueberries: 7.15 },
  { day: 'Day 3', Avocados: 3.55, Strawberries: 6.10, Blueberries: 7.30 },
  { day: 'Day 4', Avocados: 3.62, Strawberries: 6.25, Blueberries: 7.45 },
  { day: 'Day 5', Avocados: 3.58, Strawberries: 6.18, Blueberries: 7.40 },
  { day: 'Day 6', Avocados: 3.70, Strawberries: 6.35, Blueberries: 7.55 },
  { day: 'Day 7', Avocados: 3.78, Strawberries: 6.50, Blueberries: 7.68 }
];

export default function MarketForecast() {
  return (
    <div className="space-y-6">
      <div className="glass-panel p-5 rounded-2xl">
        <h3 className="text-sm font-bold text-white mb-1">7-Day Commodity Spot Market Price Forecast ($/kg)</h3>
        <p className="text-xs text-slate-400 mb-4">Ridge Regression & Time-Series Commodity Spot Price Prediction Engine</p>

        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={mockPriceForecast}>
              <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
              <XAxis dataKey="day" stroke="#64748b" fontSize={11} />
              <YAxis stroke="#64748b" fontSize={11} />
              <Tooltip contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
              <Legend />
              <Line type="monotone" dataKey="Avocados" stroke="#10b981" strokeWidth={2} />
              <Line type="monotone" dataKey="Strawberries" stroke="#f43f5e" strokeWidth={2} />
              <Line type="monotone" dataKey="Blueberries" stroke="#06b6d4" strokeWidth={2} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
