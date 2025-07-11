import ChatInterface from './components/ChatInterface';
import './index.css';

function App() {
  const [user, setUser] = useState<any>(null);

  if (!user) {
    return <AuthForm onAuth={setUser} />;
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <ChatInterface />
    </div>
  );
}

export default App;
