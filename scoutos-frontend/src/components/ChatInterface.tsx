import { useState } from "react";
import { useUser } from "../context/UserContext";

interface Memory {
  id: number;
  user_id: number;
  content: string;
  topic: string;
  tags: string[];
  timestamp: string;
}

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function ChatInterface() {
  const { user } = useUser();
  const [messages, setMessages] = useState<{ sender: string, text: string }[]>([]);
  const [input, setInput] = useState('');

  async function sendMessage() {
    if (!input.trim()) return;

    // Show the user's message immediately
    setMessages([...messages, { sender: 'user', text: input }]);
    const userText = input;
    setMessages((msgs) => [...msgs, { sender: 'user', text: userText }]);
    setInput('');

    if (!user) return;

    // Call the backend to store the memory
    try {
      const response = await fetch(`${API_URL}/memory/add`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: user.id,
          content: userText,
          topic: 'General',
          tags: [],
        }),
      });
      const data = await response.json();
      const saved: Memory | undefined = data.memory;

      // Display confirmation from the API using returned memory data
      const confirmation = saved
        ? `Memory "${saved.content}" saved (id ${saved.id}).`
        : 'Memory saved!';
      setMessages((msgs) => [
        ...msgs,
        { sender: 'assistant', text: confirmation },
      ]);
    } catch (err) {
      console.error(err);
      setMessages((msgs) => [
        ...msgs,
        { sender: 'assistant', text: 'Error saving memory!' },
      ]);
    }
  }

  return (
    <div className="w-full max-w-xl mx-auto my-8 bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-4">
      <div className="mb-4 h-80 overflow-y-auto">
        {messages.map((msg, i) => (
          <div key={i} className={msg.sender === "user" ? "text-right" : "text-left"}>
            <span className={`inline-block p-2 my-1 rounded-lg ${msg.sender === "user" ? "bg-blue-200" : "bg-gray-200"}`}>
              {msg.text}
            </span>
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          className="flex-1 border p-2 rounded-xl bg-white dark:bg-gray-700 dark:text-white"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask ScoutOS..."
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
        />
        <button className="bg-blue-600 text-white px-4 py-2 rounded-xl" onClick={sendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}
