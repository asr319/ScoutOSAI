import { useEffect, useState } from "react";
import { useUser } from "../context/UserContext";

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

interface Memory {
  id: number;
  user_id: number;
  content: string;
  topic: string;
  tags: string[];
  timestamp: string;
}

export default function MemoryManager() {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [content, setContent] = useState("");
  const [topic, setTopic] = useState("");
  const [tags, setTags] = useState("");
  const [searchTopic, setSearchTopic] = useState("");
  const [searchTag, setSearchTag] = useState("");
  const { user } = useUser();

  async function loadMemories() {
    if (!user) return;
    const res = await fetch(`${API_URL}/memory/list?user_id=${user.id}`);
    const res = await fetch(`${API_URL}/memory/list?user_id=${userId}`);
    if (res.ok) {
      const data = await res.json();
      setMemories(data);
    }
  }

  useEffect(() => { loadMemories(); }, []);

  async function addMemory() {
    if (!user) return;
    const res = await fetch(`${API_URL}/memory/add`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: user.id,
        content,
        topic,
        tags: tags.split(',').map(t => t.trim()).filter(t => t)
      })
    });
    if (res.ok) {
      const { memory } = await res.json();
      setMemories([...memories, mem.memoryory]);
      setContent("");
      setTopic("");
      setTags("");
    }
  }

  async function search() {
    if (!user) return;
    const params = new URLSearchParams();
    params.append("user_id", String(user.id));
    if (searchTopic) params.append("topic", searchTopic);
    if (searchTag) params.append("tag", searchTag);
    const res = await fetch(`${API_URL}/memory/search?${params.toString()}`);
    if (res.ok) {
      const data = await res.json();
      setMemories(data);
    }
  }

  async function deleteMemory(id: number) {
    await fetch(`${API_URL}/memory/delete/${id}`, { method: 'DELETE' });
    setMemories(memories.filter(m => m.id !== id));
  }

  return (
    <div className="bg-white rounded-xl shadow p-4">
      <h2 className="text-xl font-semibold mb-2">Memories</h2>
      <div className="flex flex-col gap-2 mb-4">
        <input className="border p-2 rounded" placeholder="Content" value={content} onChange={e => setContent(e.target.value)} />
        <input className="border p-2 rounded" placeholder="Topic" value={topic} onChange={e => setTopic(e.target.value)} />
        <input className="border p-2 rounded" placeholder="Tags comma separated" value={tags} onChange={e => setTags(e.target.value)} />
        <button className="bg-blue-600 text-white rounded p-2" onClick={addMemory}>Add Memory</button>
      </div>

      <div className="flex gap-2 mb-4">
        <input className="border p-2 rounded" placeholder="Search topic" value={searchTopic} onChange={e => setSearchTopic(e.target.value)} />
        <input className="border p-2 rounded" placeholder="Search tag" value={searchTag} onChange={e => setSearchTag(e.target.value)} />
        <button className="bg-green-600 text-white rounded p-2" onClick={search}>Search</button>
      </div>

      <ul className="space-y-2">
        {memories.map(m => (
          <li key={m.id} className="border p-2 rounded flex justify-between">
            <div>
              <div className="font-semibold">{m.topic}</div>
              <div>{m.content}</div>
              <div className="text-sm text-gray-500">{m.tags.join(', ')}</div>
            </div>
            <button className="text-red-600" onClick={() => deleteMemory(m.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
