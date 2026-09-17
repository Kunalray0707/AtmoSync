import { useEffect, useState } from 'react';
import { commoditiesAPI } from '../services/api';

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    commoditiesAPI.getDashboardSummary()
      .then((response) => setSummary(response.data))
      .catch(() => setError('Dashboard data is unavailable. Start the API and refresh.'));
  }, []);

  const metrics = summary ? [
    ['Commodities', summary.total_commodities],
    ['Active trucks', summary.active_trucks],
    ['Alerts', summary.total_alerts],
    ['Sensor readings', summary.total_sensor_readings],
  ] : [];

  return (
    <section>
      <h1 className="mb-2 text-3xl font-bold text-gray-900">Operations dashboard</h1>
      <p className="mb-6 text-gray-500">A current view of monitored cold-chain activity.</p>
      {error && <p className="mb-4 rounded-lg bg-red-50 p-3 text-red-700">{error}</p>}
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
        {metrics.map(([label, value]) => <div className="stat-card" key={label}><div><p className="stat-label">{label}</p><p className="stat-value">{value}</p></div></div>)}
      </div>
      {!summary && !error && <p className="mt-8 text-gray-500">Loading dashboard...</p>}
    </section>
  );
}