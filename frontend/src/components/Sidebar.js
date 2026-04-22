import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';

const nav = [
  { path: '/',         icon: '⬡', label: 'Dashboard' },
  { path: '/products', icon: '◈', label: 'Products' },
];

const s = {
  sidebar: {
    width: '220px', minHeight: '100vh',
    background: 'var(--bg2)',
    borderRight: '1px solid var(--border)',
    display: 'flex', flexDirection: 'column',
    padding: '24px 0', flexShrink: 0,
  },
  brand: {
    padding: '0 24px 32px',
    fontFamily: 'var(--font-display)',
    fontSize: '16px', fontWeight: 700,
    color: 'var(--text)',
    display: 'flex', alignItems: 'center', gap: '10px',
    borderBottom: '1px solid var(--border)',
    marginBottom: '16px',
  },
  dot: {
    width: 8, height: 8, borderRadius: '50%',
    background: 'var(--accent)',
    boxShadow: '0 0 8px var(--accent)',
    flexShrink: 0,
  },
  section: {
    padding: '0 12px', marginBottom: '4px',
  },
  item: (active) => ({
    display: 'flex', alignItems: 'center', gap: '10px',
    padding: '10px 12px', borderRadius: 'var(--radius-sm)',
    cursor: 'pointer', fontSize: '14px',
    color: active ? 'var(--accent)' : 'var(--text2)',
    background: active ? 'rgba(79,70,229,0.08)' : 'transparent',
    border: active ? '1px solid rgba(79,70,229,0.15)' : '1px solid transparent',
    transition: 'all 0.15s ease',
    fontWeight: active ? 600 : 400,
  }),
  icon: { fontSize: '16px', lineHeight: 1 },
  spacer: { flex: 1 },
  user: {
    margin: '16px 12px 0',
    padding: '12px',
    borderRadius: 'var(--radius-sm)',
    background: 'var(--bg3)',
    border: '1px solid var(--border)',
  },
  userName: { fontSize: '13px', fontWeight: 500, color: 'var(--text)' },
  userRole: { fontSize: '11px', color: 'var(--text3)', marginTop: '2px', textTransform: 'uppercase', letterSpacing: '0.08em' },
  logout: {
    marginTop: '8px', padding: '8px 12px',
    background: 'transparent', borderRadius: 'var(--radius-sm)',
    color: 'var(--text2)', fontSize: '12px',
    border: '1px solid var(--border)', width: '100%',
    textAlign: 'left', cursor: 'pointer',
    transition: 'all 0.15s',
  },
};

export default function Sidebar() {
  const navigate = useNavigate();
  const location = useLocation();
  const user = JSON.parse(localStorage.getItem('user') || '{}');

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    navigate('/login');
  };

  return (
    <div style={s.sidebar}>
      <div style={s.brand}>
        <span style={s.dot} />
        DD Workshop
      </div>
      <div style={{ padding: '0 12px', marginBottom: '24px' }}>
        {nav.map(item => (
          <div
            key={item.path}
            style={s.item(location.pathname === item.path)}
            onClick={() => navigate(item.path)}
          >
            <span style={s.icon}>{item.icon}</span>
            {item.label}
          </div>
        ))}
      </div>
      <div style={s.spacer} />
      <div style={{ padding: '0 12px' }}>
        <div style={s.user}>
          <div style={s.userName}>{user.username || 'User'}</div>
          <div style={s.userRole}>{user.role || 'user'}</div>
        </div>
        <button style={s.logout} onClick={logout}>← Sign out</button>
      </div>
    </div>
  );
}
