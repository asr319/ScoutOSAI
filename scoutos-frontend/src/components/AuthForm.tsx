import { useState } from 'react';
import { useUser } from '../hooks/useUser';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

type Mode = 'login' | 'register';

export default function AuthForm() {
  const [mode, setMode] = useState<Mode>('login');
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { setUser } = useUser();

  async function handleSubmit() {
    setError('');
    try {
      let data: { id: number; token: string } | null = null;

      if (mode === 'register') {
        const registerRes = await fetch(`${API_URL}/user/register`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password })
        });
        if (!registerRes.ok) {
          const body = await registerRes.json().catch(() => ({}));
          throw new Error(body.detail || 'Request failed');
        }

        const loginRes = await fetch(`${API_URL}/user/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password })
        });
        if (!loginRes.ok) {
          const body = await loginRes.json().catch(() => ({}));
          throw new Error(body.detail || 'Login failed');
        }
        data = await loginRes.json();
      } else {
        const loginRes = await fetch(`${API_URL}/user/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ username, password })
        });
        if (!loginRes.ok) {
          const body = await loginRes.json().catch(() => ({}));
          throw new Error(body.detail || 'Request failed');
        }
        data = await loginRes.json();
      }

      setUser({ id: data.id, username, token: data.token });
      setUsername('');
      setPassword('');
    } catch (err) {
      if (err instanceof Error) setError(err.message);
      else setError('Unknown error');
    }
  }

  return (
    <div className="max-w-sm mx-auto bg-white p-6 rounded-xl shadow">
      <h2 className="text-xl font-semibold mb-4 capitalize">{mode}</h2>
      <div className="flex flex-col gap-3">
        <input
          className="border rounded p-2"
          placeholder="Username"
          value={username}
          onChange={e => setUsername(e.target.value)}
        />
        <input
          className="border rounded p-2"
          type="password"
          placeholder="Password"
          value={password}
          onChange={e => setPassword(e.target.value)}
        />
        {error && <div className="text-red-600 text-sm">{error}</div>}
        <button
          className="bg-blue-600 text-white rounded p-2"
          onClick={handleSubmit}
        >{mode === 'login' ? 'Login' : 'Register'}</button>
        <button
          className="text-sm text-blue-700 underline"
          onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
        >
          {mode === 'login' ? 'Need an account? Register' : 'Have an account? Login'}
        </button>
      </div>
    </div>
  );
}
