import { useState } from "react"
import { toast } from 'react-hot-toast'
import { useUser } from "../hooks/useUser"
import LogoutButton from "./LogoutButton"
import LoadingSpinner from './LoadingSpinner'

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function ChatInterface() {
  const { user } = useUser();
  const [messages, setMessages] = useState<{sender: string, text: string}[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false)

  async function sendMessage() {
    if (!input.trim() || !user) return;

    setLoading(true)

    // Show the user's message immediately
    setMessages([...messages, { sender: 'user', text: input }]);
    const userText = input;
    setInput('');

    // Call the backend to store the memory
    try {
      const response = await fetch(`${API_URL}/memory/add`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(user?.token ? { Authorization: `Bearer ${user.token}` } : {}),
        },
        body: JSON.stringify({
          user_id: user?.id ?? 0,
          content: userText,
          topic: 'General',
          tags: [],
        }),
      });
      const data = await response.json()

      // Display confirmation from the API
      setMessages((msgs) => [
        ...msgs,
        { sender: 'assistant', text: data.message || 'Memory saved!' },
      ])
      toast.success('Memory saved')
    } catch (err) {
      console.error(err);
      setMessages((msgs) => [
        ...msgs,
        { sender: 'assistant', text: 'Error saving memory!' },
      ]);
      toast.error('Error saving memory')
    }
    // Fetch AI assistant reply
    try {
      const res = await fetch(`${API_URL}/ai/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ prompt: userText }),
      });
      if (res.ok) {
        const data = await res.json()
        setMessages((msgs) => [
          ...msgs,
          { sender: 'assistant', text: data.response },
        ])
        toast.success('AI response received')
      } else {
        const body = await res.json().catch(() => ({}))
        toast.error(body.detail || 'Error fetching AI response')
      }
    } catch (err) {
      console.error(err);
      setMessages((msgs) => [
        ...msgs,
        { sender: 'assistant', text: 'Error fetching AI response!' },
      ]);
      toast.error('Error fetching AI response')
    } finally {
      setLoading(false)
    }
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
          className="bg-blue-600 text-white px-4 py-2 rounded-xl flex items-center justify-center gap-2"
          onClick={sendMessage}
          disabled={loading}
        >
          {loading && <LoadingSpinner />}
          Send
        </button>
      </div>
    </div>
  );
}
