import ChatInterface from './components/ChatInterface';
// Temporarily unused components
// import MemoryManager from './components/MemoryManager';
// import AuthForm from './components/AuthForm';
// import { Toaster } from 'react-hot-toast';
// import { UserProvider, useUser } from './context/UserContext';
import './index.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-100">
      <ChatInterface />
    </div>
  );
}

export default App;
