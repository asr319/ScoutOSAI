import React, { useState, useEffect } from "react";

interface Memory {
  id: number;
  content: string;
  topic: string;
  tags: string[];
}

export default function MemoryList({ user }: { user: any }) {
  const [memories, setMemories] = useState<Memory[]>([]);
  const [content, setContent] = useState("");
  const [topic, setTopic] = useState("");
  const [tags, setTags] = useState("");

  async function load() {
    const res = await fetch(`http://localhost:8000/memory/list/${user.id}`);
    if (res.ok) {
      const data = await res.json();
      setMemories(data.memories);
    }
  }

  useEffect(() => {
    load();
  }, [user]);

  async function addMemory(e: React.FormEvent) {
    e.preventDefault();
    await fetch("http://localhost:8000/memory/add", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: user.id,
        content,
        topic,
        tags: tags.split(",").map((t) => t.trim()).filter(Boolean),
      }),
    });
    setContent("");
    setTopic("");
    setTags("");
    load();
  }

  return (
    <div className="max-w-xl mx-auto bg-white rounded-2xl p-4 shadow-lg my-8">
      <h2 className="text-xl font-bold mb-2">Memories</h2>
      <ul className="mb-4">
        {memories.map((m) => (
          <li key={m.id} className="border-b py-1">
            <div className="font-semibold">{m.topic}</div>
            <div>{m.content}</div>
            <div className="text-sm text-gray-500">{m.tags.join(", ")}</div>
          </li>
        ))}
      </ul>
      <form onSubmit={addMemory} className="flex flex-col gap-2">
        <input
          className="border rounded-xl p-2"
          placeholder="Topic"
          value={topic}
          onChange={(e) => setTopic(e.target.value)}
        />
        <input
          className="border rounded-xl p-2"
          placeholder="Content"
          value={content}
          onChange={(e) => setContent(e.target.value)}
        />
        <input
          className="border rounded-xl p-2"
          placeholder="Tags comma separated"
          value={tags}
          onChange={(e) => setTags(e.target.value)}
        />
        <button type="submit" className="bg-blue-600 text-white px-4 py-2 rounded-xl">
          Add Memory
        </button>
      </form>
    </div>
  );
}
