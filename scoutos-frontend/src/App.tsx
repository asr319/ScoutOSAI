import ChatInterface from './components/ChatInterface';
import MemoryList from './components/MemoryList';
import './index.css';

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <h1 className="text-3xl font-bold text-center mt-8">ScoutOS Dashboard</h1>
      <ChatInterface />
      <MemoryList />
    </div>
  );
}

export default App;
