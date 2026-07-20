import React from 'react';
import { Download, FileText, FileSpreadsheet, Presentation, FileCode } from 'lucide-react';

export default function ReportsCenter() {
  const formats = [
    { format: 'pdf', label: 'Executive PDF Report', icon: FileText, color: 'text-rose-400', desc: 'Formatted multi-page PDF with executive summary KPIs' },
    { format: 'excel', label: 'Excel Workbook (.xlsx)', icon: FileSpreadsheet, color: 'text-emerald-400', desc: 'Formatted multi-tab spreadsheet with styling' },
    { format: 'pptx', label: 'PowerPoint Deck (.pptx)', icon: Presentation, color: 'text-amber-400', desc: 'Executive slide presentation deck' },
    { format: 'csv', label: 'Raw CSV Telemetry', icon: Download, color: 'text-cyan-400', desc: 'Comma-separated values for data analysis' },
    { format: 'json', label: 'JSON Stream Dataset', icon: FileCode, color: 'text-indigo-400', desc: 'Structured JSON payload stream' }
  ];

  const handleDownload = (fmt) => {
    window.open(`/api/reports/download?format=${fmt}`, '_blank');
  };

  return (
    <div className="space-y-6">
      <div className="glass-panel p-5 rounded-2xl">
        <h3 className="text-sm font-bold text-white mb-1">Executive Reports & Export Engine</h3>
        <p className="text-xs text-slate-400 mb-4">Generate and download multi-format operational and financial reports</p>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {formats.map((item, idx) => {
            const Icon = item.icon;
            return (
              <div key={idx} className="glass-card p-4 rounded-xl space-y-3">
                <div className="flex items-center gap-3">
                  <div className="w-9 h-9 rounded-lg bg-slate-900 flex items-center justify-center">
                    <Icon className={`w-5 h-5 ${item.color}`} />
                  </div>
                  <div>
                    <h4 className="text-xs font-bold text-white">{item.label}</h4>
                    <p className="text-[10px] text-slate-400 leading-tight">{item.desc}</p>
                  </div>
                </div>

                <button
                  onClick={() => handleDownload(item.format)}
                  className="w-full py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-xs text-slate-200 font-semibold flex items-center justify-center gap-2 transition-colors"
                >
                  <Download className="w-3.5 h-3.5 text-cyan-400" /> Download {item.format.toUpperCase()}
                </button>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
