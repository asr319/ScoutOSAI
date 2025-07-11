import ChatInterface from './components/ChatInterface';
import { Toaster } from 'react-hot-toast';
import './index.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900">
      <Toaster position="top-right" />
      <ChatInterface />
    </div>
  );
}

export default App;
