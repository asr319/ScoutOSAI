import { useState } from "react";
import toast from "react-hot-toast";

export default function ChatInterface() {
  const [messages, setMessages] = useState<{sender: string, text: string}[]>([]);
  const [input, setInput] = useState('');

  async function sendMessage() {
    if (!input.trim()) return;
    const userText = input;
    setMessages([...messages, { sender: "user", text: userText }]);
    setInput("");

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/memory/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: 1, content: userText, topic: "chat", tags: [] })
      });
      if (!res.ok) throw new Error(`Request failed: ${res.status}`);
      toast.success("Message saved");
    } catch (err) {
      console.error(err);
      toast.error("Failed to reach server");
    }

    // TODO: Display assistant response when backend is implemented
  }

  return (
    <div className="w-full max-w-xl mx-auto my-8 bg-white dark:bg-gray-800 rounded-2xl shadow-lg p-4">
      <div className="mb-4 h-80 overflow-y-auto">
          {messages.map((msg, i) => (
            <div key={i} className={msg.sender === 'user' ? 'text-right' : 'text-left'}>
              <span className={`inline-block p-2 my-1 rounded-lg ${msg.sender === 'user' ? 'bg-blue-200 dark:bg-blue-400' : 'bg-gray-200 dark:bg-gray-600'} text-gray-900 dark:text-white`}>
                {msg.text}
              </span>
            </div>
          ))}
      </div>
      <div className="flex gap-2">
        <input
          className="flex-1 border p-2 rounded-xl bg-white dark:bg-gray-700 dark:text-white"
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder="Ask ScoutOS..."
          onKeyDown={e => e.key === 'Enter' && sendMessage()}
        />
        <button
          className="bg-blue-600 text-white px-4 py-2 rounded-xl"
          onClick={sendMessage}
        >Send</button>
      </div>
    </div>
  );
}
