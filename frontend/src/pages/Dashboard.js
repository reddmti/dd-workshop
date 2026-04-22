import React, { useState, useEffect } from 'react';
import Sidebar from '../components/Sidebar';
import { getProducts, getHealth, getSlowReport } from '../api';

const s = {
  root: { display: 'flex', minHeight: '100vh', background: 'var(--bg)' },
  main: { flex: 1, padding: '40px', overflow: 'auto' },
  header: { marginBottom: '40px' },
  title: {
    fontFamily: 'var(--font-display)',
    fontSize: '28px', fontWeight: 700, color: 'var(--text)',
    marginBottom: '6px',
  },
  sub: { fontSize: '14px', color: 'var(--text2)' },
  grid: {
    display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)',
    gap: '16px', marginBottom: '32px',
  },
  card: {
    padding: '24px', borderRadius: 'var(--radius)',
    background: 'var(--bg2)',
    border: '1px solid var(--border)',
    animation: 'fadeIn 0.4s ease',
  },
  cardLabel: {
    fontSize: '11px', color: 'var(--text3)',
    textTransform: 'uppercase', letterSpacing: '0.1em',
    fontFamily: 'var(--font-display)', marginBottom: '12px',
  },
  cardValue: {
    fontFamily: 'var(--font-display)',
    fontSize: '36px', fontWeight: 800, color: 'var(--text)',
    lineHeight: 1,
  },
  cardChange: { fontSize: '12px', color: 'var(--success)', marginTop: '8px' },
  section: {
    background: 'var(--bg2)', borderRadius: 'var(--radius)',
    border: '1px solid var(--border)', padding: '28px',
    marginBottom: '20px', animation: 'fadeIn 0.5s ease',
  },
  sectionTitle: {
    fontFamily: 'var(--font-display)',
    fontSize: '16px', fontWeight: 600, color: 'var(--text)',
    marginBottom: '20px',
  },
  btn: (variant) => ({
    padding: '12px 24px', borderRadius: 'var(--radius-sm)',
    fontSize: '13px', fontWeight: 600,
    fontFamily: 'var(--font-display)', letterSpacing: '0.04em',
    background: variant === 'danger' ? 'rgba(220,38,38,0.08)'
              : variant === 'accent' ? 'var(--accent)' : 'var(--bg2)',
    color: variant === 'danger' ? '#dc2626'
         : variant === 'accent' ? '#fff' : 'var(--text2)',
    border: variant === 'danger' ? '1px solid rgba(220,38,38,0.2)'
          : variant === 'accent' ? 'none' : '1px solid var(--border)',
    cursor: 'pointer',
    boxShadow: variant === 'accent' ? '0 4px 16px var(--accent-glow)' : 'none',
  }),
  status: (ok) => ({
    display: 'inline-flex', alignItems: 'center', gap: '8px',
    padding: '8px 16px', borderRadius: '100px',
    fontSize: '13px', fontWeight: 500,
    background: ok ? 'rgba(16,185,129,0.1)' : 'rgba(239,68,68,0.1)',
    color: ok ? 'var(--success)' : 'var(--danger)',
    border: `1px solid ${ok ? 'rgba(16,185,129,0.2)' : 'rgba(239,68,68,0.2)'}`,
  }),
  statusDot: (ok) => ({
    width: 6, height: 6, borderRadius: '50%',
    background: ok ? 'var(--success)' : 'var(--danger)',
  }),
  row: { display: 'flex', gap: '12px', alignItems: 'center', flexWrap: 'wrap' },
  result: {
    marginTop: '16px', padding: '16px',
    background: 'var(--bg3)', borderRadius: 'var(--radius-sm)',
    fontSize: '12px', color: 'var(--text2)', fontFamily: 'monospace',
    maxHeight: '120px', overflow: 'auto',
    border: '1px solid var(--border)',
  },
};

export default function Dashboard() {
  const [health, setHealth] = useState(null);
  const [stats, setStats] = useState(null);
  const [slowLoading, setSlowLoading] = useState(false);
  const [slowResult, setSlowResult] = useState(null);
  const [slowTime, setSlowTime] = useState(null);

  useEffect(() => {
    getHealth().then(r => setHealth(r.data)).catch(() => setHealth({ status: 'error' }));
    getProducts(1, 1).then(r => setStats(r.data)).catch(() => {});
  }, []);

  const runSlowReport = async () => {
    setSlowLoading(true);
    setSlowResult(null);
    const start = Date.now();
    try {
      const r = await getSlowReport();
      setSlowTime(((Date.now() - start) / 1000).toFixed(2));
      setSlowResult({ success: true, total: r.data.total });
    } catch {
      setSlowResult({ success: false });
      setSlowTime(((Date.now() - start) / 1000).toFixed(2));
    } finally {
      setSlowLoading(false);
    }
  };

  const ok = health?.status === 'healthy';

  return (
    <div style={s.root}>
      <Sidebar />
      <div style={s.main}>
        <div style={s.header}>
          <div style={s.title}>Dashboard</div>
          <div style={s.sub}>System overview and observability controls</div>
        </div>

        <div style={s.grid}>
          {[
            { label: 'API Status', value: ok ? 'Online' : 'Error', change: health?.version || '—' },
            { label: 'Total Products', value: stats?.total ?? '—', change: 'in database' },
            { label: 'Service', value: 'v2.0', change: 'dd-workshop-api' },
            { label: 'Environment', value: 'Workshop', change: 'production-like' },
          ].map((c, i) => (
            <div key={i} style={s.card}>
              <div style={s.cardLabel}>{c.label}</div>
              <div style={s.cardValue}>{c.value}</div>
              <div style={s.cardChange}>{c.change}</div>
            </div>
          ))}
        </div>

        <div style={s.section}>
          <div style={s.sectionTitle}>API Health</div>
          <div style={s.row}>
            <div style={s.status(ok)}>
              <span style={s.statusDot(ok)} />
              {ok ? 'All systems operational' : 'Service degraded'}
            </div>
            <span style={{ fontSize: '12px', color: 'var(--text3)' }}>
              {health ? `v${health.version} · ${health.service}` : 'Checking...'}
            </span>
          </div>
        </div>

        <div style={s.section}>
          <div style={s.sectionTitle}>⚡ Performance Demo Controls</div>
          <p style={{ fontSize: '13px', color: 'var(--text2)', marginBottom: '16px' }}>
            Trigger intentional performance degradation to demonstrate APM traces and Synthetic test failures in Datadog.
          </p>
          <div style={s.row}>
            <button style={s.btn('danger')} onClick={runSlowReport} disabled={slowLoading}>
              {slowLoading ? '⏳ Running slow report...' : '🐌 Trigger Slow Report'}
            </button>
            <span style={{ fontSize: '12px', color: 'var(--text3)' }}>
              N+1 queries + artificial delays → visible in APM
            </span>
          </div>
          {slowResult && (
            <div style={s.result}>
              {slowResult.success
                ? `✓ Completed in ${slowTime}s — ${slowResult.total} products processed. Check Datadog APM for traces.`
                : `✗ Failed after ${slowTime}s — Check Datadog APM for error traces.`}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
