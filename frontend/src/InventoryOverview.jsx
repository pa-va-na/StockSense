import { useState, useEffect } from 'react';

function InventoryOverview() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/inventory-overview')
      .then(res => res.json())
      .then(data => setProducts(data));
  }, []);

  const needsRestockCount = products.filter(p => p.status !== 'ok').length;
  const healthyCount = products.filter(p => p.status === 'ok').length;
  const statusLabels = { ok: 'Healthy', low: 'Reorder soon', out: 'Out of stock' };

  return (
    <>
      <div className="page-heading">
        <h1>Inventory Overview</h1>
        <p className="subtitle">Live stock status across your shop</p>
      </div>

      <div className="stats-row">
        <div className="stat-card">
          <span className="stat-value">{products.length}</span>
          <span className="stat-label">Total Products</span>
        </div>
        <div className="stat-card stat-sage">
          <span className="stat-value">{healthyCount}</span>
          <span className="stat-label">Healthy Stock</span>
        </div>
        <div className="stat-card stat-rose">
          <span className="stat-value">{needsRestockCount}</span>
          <span className="stat-label">Needs Restock</span>
        </div>
      </div>

      <div className="table-card">
        <table>
          <thead>
            <tr>
              <th>Name</th>
              <th>Category</th>
              <th>Current Stock</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {products.map((p) => (
              <tr key={p.product_id} className={`row-${p.status}`}>
                <td>{p.name}</td>
                <td><span className={`badge badge-${p.category.toLowerCase()}`}>{p.category}</span></td>
                <td className="stock-cell">{p.current_stock}</td>
                <td><span className={`status status-${p.status}`}>{statusLabels[p.status]}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </>
  );
}

export default InventoryOverview;