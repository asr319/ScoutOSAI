import { useState } from "react";

export default function ChatInterface() {
  const [messages, setMessages] = useState<{sender: string, text: string}[]>([]);
  const [input, setInput] = useState('');

  async function sendMessage() {
    if (!input.trim()) return;
    setMessages([...messages, {sender: 'user', text: input}]);
    const userText = input;
    setInput('');

    // Save to backend memory
    await fetch('http://localhost:8000/memory/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ user_id: 1, content: userText, topic: '', tags: [] })
    });

    // Get AI reply
    const aiRes = await fetch('http://localhost:8000/ai/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt: userText })
    });
    const aiData = await aiRes.json();
    setMessages(msgs => [...msgs, { sender: 'assistant', text: aiData.response }]);
  }

  return (
    <div className="w-full max-w-xl mx-auto my-8 bg-white rounded-2xl shadow-lg p-4">
      <div className="mb-4 h-80 overflow-y-auto">
        {messages.map((msg, i) => (
          <div key={i} className={msg.sender === 'user' ? 'text-right' : 'text-left'}>
            <span className={`inline-block p-2 my-1 rounded-lg ${msg.sender === 'user' ? 'bg-blue-200' : 'bg-gray-200'}`}>
              {msg.text}
            </span>
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input
          className="flex-1 border p-2 rounded-xl"
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
