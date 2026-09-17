import { useState } from 'react';

export default function Upload() {
  const [fileName, setFileName] = useState('');
  return <section><h1 className="card-header">Upload data</h1><div className="card"><label className="block text-sm font-medium text-gray-700" htmlFor="dataset">Choose a CSV dataset</label><input id="dataset" className="mt-3 block w-full" type="file" accept=".csv" onChange={(event) => setFileName(event.target.files?.[0]?.name || '')} />{fileName && <p className="mt-3 text-sm text-gray-600">Selected: {fileName}</p>}<p className="mt-4 text-sm text-gray-500">Dataset upload processing will be enabled when the backend import endpoint is available.</p></div></section>;
}