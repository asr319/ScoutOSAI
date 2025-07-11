import React, { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function AuthForm({ onAuth }: { onAuth: (user: any) => void }) {
  const [mode, setMode] = useState("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [msg, setMsg] = useState("");

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    const res = await fetch(`${API_URL}/user/${mode}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
    });
    const data = await res.json();
    if (res.ok) {
      setMsg(data.message);
      onAuth({ username, id: data.id });
    } else {
      setMsg(data.detail);
    }
  }

  return (
    <form onSubmit={submit} className="max-w-sm mx-auto my-8 bg-white rounded-2xl shadow-lg p-6">
      <h2 className="text-xl font-bold mb-4">{mode === "login" ? "Login" : "Register"}</h2>
      <input className="w-full mb-2 p-2 border rounded-xl" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
      <input className="w-full mb-2 p-2 border rounded-xl" placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
      <button className="bg-blue-600 text-white px-4 py-2 rounded-xl w-full" type="submit">{mode === "login" ? "Login" : "Register"}</button>
      <button type="button" className="underline text-blue-600 mt-2" onClick={() => setMode(mode === "login" ? "register" : "login")}> 
        {mode === "login" ? "No account? Register" : "Already have an account? Login"}
      </button>
      {msg && <div className="text-center text-red-600 mt-2">{msg}</div>}
    </form>
  );
}
