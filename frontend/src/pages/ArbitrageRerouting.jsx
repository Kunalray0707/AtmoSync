import React from 'react';
import { TrendingUp, ArrowRight, DollarSign, Navigation, ShieldCheck } from 'lucide-react';

export default function ArbitrageRerouting({ opportunities }) {
  const sampleOpps = [
    {
      container_id: 'CONT-1002',
      shipment_id: 'SHP-NL-01-202',
      commodity: 'Avocados',
      primary_destination: 'Rotterdam Port (Netherlands)',
      best_alternative_destination: {
        destination: 'Antwerp Port (Belgium)',
        extra_distance_km: -120,
        spot_market_price_per_kg: 3.90,
        reroute_cost_usd: 650.0,
        net_profit_delta_usd: 8450.00
      },
      arbitrage_score: 84.5,
      recommendation: 'REROUTE_RECOMMENDED'
    },
    {
      container_id: 'CONT-1005',
      shipment_id: 'SHP-ES-03-205',
      commodity: 'Strawberries',
      primary_destination: 'London Gateway (UK)',
      best_alternative_destination: {
        destination: 'Le Havre Port (France)',
        extra_distance_km: -350,
        spot_market_price_per_kg: 6.40,
        reroute_cost_usd: 820.0,
        net_profit_delta_usd: 10000.00
      },
      arbitrage_score: 95.0,
      recommendation: 'REROUTE_RECOMMENDED'
    }
  ];

  const list = (opportunities && opportunities.length > 0) ? opportunities : sampleOpps;

  return (
    <div className="space-y-6">
      <div className="glass-panel p-5 rounded-2xl flex items-center justify-between">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-emerald-400" />
            Live Arbitrage Rerouting Opportunities
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Micro-climate shelf life vs regional spot price differential recommendations
          </p>
        </div>
        <div className="text-right">
          <span className="text-xs text-slate-400">Total Net Gain:</span>
          <div className="text-xl font-black text-emerald-400">+$18,450.00</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {list.map((opp, idx) => {
          const alt = opp.best_alternative_destination;
          return (
            <div key={idx} className="glass-card p-5 rounded-2xl border border-emerald-500/30 space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-xs font-bold text-white">{opp.container_id}</span>
                  <span className="text-[10px] text-slate-400 ml-2">({opp.commodity})</span>
                </div>
                <span className="px-2.5 py-0.5 rounded-full bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
                  Score: {opp.arbitrage_score} / 100
                </span>
              </div>

              <div className="grid grid-cols-2 gap-3 p-3 rounded-xl bg-slate-900/80 text-xs">
                <div>
                  <span className="text-[10px] text-slate-400 uppercase">Primary Destination</span>
                  <div className="font-semibold text-slate-300">{opp.primary_destination}</div>
                </div>
                <div>
                  <span className="text-[10px] text-slate-400 uppercase">Recommended Diversion</span>
                  <div className="font-bold text-emerald-400 flex items-center gap-1">
                    <ArrowRight className="w-3 h-3" /> {alt?.destination}
                  </div>
                </div>
              </div>

              <div className="flex items-center justify-between pt-2 border-t border-slate-800 text-xs">
                <div>
                  <span className="text-slate-400">Reroute Cost: </span>
                  <span className="font-semibold text-rose-400">${alt?.reroute_cost_usd}</span>
                </div>
                <div>
                  <span className="text-slate-400">Net Profit Gain: </span>
                  <span className="font-black text-emerald-400 text-sm">+${alt?.net_profit_delta_usd?.toLocaleString()}</span>
                </div>
              </div>

              <button className="w-full py-2 rounded-xl bg-gradient-to-r from-emerald-500 to-teal-600 text-slate-950 font-bold text-xs shadow-lg shadow-emerald-500/20 hover:brightness-110 transition-all flex items-center justify-center gap-1.5">
                <Navigation className="w-3.5 h-3.5" /> Execute Route Diversion
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
}
