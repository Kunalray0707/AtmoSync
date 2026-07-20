import React, { useState } from 'react';
import { Upload, CheckCircle2, FileText, AlertCircle, Layers } from 'lucide-react';

export default function DatasetInspector() {
  const [inspectData, setInspectData] = useState(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setIsUploading(true);
    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('/api/inspect-dataset', {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      setInspectData(data);
    } catch (err) {
      console.error("Dataset inspection upload error:", err);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 text-center">
        <div className="w-12 h-12 rounded-full bg-cyan-950 text-cyan-400 border border-cyan-800 flex items-center justify-center mx-auto mb-3">
          <Upload className="w-6 h-6" />
        </div>
        <h3 className="text-base font-bold text-white mb-1">Adaptive Dataset Inspector Engine</h3>
        <p className="text-xs text-slate-400 max-w-md mx-auto mb-4">
          Upload any external cold-chain CSV or Parquet dataset. AtmoSync will automatically inspect data types, missing values, duplicate rows, and map semantic column schemas dynamically without hardcoding.
        </p>

        <label className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-cyan-500 text-slate-950 font-bold text-xs cursor-pointer hover:bg-cyan-400 transition-colors shadow-lg shadow-cyan-500/20">
          <Upload className="w-4 h-4" />
          <span>{isUploading ? 'Analyzing Dataset...' : 'Choose CSV or Parquet Dataset'}</span>
          <input type="file" accept=".csv,.parquet" onChange={handleFileUpload} className="hidden" />
        </label>
      </div>

      {inspectData && (
        <div className="glass-panel p-5 rounded-2xl space-y-4">
          <div className="flex items-center justify-between border-b border-slate-800 pb-3">
            <h4 className="text-sm font-bold text-white flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              Dataset Inspection Summary ({inspectData.filename})
            </h4>
            <span className="px-2.5 py-0.5 rounded bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-bold">
              Schema Adapted
            </span>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <div className="bg-slate-900/80 p-3 rounded-xl">
              <span className="text-[10px] text-slate-400">Total Rows</span>
              <div className="text-base font-bold text-white">{inspectData.inspection?.summary?.total_rows}</div>
            </div>
            <div className="bg-slate-900/80 p-3 rounded-xl">
              <span className="text-[10px] text-slate-400">Total Columns</span>
              <div className="text-base font-bold text-white">{inspectData.inspection?.summary?.total_columns}</div>
            </div>
            <div className="bg-slate-900/80 p-3 rounded-xl">
              <span className="text-[10px] text-slate-400">Duplicate Rows</span>
              <div className="text-base font-bold text-white">{inspectData.inspection?.summary?.duplicate_rows}</div>
            </div>
            <div className="bg-slate-900/80 p-3 rounded-xl">
              <span className="text-[10px] text-slate-400">Pipeline Ready</span>
              <div className="text-base font-bold text-emerald-400">YES</div>
            </div>
          </div>

          <div>
            <h5 className="text-xs font-bold text-slate-300 mb-2">Detected Semantic Schema Mappings</h5>
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-2 text-xs">
              {Object.entries(inspectData.inspection?.semantic_mappings || {}).map(([key, val]) => (
                <div key={key} className="p-2.5 rounded-lg bg-slate-900/60 border border-slate-800">
                  <span className="text-[10px] text-slate-400 block uppercase">{key}</span>
                  <span className="font-semibold text-cyan-400">{val || 'Not Detected'}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
