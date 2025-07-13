import { useState, type FormEvent } from 'react';
import { useUser } from '../hooks/useUser';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export default function AuthForm() {
  const { setUser } = useUser();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [mode, setMode] = useState<'login' | 'register'>('login');
  const [error, setError] = useState('');

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError('');
    const res = await fetch(`${API_URL}/user/${mode}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });
    if (res.ok) {
      const data = await res.json();
      setUser({ id: data.id, username });
    } else {
      try {
        const data = await res.json();
        setError(data.detail || 'Error');
      } catch {
        setError('Error');
      }
    }
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white p-4 rounded-xl shadow space-y-2 w-80">
      <h2 className="text-xl font-semibold capitalize">{mode}</h2>
      {error && <div className="text-red-600" role="alert">{error}</div>}
      <input
        className="border p-2 rounded w-full"
        placeholder="Username"
        value={username}
        onChange={e => setUsername(e.target.value)}
      />
      <input
        className="border p-2 rounded w-full"
        type="password"
        placeholder="Password"
        value={password}
        onChange={e => setPassword(e.target.value)}
      />
      <button type="submit" className="bg-blue-600 text-white rounded p-2 w-full">
        {mode === 'login' ? 'Login' : 'Register'}
      </button>
      <button
        type="button"
        onClick={() => setMode(mode === 'login' ? 'register' : 'login')}
        className="text-sm text-blue-600 underline w-full"
      >
        {mode === 'login' ? 'Need an account? Register' : 'Have an account? Login'}
      </button>
    </form>
  );
}
