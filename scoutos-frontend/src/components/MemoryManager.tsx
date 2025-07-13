import { useCallback, useEffect, useState } from "react";
import { toast } from 'react-hot-toast'
import { useUser } from "../hooks/useUser";

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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
  const [suggestedTags, setSuggestedTags] = useState<string[]>([]);
  const [searchTopic, setSearchTopic] = useState("");
  const [searchTag, setSearchTag] = useState("");
  const [editing, setEditing] = useState<Memory | null>(null);
  const [editContent, setEditContent] = useState("");
  const [editTopic, setEditTopic] = useState("");
  const [editTags, setEditTags] = useState("");
  const { user } = useUser();

  const loadMemories = useCallback(async () => {
    if (!user) return;
    const res = await fetch(`${API_URL}/memory/list?user_id=${user.id}`, {
      headers: user.token ? { Authorization: `Bearer ${user.token}` } : {},
    });
    if (res.ok) {
      const data = await res.json();
      setMemories(data);
    }
  }, [user]);

  useEffect(() => { loadMemories(); }, [loadMemories]);

  async function fetchTagsFor(contentText: string) {
    if (!contentText) return;
    const res = await fetch(`${API_URL}/ai/tags`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(user?.token ? { Authorization: `Bearer ${user.token}` } : {}),
      },
      body: JSON.stringify({ content: contentText }),
    });
    if (res.ok) {
      const data = await res.json();
      if (Array.isArray(data.tags)) {
        setSuggestedTags(data.tags);
        toast.success(`Suggested tags: ${data.tags.join(', ')}`);
      }
    }
  }

  async function addMemory() {
    if (!user) return;
    const res = await fetch(`${API_URL}/memory/add`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        ...(user.token ? { Authorization: `Bearer ${user.token}` } : {}),
      },
      body: JSON.stringify({
        user_id: user.id,
        content,
        topic,
        tags: tags.split(',').map(t => t.trim()).filter(t => t)
      })
    });
    if (res.ok) {
      const mem = await res.json();
      setMemories([...memories, mem.memory]);
      setContent("");
      setTopic("");
      setTags("");
      fetchTagsFor(content);
    }
  }

  async function search() {
    if (!user) return;
    const params = new URLSearchParams();
    params.append("user_id", String(user.id));
    if (searchTopic) params.append("topic", searchTopic);
    if (searchTag) params.append("tag", searchTag);
    const res = await fetch(`${API_URL}/memory/search?${params.toString()}`, {
      headers: user.token ? { Authorization: `Bearer ${user.token}` } : {},
    });
    if (res.ok) {
      const data = await res.json();
      setMemories(data);
    }
  }

  async function deleteMemory(id: number) {
    await fetch(`${API_URL}/memory/delete/${id}?user_id=${user.id}`, {
      method: 'DELETE',
      headers: user?.token ? { Authorization: `Bearer ${user.token}` } : {},
    });
    setMemories(memories.filter(m => m.id !== id));
  }

  function startEdit(mem: Memory) {
    setEditing(mem);
    setEditContent(mem.content);
    setEditTopic(mem.topic);
    setEditTags(mem.tags.join(', '));
  }

  async function saveEdit() {
    if (!editing || !user) return;
    const res = await fetch(`${API_URL}/memory/update/${editing.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        ...(user.token ? { Authorization: `Bearer ${user.token}` } : {}),
      },
      body: JSON.stringify({
        user_id: user.id,
        content: editContent,
        topic: editTopic,
        tags: editTags.split(',').map(t => t.trim()).filter(t => t),
      }),
    });
    if (res.ok) {
      const data = await res.json();
      setMemories(memories.map(m => (m.id === editing.id ? data.memory : m)));
      setEditing(null);
    }
  }

  async function requestSummary() {
    if (!user) return;
    const res = await fetch(`${API_URL}/ai/summary`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(user.token ? { Authorization: `Bearer ${user.token}` } : {}),
      },
      body: JSON.stringify({ content }),
    });
    if (res.ok) {
      const data = await res.json();
      toast.success(data.summary || 'Summary requested');
    }
  }

  async function requestMergeAdvice() {
    if (!user) return;
    const res = await fetch(`${API_URL}/ai/merge`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...(user.token ? { Authorization: `Bearer ${user.token}` } : {}),
      },
      body: JSON.stringify({
        memory_a: memories[0]?.content || '',
        memory_b: memories[1]?.content || '',
      }),
    });
    if (res.ok) {
      const data = await res.json();
      toast.success(data.message || 'Merge advice requested');
    }
  }

  return (
    <div className="bg-white rounded-xl shadow p-4">
      <h2 className="text-xl font-semibold mb-2">Memories</h2>
      <div className="flex flex-col gap-2 mb-4">
        <input className="border p-2 rounded" placeholder="Content" value={content} onChange={e => setContent(e.target.value)} />
        <input className="border p-2 rounded" placeholder="Topic" value={topic} onChange={e => setTopic(e.target.value)} />
        <input className="border p-2 rounded" placeholder="Tags comma separated" value={tags} onChange={e => setTags(e.target.value)} />
        <button className="bg-blue-600 text-white rounded p-2" onClick={addMemory}>Add Memory</button>
        {suggestedTags.length > 0 && (
          <div className="text-sm text-gray-600">Suggested tags: {suggestedTags.join(', ')}</div>
        )}
      </div>

      <div className="flex gap-2 mb-4">
        <input className="border p-2 rounded" placeholder="Search topic" value={searchTopic} onChange={e => setSearchTopic(e.target.value)} />
        <input className="border p-2 rounded" placeholder="Search tag" value={searchTag} onChange={e => setSearchTag(e.target.value)} />
        <button className="bg-green-600 text-white rounded p-2" onClick={search}>Search</button>
      </div>

      <div className="flex gap-2 mb-4">
        <button className="bg-purple-600 text-white rounded p-2" onClick={requestSummary}>Get Summary</button>
        <button className="bg-purple-600 text-white rounded p-2" onClick={requestMergeAdvice}>Merge Advice</button>
      </div>

      <ul className="space-y-2">
        {memories.map(m => (
          <li key={m.id} className="border p-2 rounded">
            {editing?.id === m.id ? (
              <div className="flex flex-col gap-2">
                <input
                  className="border p-2 rounded"
                  value={editContent}
                  onChange={e => setEditContent(e.target.value)}
                />
                <input
                  className="border p-2 rounded"
                  value={editTopic}
                  onChange={e => setEditTopic(e.target.value)}
                />
                <input
                  className="border p-2 rounded"
                  value={editTags}
                  onChange={e => setEditTags(e.target.value)}
                />
                <div className="flex gap-2">
                  <button
                    className="bg-blue-600 text-white rounded p-2"
                    onClick={saveEdit}
                  >
                    Save
                  </button>
                  <button
                    className="rounded p-2 border"
                    onClick={() => setEditing(null)}
                  >
                    Cancel
                  </button>
                </div>
              </div>
            ) : (
              <div className="flex justify-between">
                <div>
                  <div className="font-semibold">{m.topic}</div>
                  <div>{m.content}</div>
                  <div className="text-sm text-gray-500">{m.tags.join(', ')}</div>
                </div>
                <div className="flex flex-col items-end gap-1">
                  <button className="text-blue-600" onClick={() => startEdit(m)}>Edit</button>
                  <button className="text-red-600" onClick={() => deleteMemory(m.id)}>Delete</button>
                </div>
              </div>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
}
