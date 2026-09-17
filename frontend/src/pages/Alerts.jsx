import { useEffect, useState } from 'react';
import { alertsAPI } from '../services/api';

export default function Alerts() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState('');
  useEffect(() => { alertsAPI.list().then((response) => setItems(response.data)).catch(() => setError('Unable to load alerts.')); }, []);
  return <section><h1 className="card-header">Alerts</h1>{error && <p className="text-red-700">{error}</p>}<div className="space-y-3">{items.map((item) => <article className="card" key={item.id}><div className="flex justify-between gap-4"><h2 className="font-semibold">{item.title}</h2><span className="badge-warning">{item.severity}</span></div><p className="mt-2 text-gray-600">{item.message}</p></article>)}{!items.length && !error && <div className="card text-gray-500">No alerts found.</div>}</div></section>;
}