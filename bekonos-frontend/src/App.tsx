import { useState, useEffect } from "react";
import ChatInterface from "./components/ChatInterface";
import MemoryManager from "./components/MemoryManager";
import AnalyticsChart from "./components/AnalyticsChart";
import ChainAdmin from "./components/ChainAdmin";
import ProfileEditor from "./components/ProfileEditor";
import LogoutButton from "./components/LogoutButton";
import AuthForm from "./components/AuthForm";
import { useUser } from "./hooks/useUser";
import { Toaster } from "react-hot-toast";
import "./index.css";

function AppContent() {
  const { user } = useUser();
  const [page, setPage] = useState<
    "chat" | "memory" | "analytics" | "admin" | "profile"
  >("chat");
  const [dark, setDark] = useState(false);

  useEffect(() => {
    if (dark) {
      document.documentElement.classList.add("dark");
    } else {
      document.documentElement.classList.remove("dark");
    }
  }, [dark]);

  if (!user) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <AuthForm />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 dark:bg-gray-900 dark:text-gray-100 flex flex-col items-center p-4">
      <div className="self-end mb-2 flex gap-2">
        <button
          className="border rounded px-2 py-1"
          onClick={() => setDark((d) => !d)}
        >
          {dark ? "Light" : "Dark"} Mode
        </button>
        <LogoutButton />
      </div>
      <nav className="mb-4 space-x-4">
        <button
          className={`px-3 py-1 rounded ${page === "chat" ? "bg-primary text-white" : "bg-gray-200"}`}
          onClick={() => setPage("chat")}
        >
          Chat
        </button>
        <button
          className={`px-3 py-1 rounded ${page === "memory" ? "bg-primary text-white" : "bg-gray-200"}`}
          onClick={() => setPage("memory")}
        >
          Memories
        </button>
        <button
          className={`px-3 py-1 rounded ${page === "analytics" ? "bg-primary text-white" : "bg-gray-200"}`}
          onClick={() => setPage("analytics")}
        >
          Analytics
        </button>
        <button
          className={`px-3 py-1 rounded ${page === "admin" ? "bg-primary text-white" : "bg-gray-200"}`}
          onClick={() => setPage("admin")}
        >
          Admin
        </button>
        <button
          className={`px-3 py-1 rounded ${page === "profile" ? "bg-primary text-white" : "bg-gray-200"}`}
          onClick={() => setPage("profile")}
        >
          Profile
        </button>
      </nav>
      {page === "chat" && <ChatInterface />}
      {page === "memory" && <MemoryManager />}
      {page === "analytics" && <AnalyticsChart />}
      {page === "admin" && <ChainAdmin />}
      {page === "profile" && <ProfileEditor />}
    </div>
  );
}

export default function App() {
  return (
    <>
      <AppContent />
      <Toaster position="top-right" />
    </>
  );
}
