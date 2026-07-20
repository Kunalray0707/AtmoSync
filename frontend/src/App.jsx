import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import ExecutiveDashboard from './pages/ExecutiveDashboard';
import ContainerMonitoring from './pages/ContainerMonitoring';
import SpoilageAnalytics from './pages/SpoilageAnalytics';
import ArbitrageRerouting from './pages/ArbitrageRerouting';
import RouteTrackingMap from './pages/RouteTrackingMap';
import MarketForecast from './pages/MarketForecast';
import MLInsights from './pages/MLInsights';
import DatasetInspector from './pages/DatasetInspector';
import ReportsCenter from './pages/ReportsCenter';
import AlertCenter from './pages/AlertCenter';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [dashboardSummary, setDashboardSummary] = useState(null);
  const [containers, setContainers] = useState([]);
  const [arbitrageOpps, setArbitrageOpps] = useState([]);
  const [alerts, setAlerts] = useState([]);

  const fetchData = async () => {
    try {
      const summaryRes = await fetch('/api/dashboard/summary');
      if (summaryRes.ok) setDashboardSummary(await summaryRes.json());

      const containerRes = await fetch('/api/containers');
      if (containerRes.ok) {
        const cData = await containerRes.json();
        setContainers(cData.containers || []);
      }

      const arbRes = await fetch('/api/arbitrage');
      if (arbRes.ok) {
        const aData = await arbRes.json();
        setArbitrageOpps(aData.opportunities || []);
      }

      const alertRes = await fetch('/api/alerts');
      if (alertRes.ok) {
        const alData = await alertRes.json();
        setAlerts(alData.alerts || []);
      }
    } catch (e) {
      console.log("Offline mode simulation state active.");
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 4000);
    return () => clearInterval(interval);
  }, []);

  const renderActiveTab = () => {
    switch (activeTab) {
      case 'dashboard':
        return <ExecutiveDashboard summary={dashboardSummary} />;
      case 'containers':
        return <ContainerMonitoring containers={containers} />;
      case 'spoilage':
        return <SpoilageAnalytics />;
      case 'arbitrage':
        return <ArbitrageRerouting opportunities={arbitrageOpps} />;
      case 'map':
        return <RouteTrackingMap />;
      case 'forecast':
        return <MarketForecast />;
      case 'ml':
        return <MLInsights />;
      case 'inspector':
        return <DatasetInspector />;
      case 'reports':
        return <ReportsCenter />;
      case 'alerts':
        return <AlertCenter alerts={alerts} />;
      default:
        return <ExecutiveDashboard summary={dashboardSummary} />;
    }
  };

  return (
    <div className="flex min-h-screen bg-slate-950 text-slate-100 font-sans">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <div className="flex-1 flex flex-col min-w-0">
        <Header activeTab={activeTab} onRefresh={fetchData} />
        <main className="flex-1 p-6 overflow-y-auto">
          {renderActiveTab()}
        </main>
      </div>
    </div>
  );
}
