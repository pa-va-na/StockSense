import { useState, useEffect } from 'react';

function RestockForm() {
  const [products, setProducts] = useState([]);
  const [formData, setFormData] = useState({
    product_id: '',
    dealer_id: 1,
    shop_id: 3,
    batch_no: '',
    quantity: '',
    cost_price: '',
    order_date: '',
    delivery_date: '',
    manufacture_date: '',
    expiry_date: '',
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  useEffect(() => {
    fetch('http://127.0.0.1:8000/inventory-overview')
      .then(res => res.json())
      .then(data => setProducts(data));
  }, []);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setMessage('');
    setError('');

    fetch('http://127.0.0.1:8000/restock', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        ...formData,
        product_id: Number(formData.product_id),
        dealer_id: Number(formData.dealer_id),
        shop_id: Number(formData.shop_id),
        quantity: Number(formData.quantity),
        cost_price: Number(formData.cost_price),
      }),
    })
      .then(async (res) => {
        const data = await res.json();
        if (!res.ok) throw new Error(data.detail || 'Something went wrong');
        setMessage(data.message);
      })
      .catch((err) => setError(err.message));
  };

  return (
    <>
      <div className="page-heading">
        <h1>Log a Restock</h1>
        <p className="subtitle">Record stock received from a dealer</p>
      </div>

      <form className="table-card restock-form" onSubmit={handleSubmit}>
        <label>
          Product
          <select name="product_id" value={formData.product_id} onChange={handleChange} required>
            <option value="">Select a product</option>
            {products.map(p => (
              <option key={p.product_id} value={p.product_id}>{p.name}</option>
            ))}
          </select>
        </label>

        <label>
          Batch No.
          <input name="batch_no" value={formData.batch_no} onChange={handleChange} required />
        </label>

        <label>
          Quantity
          <input type="number" name="quantity" value={formData.quantity} onChange={handleChange} required />
        </label>

        <label>
          Cost Price (per unit)
          <input type="number" step="0.01" name="cost_price" value={formData.cost_price} onChange={handleChange} required />
        </label>

        <label>
          Order Date
          <input type="date" name="order_date" value={formData.order_date} onChange={handleChange} required />
        </label>

        <label>
          Delivery Date
          <input type="date" name="delivery_date" value={formData.delivery_date} onChange={handleChange} required />
        </label>

        <label>
          Manufacture Date
          <input type="date" name="manufacture_date" value={formData.manufacture_date} onChange={handleChange} required />
        </label>

        <label>
          Expiry Date
          <input type="date" name="expiry_date" value={formData.expiry_date} onChange={handleChange} required />
        </label>

        <button type="submit">Add Restock</button>
        {message && <p className="form-message">{message}</p>}
        {error && <p className="form-error">{error}</p>}
      </form>
    </>
  );
}

export default RestockForm;