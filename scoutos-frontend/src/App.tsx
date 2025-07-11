import ChatInterface from './components/ChatInterface';
import MemoryManager from './components/MemoryManager';
import { Toaster } from 'react-hot-toast';
import './index.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 p-4">
      <Toaster position="top-right" />
      <div className="space-y-4">
        <ChatInterface />
        <MemoryManager />
      </div>
    </div>
  );
}

export default App;
