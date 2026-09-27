import { useState } from 'react';
import './App.css';
import logo from './assets/logo.png';
import InventoryOverview from './InventoryOverview';
import ForecastDashboard from './ForecastDashboard';

function App() {
  const [activeTab, setActiveTab] = useState('inventory');

  return (
    <div className="page">
      <header className="topbar">
        <div className="brand">
          <img src={logo} alt="StockSense logo" className="brand-mark-img" />
          <span className="brand-name">
            <span className="brand-bold">Stock</span>
            <span className="brand-light">Sense</span>
          </span>
        </div>
        <nav className="tabs">
          <button
            className={activeTab === 'inventory' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('inventory')}
          >
            Inventory
          </button>
          <button
            className={activeTab === 'forecast' ? 'tab active' : 'tab'}
            onClick={() => setActiveTab('forecast')}
          >
            Forecast
          </button>
        </nav>
      </header>

      <main className="app">
        {activeTab === 'inventory' && <InventoryOverview />}
        {activeTab === 'forecast' && <ForecastDashboard />}
      </main>
    </div>
  );
}

export default App;