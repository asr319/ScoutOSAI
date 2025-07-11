import React, { useState } from "react";
import AuthForm from "./components/AuthForm";
import ChatInterface from "./components/ChatInterface";
import MemoryList from "./components/MemoryList";
import "./index.css";

function App() {
  const [user, setUser] = useState<any>(null);

  if (!user) {
    return <AuthForm onAuth={setUser} />;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <h1 className="text-3xl font-bold text-center mt-8">ScoutOS Dashboard</h1>
      <div className="text-center text-lg">Welcome, {user.username}!</div>
      <ChatInterface user={user} />
      <MemoryList user={user} />
    </div>
  );
}

export default App;
