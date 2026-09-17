import { useEffect, useState } from 'react';
import { sensorsAPI } from '../services/api';

export default function Sensors() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState('');
  useEffect(() => { sensorsAPI.getLatest().then((response) => setItems(response.data)).catch(() => setError('Unable to load sensor readings.')); }, []);
  return <section><h1 className="card-header">Latest sensor readings</h1>{error && <p className="text-red-700">{error}</p>}<div className="card overflow-x-auto"><table className="w-full text-left text-sm"><thead><tr><th className="pb-3">Truck</th><th className="pb-3">Commodity</th><th className="pb-3">Temperature</th><th className="pb-3">Humidity</th><th className="pb-3">Risk</th></tr></thead><tbody>{items.map((item) => <tr key={item.id} className="border-t"><td className="py-3">{item.truck_id}</td><td>{item.commodity}</td><td>{item.temperature} C</td><td>{item.humidity}%</td><td>{item.spoilage_score ?? '-'}</td></tr>)}</tbody></table>{!items.length && !error && <p className="text-gray-500">No readings found.</p>}</div></section>;
}