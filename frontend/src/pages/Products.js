import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import { getProducts, createProduct, deleteProduct } from '../api';

const s = {
  root: { display: 'flex', minHeight: '100vh', background: 'var(--bg)' },
  main: { flex: 1, padding: '40px', overflow: 'auto' },
  header: { display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '32px' },
  title: { fontFamily: 'var(--font-display)', fontSize: '28px', fontWeight: 700, color: 'var(--text)' },
  sub: { fontSize: '14px', color: 'var(--text2)', marginTop: '4px' },
  btn: (v) => ({
    padding: '10px 20px', borderRadius: 'var(--radius-sm)',
    fontSize: '13px', fontWeight: 600,
    fontFamily: 'var(--font-display)',
    background: v === 'primary' ? 'var(--accent)' : 'rgba(255,255,255,0.05)',
    color: v === 'primary' ? '#fff' : 'var(--text2)',
    border: v === 'primary' ? 'none' : '1px solid var(--border)',
    cursor: 'pointer',
    boxShadow: v === 'primary' ? '0 4px 16px var(--accent-glow)' : 'none',
  }),
  table: { width: '100%', borderCollapse: 'collapse' },
  th: {
    padding: '12px 16px', textAlign: 'left',
    fontSize: '11px', fontWeight: 600,
    color: 'var(--text3)', textTransform: 'uppercase',
    letterSpacing: '0.1em', fontFamily: 'var(--font-display)',
    borderBottom: '1px solid var(--border)',
  },
  td: {
    padding: '14px 16px', fontSize: '14px',
    color: 'var(--text)', borderBottom: '1px solid rgba(255,255,255,0.04)',
  },
  tr: { transition: 'background 0.15s' },
  badge: (cat) => {
    const colors = { 'Category 1': '#7c3aed', 'Category 2': '#0891b2', 'Category 3': '#059669', 'Category 4': '#d97706', 'Category 5': '#dc2626' };
    const c = colors[cat] || '#666';
    return {
      padding: '3px 10px', borderRadius: '100px', fontSize: '11px',
      background: `${c}22`, color: c, border: `1px solid ${c}44`,
      fontWeight: 500,
    };
  },
  deleteBtn: {
    padding: '6px 12px', borderRadius: 'var(--radius-sm)',
    background: 'transparent', color: 'var(--text3)',
    border: '1px solid transparent', fontSize: '12px',
    cursor: 'pointer', transition: 'all 0.15s',
  },
  modal: {
    position: 'fixed', inset: 0, zIndex: 100,
    background: 'rgba(0,0,0,0.7)',
    backdropFilter: 'blur(4px)',
    display: 'flex', alignItems: 'center', justifyContent: 'center',
  },
  modalCard: {
    width: '440px', padding: '36px',
    background: 'var(--bg2)',
    border: '1px solid var(--border)',
    borderRadius: '20px',
    boxShadow: 'var(--shadow)',
    animation: 'fadeIn 0.2s ease',
  },
  modalTitle: {
    fontFamily: 'var(--font-display)',
    fontSize: '20px', fontWeight: 700,
    color: 'var(--text)', marginBottom: '24px',
  },
  label: {
    display: 'block', fontSize: '11px', fontWeight: 600,
    color: 'var(--text3)', marginBottom: '6px',
    textTransform: 'uppercase', letterSpacing: '0.08em',
    fontFamily: 'var(--font-display)',
  },
  input: {
    width: '100%', padding: '11px 14px',
    background: 'rgba(255,255,255,0.04)',
    border: '1px solid var(--border)',
    borderRadius: 'var(--radius-sm)',
    color: 'var(--text)', fontSize: '14px', marginBottom: '16px',
  },
  row: { display: 'flex', gap: '12px', justifyContent: 'flex-end', marginTop: '8px' },
  pagination: { display: 'flex', gap: '8px', justifyContent: 'center', marginTop: '24px' },
  pageBtn: (active) => ({
    width: 36, height: 36, borderRadius: 'var(--radius-sm)',
    background: active ? 'var(--accent)' : 'var(--bg2)',
    color: active ? '#fff' : 'var(--text2)',
    border: `1px solid ${active ? 'transparent' : 'var(--border)'}`,
    fontSize: '13px', cursor: 'pointer', display: 'flex',
    alignItems: 'center', justifyContent: 'center',
  }),
};

