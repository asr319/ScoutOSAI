import React, { useEffect, useState } from "react";

export default function MemoryList() {
  const [memories, setMemories] = useState<any[]>([]);
  const [topic, setTopic] = useState('');

  useEffect(() => {
    fetch(`http://localhost:8000/memory/list?user_id=1`)
      .then(res => res.json())
      .then(data => setMemories(data));
  }, []);

  function searchByTopic() {
    fetch(`http://localhost:8000/memory/search?user_id=1&topic=${topic}`)
      .then(res => res.json())
      .then(data => setMemories(data));
  }

  return (
    <div className="w-full max-w-xl mx-auto my-8 bg-white rounded-2xl shadow-lg p-4">
      <h2 className="text-xl font-bold mb-2">Your Memories</h2>
      <div className="flex mb-4 gap-2">
        <input
          className="flex-1 border p-2 rounded-xl"
          value={topic}
          onChange={e => setTopic(e.target.value)}
          placeholder="Search by topic..."
        />
        <button className="bg-gray-800 text-white px-4 py-2 rounded-xl" onClick={searchByTopic}>
          Search
        </button>
      </div>
      <ul>
        {memories.map((m, i) => (
          <li key={i} className="mb-2 p-2 rounded-lg bg-gray-100">
            <div><strong>Topic:</strong> {m.topic}</div>
            <div>{m.content}</div>
            <div className="text-sm text-gray-500">{m.tags && m.tags.join(', ')}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
