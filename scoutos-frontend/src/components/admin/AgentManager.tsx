import { useEffect, useState } from "react";
import { useUser } from "../../hooks/useUser";
import LoadingSpinner from "../LoadingSpinner";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface AgentConfig {
  name: string;
  enabled: boolean;
  settings: Record<string, unknown>;
}

export default function AgentManager() {
  useUser();
  const [configs, setConfigs] = useState<AgentConfig[]>([]);
  const [loading, setLoading] = useState(false);

  async function loadConfigs() {
    const res = await fetch(`${API_URL}/agent/config`);
    if (res.ok) {
      setConfigs(await res.json());
    }
  }

  useEffect(() => {
    loadConfigs();
  }, []);

  async function toggle(name: string, enabled: boolean) {
    setLoading(true);
    await fetch(`${API_URL}/agent/enable`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ name, enabled }),
    });
    setConfigs(configs.map((c) => (c.name === name ? { ...c, enabled } : c)));
    setLoading(false);
  }

  return (
    <div className="p-4 bg-white rounded shadow">
      <h2 className="text-xl font-semibold mb-2">Agent Config</h2>
      {loading && <LoadingSpinner />}
      <ul className="space-y-2">
        {configs.map((cfg) => (
          <li
            key={cfg.name}
            className="flex justify-between border p-2 rounded"
          >
            <span>{cfg.name}</span>
            <label className="flex items-center gap-1">
              <input
                type="checkbox"
                checked={cfg.enabled}
                onChange={(e) => toggle(cfg.name, e.target.checked)}
              />
              Enabled
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
}
