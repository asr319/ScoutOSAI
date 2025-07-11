import ChatInterface from './components/ChatInterface';
import MemoryManager from './components/MemoryManager';
import './index.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 p-4 space-y-4">
      <ChatInterface />
      <MemoryManager />
    </div>
  );
}

export default App;
