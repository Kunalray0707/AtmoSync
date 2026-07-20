import React from 'react';
import { Bell, AlertTriangle, Send } from 'lucide-react';

export default function AlertCenter({ alerts }) {
  const sampleAlerts = [
    {
      alert_id: 'ALT-CONT-1002-DOOR',
      container_id: 'CONT-1002',
      shipment_id: 'SHP-NL-01-202',
      severity: 'CRITICAL',
      alert_type: 'DOOR_UNLATCHED',
      message: 'Container door unlatched while transporting Strawberries',
      recommended_action: 'Notify driver/vessel crew to verify seal lock'
    },
    {
      alert_id: 'ALT-CONT-1005-SPOILAGE',
      container_id: 'CONT-1005',
      shipment_id: 'SHP-ES-03-205',
      severity: 'HIGH',
      alert_type: 'SPOILAGE_RISK_EXCEEDED',
      message: 'Spoilage risk reached 68% for Strawberries',
      recommended_action: 'Evaluate immediate port rerouting'
    }
  ];

  const list = (alerts && alerts.length > 0) ? alerts : sampleAlerts;

  const handleDispatchSlack = async (alert) => {
    try {
      await fetch('/api/alerts/trigger', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(alert)
      });
      alert('Alert dispatched to Slack & Email webhooks!');
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-5 rounded-2xl flex items-center justify-between">
        <div>
          <h3 className="text-sm font-bold text-white flex items-center gap-2">
            <Bell className="w-4 h-4 text-rose-400" />
            Active Real-Time Cold-Chain Alerts
          </h3>
          <p className="text-xs text-slate-400">Multi-channel dispatches for door breaches, temperature excursions, and spoilage risk</p>
        </div>
        <span className="px-2.5 py-1 rounded bg-rose-950 text-rose-400 border border-rose-800 text-xs font-bold">
          {list.length} Alerts Active
        </span>
      </div>

      <div className="space-y-3">
        {list.map((alt, idx) => (
          <div key={idx} className="glass-card p-4 rounded-xl border border-rose-500/30 flex items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="w-9 h-9 rounded-lg bg-rose-950 text-rose-400 border border-rose-800 flex items-center justify-center">
                <AlertTriangle className="w-5 h-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-white">{alt.container_id}</span>
                  <span className="px-1.5 py-0.5 rounded bg-rose-950 text-rose-400 text-[10px] font-bold">
                    {alt.severity}
                  </span>
                </div>
                <p className="text-xs text-slate-300 font-medium mt-0.5">{alt.message}</p>
                <p className="text-[10px] text-slate-400 mt-0.5">Action: {alt.recommended_action}</p>
              </div>
            </div>

            <button
              onClick={() => handleDispatchSlack(alt)}
              className="px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold flex items-center gap-1.5 border border-slate-700"
            >
              <Send className="w-3.5 h-3.5 text-cyan-400" /> Dispatch Webhook
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
