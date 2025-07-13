import ChatInterface from './components/ChatInterface';
import AuthForm from './components/AuthForm';
import { useUser } from './hooks/useUser';
import { Toaster } from 'react-hot-toast';
import { UserProvider } from '../context/UserContext';
import './index.css';

function AppContent() {
  const { user } = useUser();
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      {user ? <ChatInterface /> : <AuthForm />}
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
