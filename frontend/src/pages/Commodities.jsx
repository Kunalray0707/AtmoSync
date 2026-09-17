import { useEffect, useState } from 'react';
import { commoditiesAPI } from '../services/api';

export default function Commodities() {
  const [items, setItems] = useState([]);
  const [error, setError] = useState('');
  useEffect(() => { commoditiesAPI.list().then((response) => setItems(response.data)).catch(() => setError('Unable to load commodities.')); }, []);
  return <section><h1 className="card-header">Commodities</h1>{error && <p className="text-red-700">{error}</p>}<div className="card overflow-x-auto"><table className="w-full text-left text-sm"><thead><tr><th className="pb-3">Name</th><th className="pb-3">Type</th><th className="pb-3">Price</th><th className="pb-3">Region</th></tr></thead><tbody>{items.map((item) => <tr key={item.id} className="border-t"><td className="py-3">{item.name}</td><td>{item.commodity_type}</td><td>{item.current_price ?? '-'}</td><td>{item.region ?? '-'}</td></tr>)}</tbody></table>{!items.length && !error && <p className="text-gray-500">No commodities found.</p>}</div></section>;
}