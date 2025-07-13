import ChatInterface from './components/ChatInterface';
import AuthForm from './components/AuthForm';
import { UserProvider } from './context/UserContext';
import { useUser } from './hooks/useUser';
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
    <UserProvider>
      <AppContent />
    </UserProvider>
  );
}
