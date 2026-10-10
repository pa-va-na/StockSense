import { useState, useEffect } from 'react';

function SaleForm() {
  const [products, setProducts] = useState([]);
  const [productId, setProductId] = useState('');
  const [quantity, setQuantity] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetch('http://127.0.0.1:8000/inventory-overview')
      .then(res => res.json())
      .then(data => setProducts(data))
      .catch(() => setError('Could not load products. Is the backend running?'));
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();
    setMessage('');
    setError('');

    fetch('http://127.0.0.1:8000/sale', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        product_id: Number(productId),
        quantity: Number(quantity),
      }),
    })
      .then(async (res) => {
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Something went wrong');
        setMessage(`${data.message}. Total: ₹${data.total}`);
        setQuantity('');
      })
      .catch((err) => setError(err.message));
  };

  return (
    <>
      <div className="page-heading">
        <h1>Record a Sale</h1>
        <p className="subtitle">Log an item sold to a customer</p>
      </div>

      <form className="table-card restock-form" onSubmit={handleSubmit}>
        <label>
          Product
          <select value={productId} onChange={(e) => setProductId(e.target.value)} required>
            <option value="">Select a product</option>
            {products.map(p => (
              <option key={p.product_id} value={p.product_id}>{p.name}</option>
            ))}
          </select>
        </label>

        <label>
          Quantity
          <input type="number" min="1" value={quantity} onChange={(e) => setQuantity(e.target.value)} required />
        </label>

        <button type="submit">Record Sale</button>
        {message && <p className="form-message">{message}</p>}
        {error && <p className="form-error">{error}</p>}
      </form>
    </>
  );
}

export default SaleForm;