export default function Products() {
  const [products, setProducts] = useState([]);
  const [total, setTotal] = useState(0);
  const [page, setPage] = useState(1);
  const [showModal, setShowModal] = useState(false);
  const [form, setForm] = useState({ name: '', price: '', stock: '', category: '' });
  const [loadError, setLoadError] = useState(false);
  const limit = 10;

  const load = async (p = page) => {
    try {
      setLoadError(false);
      const r = await getProducts(p, limit);
      setProducts(r.data.products);
      setTotal(r.data.total);
    } catch {
      setLoadError(true);
    }
  };

  useEffect(() => { load(); }, [page]);

  const handleCreate = async e => {
    e.preventDefault();
    await createProduct({ ...form, price: parseFloat(form.price), stock: parseInt(form.stock) });
    setShowModal(false);
    setForm({ name: '', price: '', stock: '', category: '' });
    load();
  };

  const handleDelete = async id => {
    await deleteProduct(id);
    load();
  };

  const pages = Math.ceil(total / limit);

  return (
    <div style={s.root}>
      <Sidebar />
      <div style={s.main}>
        <div style={s.header}>
          <div>
            <div style={s.title}>Products</div>
            <div style={s.sub}>{total} items in database</div>
          </div>
          <button style={s.btn('primary')} onClick={() => setShowModal(true)}>+ New Product</button>
        </div>

        {loadError && (
          <div style={{ padding: '16px', marginBottom: '16px', borderRadius: 'var(--radius-sm)', background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.2)', color: '#fca5a5', fontSize: '13px' }}>
            Failed to load products. Check API connectivity.
          </div>
        )}
        <div style={{ background: 'var(--bg2)', borderRadius: 'var(--radius)', border: '1px solid var(--border)', overflow: 'hidden', animation: 'fadeIn 0.4s ease' }}>
          <table style={s.table}>
            <thead>
              <tr>
                {['ID', 'Name', 'Price', 'Stock', 'Category', ''].map(h => (
                  <th key={h} style={s.th}>{h}</th>
                ))}
              </tr>
            </thead>
            <tbody>
              {products.map(p => (
                <tr key={p.id} style={s.tr}>
                  <td style={{ ...s.td, color: 'var(--text3)', fontSize: '12px' }}>#{p.id}</td>
                  <td style={{ ...s.td, fontWeight: 500 }}>{p.name}</td>
                  <td style={s.td}>${p.price.toFixed(2)}</td>
                  <td style={{ ...s.td, color: p.stock < 10 ? 'var(--warning)' : 'var(--text)' }}>{p.stock}</td>
                  <td style={s.td}><span style={s.badge(p.category)}>{p.category}</span></td>
                  <td style={s.td}>
                    <button style={s.deleteBtn} onClick={() => handleDelete(p.id)}>Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {pages > 1 && (
          <div style={s.pagination}>
            {Array.from({ length: pages }, (_, i) => i + 1).map(p => (
              <button key={p} style={s.pageBtn(p === page)} onClick={() => setPage(p)}>{p}</button>
            ))}
          </div>
        )}
      </div>

      {showModal && (
        <div style={s.modal} onClick={e => e.target === e.currentTarget && setShowModal(false)}>
          <div style={s.modalCard}>
            <div style={s.modalTitle}>New Product</div>
            <form onSubmit={handleCreate}>
              {[
                { key: 'name', label: 'Product name', type: 'text', placeholder: 'Enter name' },
                { key: 'price', label: 'Price (USD)', type: 'number', placeholder: '0.00' },
                { key: 'stock', label: 'Stock', type: 'number', placeholder: '0' },
                { key: 'category', label: 'Category', type: 'text', placeholder: 'Category 1' },
              ].map(f => (
                <div key={f.key}>
                  <label style={s.label}>{f.label}</label>
                  <input
                    style={s.input} type={f.type} placeholder={f.placeholder}
                    value={form[f.key]} required
                    onChange={e => setForm(prev => ({ ...prev, [f.key]: e.target.value }))}
                  />
                </div>
              ))}
              <div style={s.row}>
                <button type="button" style={s.btn('secondary')} onClick={() => setShowModal(false)}>Cancel</button>
                <button type="submit" style={s.btn('primary')}>Create</button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
