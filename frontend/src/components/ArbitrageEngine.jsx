import React from 'react';

export default function ArbitrageEngine({ summary }) {
  const arbitrage = summary?.arbitrage_summary || {
    evaluated_containers: 10,
    recommended_reroutes_count: 2,
    total_potential_margin_gain_usd: 36600.0,
    recommendations: [
      {
        container_id: "CONT-1002",
        commodity: "Strawberries",
        current_route: "Hamburg -> Rotterdam",
        destination_market: "Hamburg",
        original_spot_price_usd: 4800.0,
        destination_spot_price_usd: 5100.0,
        gross_value_delta_usd: 24000.0,
        rerouting_cost_usd: 1600.0,
        net_profit_gain_usd: 22400.0,
        cargo_saved_metric_tons: 80.0,
        action_recommendation: "EXECUTE_IMMEDIATE_REROUTE"
      },
      {
        container_id: "CONT-1005",
        commodity: "Salmon",
        current_route: "Oslo -> Rotterdam",
        destination_market: "Hamburg",
        original_spot_price_usd: 9200.0,
        destination_spot_price_usd: 9800.0,
        gross_value_delta_usd: 18000.0,
        rerouting_cost_usd: 3800.0,
        net_profit_gain_usd: 14200.0,
        cargo_saved_metric_tons: 30.0,
        action_recommendation: "EXECUTE_IMMEDIATE_REROUTE"
      }
    ]
  };

  return (
    <div style={{ padding: '32px' }}>
      <div className="dashboard-grid" style={{ marginBottom: '24px' }}>
        <div className="glass-card kpi-card">
          <span className="kpi-label">Evaluated Containers</span>
          <span className="kpi-val" style={{ color: '#60A5FA' }}>{arbitrage.evaluated_containers} Reefers</span>
        </div>
        <div className="glass-card kpi-card">
          <span className="kpi-label">Reroute Opportunities</span>
          <span className="kpi-val" style={{ color: '#FBBF24' }}>{arbitrage.recommended_reroutes_count} Active</span>
        </div>
        <div className="glass-card kpi-card">
          <span className="kpi-label">Net Profit Margin Gain</span>
          <span className="kpi-val" style={{ color: '#34D399' }}>${arbitrage.total_potential_margin_gain_usd?.toLocaleString()}</span>
        </div>
        <div className="glass-card kpi-card">
          <span className="kpi-label">Reroute Execution Status</span>
          <span className="kpi-val" style={{ color: '#38BDF8' }}>AUTO-READY</span>
        </div>
      </div>

      <div className="glass-card">
        <h3 style={{ marginBottom: '16px', fontSize: '1.2rem', color: '#F8FAFC' }}>
          📈 Profitable Destination Arbitrage Opportunities
        </h3>

        <table className="data-table">
          <thead>
            <tr>
              <th>Container ID</th>
              <th>Commodity</th>
              <th>Original Spot Price</th>
              <th>Target Spot Price</th>
              <th>Cargo MT</th>
              <th>Reroute Cost</th>
              <th>Net Profit Gain</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            {arbitrage.recommendations.map(r => (
              <tr key={r.container_id}>
                <td style={{ fontFamily: 'var(--font-mono)', fontWeight: 600 }}>{r.container_id}</td>
                <td>{r.commodity}</td>
                <td>${r.original_spot_price_usd?.toLocaleString()} / ton</td>
                <td style={{ fontWeight: 700, color: '#60A5FA' }}>${r.destination_spot_price_usd?.toLocaleString()} / ton</td>
                <td>{r.cargo_saved_metric_tons} MT</td>
                <td style={{ color: '#EF4444' }}>-${r.rerouting_cost_usd?.toLocaleString()}</td>
                <td style={{ fontWeight: 800, color: '#34D399', fontSize: '1.05rem' }}>
                  +${r.net_profit_gain_usd?.toLocaleString()}
                </td>
                <td>
                  <button className="btn-primary" style={{ padding: '6px 14px', fontSize: '0.8rem' }}>
                    Approve Reroute
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
