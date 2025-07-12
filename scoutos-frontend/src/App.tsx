import ChatInterface from './components/ChatInterface';
import MemoryManager from './components/MemoryManager';
import AuthForm from './components/AuthForm';
import { Toaster } from 'react-hot-toast';
import { UserProvider } from './context/UserContext';
import { useUser } from './hooks/useUser';
import './index.css';

function Main() {
  const { user } = useUser();
  return user ? (
    <div className="space-y-4">
      <ChatInterface />
      <MemoryManager />
    </div>
  ) : (
    <AuthForm />
  );
}

function App() {
  return (
    <UserProvider>
      <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-4">
        <Toaster position="top-right" />
        <Main />
      </div>
    </UserProvider>
  );
}

export default App;
