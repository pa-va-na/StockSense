import { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

const CATEGORY_COLORS = {
  Household: '#D8A2A2',
  Stationery: '#8EA66B',
  Grocery: '#0D1C42',
};

function AnalyticsPage() {
  const [categoryData, setCategoryData] = useState([]);
  const [productData, setProductData] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/analytics/category-totals')
      .then(res => res.json())
      .then(data => setCategoryData(data));

    fetch('http://127.0.0.1:8000/analytics/product-totals')
      .then(res => res.json())
      .then(data => setProductData(data));
  }, []);

  return (
    <>
      <div className="page-heading">
        <h1>Sales Insights</h1>
        <p className="subtitle">What sells, what doesn't, across five years of history</p>
      </div>

      <div className="table-card chart-card">
        <h3>Units sold by category</h3>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart data={categoryData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#FFF9D6" />
            <XAxis dataKey="category" tick={{ fontSize: 12 }} />
            <YAxis tick={{ fontSize: 12 }} />
            <Tooltip />
            <Bar dataKey="total_sold" radius={[6, 6, 0, 0]}>
              {categoryData.map((entry) => (
                <Cell key={entry.category} fill={CATEGORY_COLORS[entry.category]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className="table-card chart-card">
        <h3>Products ranked by units sold</h3>
        <p className="chart-note">The three slowest movers are highlighted in rose.</p>
        <ResponsiveContainer width="100%" height={420}>
          <BarChart data={productData} layout="vertical" margin={{ left: 40 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#FFF9D6" />
            <XAxis type="number" tick={{ fontSize: 12 }} />
            <YAxis type="category" dataKey="name" width={150} tick={{ fontSize: 12 }} />
            <Tooltip />
            <Bar dataKey="total_sold" radius={[0, 6, 6, 0]}>
              {productData.map((entry, index) => (
                <Cell key={entry.name} fill={index < 3 ? '#D8A2A2' : '#8EA66B'} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </>
  );
}

export default AnalyticsPage;