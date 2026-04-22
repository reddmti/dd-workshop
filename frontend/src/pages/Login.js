import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../api';

const styles = {
  root: {
    minHeight: '100vh',
    display: 'flex',
    background: 'var(--bg)',
    position: 'relative',
    overflow: 'hidden',
  },
  bg: {
    position: 'absolute', inset: 0, zIndex: 0,
    background: `
      radial-gradient(ellipse 80% 60% at 20% 50%, rgba(79,70,229,0.06) 0%, transparent 60%),
      radial-gradient(ellipse 60% 80% at 80% 20%, rgba(99,102,241,0.04) 0%, transparent 50%)
    `,
  },
  grid: {
    position: 'absolute', inset: 0, zIndex: 0,
    backgroundImage: `
      linear-gradient(rgba(0,0,0,0.03) 1px, transparent 1px),
      linear-gradient(90deg, rgba(0,0,0,0.03) 1px, transparent 1px)
    `,
    backgroundSize: '40px 40px',
  },
  left: {
    flex: 1, display: 'flex', flexDirection: 'column',
    justifyContent: 'center', padding: '80px',
    position: 'relative', zIndex: 1,
  },
  brand: {
    fontFamily: 'var(--font-display)',
    fontSize: '13px', fontWeight: 600,
    letterSpacing: '0.15em', textTransform: 'uppercase',
    color: 'var(--accent2)', marginBottom: '64px',
    display: 'flex', alignItems: 'center', gap: '8px',
  },
  dot: {
    width: 8, height: 8, borderRadius: '50%',
    background: 'var(--accent)', display: 'inline-block',
    boxShadow: '0 0 10px var(--accent)',
    animation: 'pulse-glow 2s ease-in-out infinite',
  },
  headline: {
    fontFamily: 'var(--font-display)',
    fontSize: '52px', fontWeight: 800, lineHeight: 1.1,
    color: 'var(--text)', marginBottom: '16px',
    letterSpacing: '-0.02em',
  },
  sub: {
    fontSize: '17px', color: 'var(--text2)',
    fontWeight: 300, maxWidth: '400px', lineHeight: 1.7,
  },
  pills: {
    display: 'flex', gap: '8px', flexWrap: 'wrap', marginTop: '40px',
  },
  pill: {
    padding: '6px 14px', borderRadius: '100px',
    border: '1px solid var(--border)',
    fontSize: '12px', color: 'var(--text2)',
    background: 'rgba(255,255,255,0.03)',
    fontFamily: 'var(--font-display)', letterSpacing: '0.05em',
  },
  right: {
    width: '480px', display: 'flex', alignItems: 'center',
    justifyContent: 'center', padding: '40px',
    position: 'relative', zIndex: 1,
  },
  card: {
    width: '100%', padding: '48px',
    background: '#ffffff',
    border: '1px solid var(--border)',
    borderRadius: '20px',
    boxShadow: 'var(--shadow)',
    animation: 'fadeIn 0.5s ease',
  },
  cardTitle: {
    fontFamily: 'var(--font-display)',
    fontSize: '24px', fontWeight: 700,
    color: 'var(--text)', marginBottom: '6px',
  },
  cardSub: {
    fontSize: '14px', color: 'var(--text2)', marginBottom: '36px',
  },
  label: {
    display: 'block', fontSize: '12px', fontWeight: 500,
    color: 'var(--text2)', marginBottom: '8px',
    textTransform: 'uppercase', letterSpacing: '0.08em',
    fontFamily: 'var(--font-display)',
  },
  input: {
    width: '100%', padding: '14px 16px',
    background: 'var(--bg2)',
    border: '1px solid var(--border)',
    borderRadius: 'var(--radius-sm)',
    color: 'var(--text)', fontSize: '15px',
    marginBottom: '20px',
  },
  btn: {
    width: '100%', padding: '15px',
    background: 'var(--accent)',
    borderRadius: 'var(--radius-sm)',
    color: '#fff', fontSize: '15px',
    fontWeight: 600, fontFamily: 'var(--font-display)',
    letterSpacing: '0.04em',
    boxShadow: '0 4px 20px var(--accent-glow)',
    marginTop: '8px',
  },
  btnDisabled: {
    opacity: 0.6, cursor: 'not-allowed',
  },
  error: {
    padding: '12px 16px', borderRadius: 'var(--radius-sm)',
    background: 'rgba(239,68,68,0.1)',
    border: '1px solid rgba(239,68,68,0.2)',
    color: '#fca5a5', fontSize: '13px', marginBottom: '16px',
  },
  hint: {
    marginTop: '24px', padding: '16px',
    borderRadius: 'var(--radius-sm)',
    background: 'var(--bg2)',
    border: '1px solid var(--border)',
    fontSize: '12px', color: 'var(--text2)',
  },
  hintRow: { display: 'flex', justifyContent: 'space-between', marginBottom: '4px' },
  hintKey: { color: 'var(--text)', fontWeight: 500 },
};

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async e => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      const res = await login(username, password);
      localStorage.setItem('token', res.data.token);
      localStorage.setItem('user', JSON.stringify(res.data.user));
      navigate('/');
    } catch {
      setError('Invalid username or password. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.root}>
      <div style={styles.bg} />
      <div style={styles.grid} />
      <div style={styles.left}>
        <div style={styles.brand}>
          <span style={styles.dot} />
          DD Workshop
        </div>
        <h1 style={styles.headline}>
          Observability<br />
          <span style={{ color: 'var(--accent2)' }}>Starts Here</span>
        </h1>
        <p style={styles.sub}>
          Full-stack demo platform for Datadog CI Visibility,
          Code Analysis, APM and Synthetic Monitoring.
        </p>
        <div style={styles.pills}>
          {['CI Visibility', 'Code Analysis', 'APM', 'Synthetics', 'DORA Metrics'].map(t => (
            <span key={t} style={styles.pill}>{t}</span>
          ))}
        </div>
      </div>
      <div style={styles.right}>
        <div style={styles.card}>
          <div style={styles.cardTitle}>Welcome back</div>
          <div style={styles.cardSub}>Sign in to your account to continue</div>
          {error && <div style={styles.error}>{error}</div>}
          <form onSubmit={handleSubmit}>
            <label style={styles.label}>Username</label>
            <input
              style={styles.input}
              type="text"
              value={username}
              onChange={e => setUsername(e.target.value)}
              placeholder="Enter your username"
              required
            />
            <label style={styles.label}>Password</label>
            <input
              style={styles.input}
              type="password"
              value={password}
              onChange={e => setPassword(e.target.value)}
              placeholder="Enter your password"
              required
            />
            <button
              type="submit"
              style={{ ...styles.btn, ...(loading ? styles.btnDisabled : {}) }}
              disabled={loading}
            >
              {loading ? 'Signing in...' : 'Sign in →'}
            </button>
          </form>
          <div style={styles.hint}>
            <div style={{ ...styles.hintRow, marginBottom: '8px' }}>
              <span style={{ fontSize: '11px', color: 'var(--text3)', textTransform: 'uppercase', letterSpacing: '0.1em' }}>Demo credentials</span>
            </div>
            {[['admin', 'admin123'], ['demo', 'demo2024']].map(([u, p]) => (
              <div key={u} style={styles.hintRow}>
                <span style={styles.hintKey}>{u}</span>
                <span style={{ color: 'var(--text3)' }}>{p}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
