import { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function ForecastDashboard() {
  const [products, setProducts] = useState([]);
  const [selectedProductId, setSelectedProductId] = useState(39);
  const [forecastData, setForecastData] = useState([]);

  // Load the product list once, to populate the dropdown
  useEffect(() => {
    fetch('http://127.0.0.1:8000/inventory-overview')
      .then(res => res.json())
      .then(data => setProducts(data));
  }, []);

  // Re-fetch the forecast every time the selected product changes
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/forecast/${selectedProductId}`)
      .then(res => res.json())
      .then(data => setForecastData(data));
  }, [selectedProductId]);

  return (
    <>
      <div className="page-heading">
        <h1>Forecast Dashboard</h1>
        <p className="subtitle">7-day demand forecast, powered by Prophet</p>
      </div>

      <div className="table-card forecast-card">
        <div className="forecast-controls">
          <label htmlFor="product-select">Product:</label>
          <select
            id="product-select"
            value={selectedProductId}
            onChange={(e) => setSelectedProductId(Number(e.target.value))}
          >
            {products.map((p) => (
              <option key={p.product_id} value={p.product_id}>{p.name}</option>
            ))}
          </select>
        </div>

        <ResponsiveContainer width="100%" height={320}>
          <LineChart data={forecastData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#FFF9D6" />
            <XAxis dataKey="ds" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip />
            <Line type="monotone" dataKey="yhat" stroke="#8EA66B" strokeWidth={3} dot={{ r: 3 }} />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </>
  );
}

export default ForecastDashboard;