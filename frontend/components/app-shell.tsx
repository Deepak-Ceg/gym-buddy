"use client";

import { useEffect, useState } from "react";

import { Dashboard } from "@/components/dashboard";
import { getDashboard, getMe, login, logout, type DashboardResponse } from "@/lib/api";

export function AppShell() {
  const [loading, setLoading] = useState(true);
  const [authChecked, setAuthChecked] = useState(false);
  const [dashboard, setDashboard] = useState<DashboardResponse | null>(null);
  const [email, setEmail] = useState("deepak@example.com");
  const [password, setPassword] = useState("deepak123");
  const [error, setError] = useState<string | null>(null);

  async function loadDashboard() {
    setLoading(true);
    try {
      const data = await getDashboard();
      setDashboard(data);
      setError(null);
    } catch {
      setDashboard(null);
      setError("Could not load your dashboard.");
    } finally {
      setLoading(false);
      setAuthChecked(true);
    }
  }

  useEffect(() => {
    async function bootstrap() {
      const me = await getMe();
      if (!me) {
        setLoading(false);
        setAuthChecked(true);
        return;
      }
      await loadDashboard();
    }

    void bootstrap();
  }, []);

  async function handleLogin(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError(null);
    try {
      await login({ email, password });
      await loadDashboard();
    } catch {
      setError("Login failed. Try the seeded demo credentials.");
      setLoading(false);
      setAuthChecked(true);
    }
  }

  async function handleLogout() {
    await logout();
    setDashboard(null);
    setAuthChecked(true);
  }

  if (loading && !dashboard) {
    return (
      <main className="page">
        <section className="card auth-card">
          <h1>Loading Gym Buddy</h1>
          <p className="muted">Checking your session and loading your dashboard.</p>
        </section>
      </main>
    );
  }

  if (!dashboard && authChecked) {
    return (
      <main className="page">
        <section className="card auth-card">
          <p className="eyebrow">Buddy Login</p>
          <h1>Sign in to Gym Buddy</h1>
          <p className="lead">
            Each buddy signs in separately and can only submit their own daily check-in. The leaderboard and buddy
            view stay shared.
          </p>

          <form className="auth-form" onSubmit={handleLogin}>
            <label>
              <span>Email</span>
              <input onChange={(event) => setEmail(event.target.value)} type="email" value={email} />
            </label>
            <label>
              <span>Password</span>
              <input onChange={(event) => setPassword(event.target.value)} type="password" value={password} />
            </label>
            <button className="submit-button" disabled={loading} type="submit">
              {loading ? "Signing in..." : "Sign In"}
            </button>
          </form>

          <div className="demo-credentials">
            <strong>Demo logins</strong>
            <p>Deepak: `deepak@example.com` / `deepak123`</p>
            <p>Arun: `arun@example.com` / `arun123`</p>
          </div>

          {error ? <p className="error-text">{error}</p> : null}
        </section>
      </main>
    );
  }

  if (!dashboard) {
    return null;
  }

  return <Dashboard data={dashboard} onLogout={handleLogout} onRefresh={loadDashboard} />;
}
