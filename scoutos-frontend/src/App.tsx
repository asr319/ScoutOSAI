import ChatInterface from './components/ChatInterface';
import AuthForm from './components/AuthForm';
import { useUser } from './hooks/useUser';
import './index.css';

function App() {
  const { user } = useUser();
  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center">
      {user ? <ChatInterface /> : <AuthForm />}
    </div>
  );
}

export default App;
