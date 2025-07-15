import { useState, useEffect } from "react";
import { useUser } from "../hooks/useUser";
import LoadingSpinner from "./LoadingSpinner";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface Chain {
  id: number;
  name: string;
  actions: unknown[];
}

export default function ChainAdmin() {
  const { user } = useUser();
  const [name, setName] = useState("");
  const [actions, setActions] = useState<string>("[]");
  const [chains, setChains] = useState<Chain[]>([]);
  const [loading, setLoading] = useState(false);

  async function loadChains() {
    const res = await fetch(`${API_URL}/chain/list`);
    if (res.ok) {
      setChains(await res.json());
    }
  }

  useEffect(() => {
    loadChains();
  }, []);

  async function createChain() {
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/chain/create`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, actions: JSON.parse(actions) }),
      });
      if (res.ok) {
        setName("");
        setActions("[]");
        loadChains();
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-xl mx-auto p-4">
      <h2 className="text-xl font-bold mb-2">Chains</h2>
      <ul className="mb-4 space-y-1">
        {chains.map((c) => (
          <li key={c.id}>{c.name}</li>
        ))}
      </ul>
      <div className="flex flex-col gap-2">
        <input
          className="border p-2 rounded"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Chain name"
        />
        <textarea
          className="border p-2 rounded"
          rows={4}
          value={actions}
          onChange={(e) => setActions(e.target.value)}
          placeholder='[{"type":"chat","prompt":"hi"}]'
        />
        <button
          className="bg-primary text-white rounded p-2 flex items-center justify-center gap-2"
          onClick={createChain}
          disabled={loading || !user}
        >
          {loading && <LoadingSpinner />}Save Chain
        </button>
      </div>
    </div>
  );
}
