import { useState } from 'react';
import ChatInterface from './components/ChatInterface';
import MemoryManager from './components/MemoryManager';
import LogoutButton from './components/LogoutButton';
import AuthForm from './components/AuthForm';
import { useUser } from './hooks/useUser';
import { Toaster } from 'react-hot-toast';
import './index.css';

function AppContent() {
  const { user } = useUser();
  const [page, setPage] = useState<'chat' | 'memory'>('chat');

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <AuthForm />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col items-center p-4">
      <div className="self-end mb-2">
        <LogoutButton />
      </div>
      <nav className="mb-4 space-x-4">
        <button
          className={`px-3 py-1 rounded ${page === 'chat' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
          onClick={() => setPage('chat')}
        >
          Chat
        </button>
        <button
          className={`px-3 py-1 rounded ${page === 'memory' ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}
          onClick={() => setPage('memory')}
        >
          Memories
        </button>
      </nav>
      {page === 'chat' ? <ChatInterface /> : <MemoryManager />}
    </div>
  );
}

export default function App() {
  return (
    <>
      <AppContent />
      <Toaster position="top-right" />
    </>
  );
}
