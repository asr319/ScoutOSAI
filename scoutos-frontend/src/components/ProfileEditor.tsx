import { useEffect, useState } from "react";
import { toast } from "react-hot-toast";
import { useUser } from "../hooks/useUser";
import LoadingSpinner from "./LoadingSpinner";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface Preferences {
  theme: "light" | "dark";
  notify: boolean;
}

export default function ProfileEditor() {
  const { user } = useUser();
  const [prefs, setPrefs] = useState<Preferences>({
    theme: "light",
    notify: true,
  });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function fetchProfile() {
      if (!user) return;
      const res = await fetch(`${API_URL}/user/profile?user_id=${user.id}`, {
        headers: user.token ? { Authorization: `Bearer ${user.token}` } : {},
      });
      if (res.ok) {
        const data = await res.json();
        if (data.preferences) {
          setPrefs({
            theme: data.preferences.theme || "light",
            notify: data.preferences.notify ?? true,
          });
        }
      }
    }
    fetchProfile();
  }, [user]);

  async function save() {
    if (!user) return;
    setLoading(true);
    try {
      const res = await fetch(`${API_URL}/user/profile`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          ...(user.token ? { Authorization: `Bearer ${user.token}` } : {}),
        },
        body: JSON.stringify({ user_id: user.id, preferences: prefs }),
      });
      if (res.ok) {
        toast.success("Profile saved");
      } else {
        const body = await res.json().catch(() => ({}));
        toast.error(body.detail || "Failed to save");
      }
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="bg-white rounded-xl shadow p-4 max-w-sm">
      <h2 className="text-xl font-semibold mb-2">Profile</h2>
      <div className="flex flex-col gap-3">
        <label className="flex justify-between items-center">
          Theme
          <select
            className="border p-2 rounded"
            value={prefs.theme}
            onChange={(e) =>
              setPrefs({
                ...prefs,
                theme: e.target.value as Preferences["theme"],
              })
            }
          >
            <option value="light">Light</option>
            <option value="dark">Dark</option>
          </select>
        </label>
        <label className="flex items-center gap-2">
          <input
            type="checkbox"
            checked={prefs.notify}
            onChange={(e) => setPrefs({ ...prefs, notify: e.target.checked })}
          />
          Enable Notifications
        </label>
        <button
          className="bg-primary text-white rounded p-2 flex items-center justify-center gap-2"
          onClick={save}
          disabled={loading}
        >
          {loading && <LoadingSpinner />}
          Save
        </button>
      </div>
    </div>
  );
}
