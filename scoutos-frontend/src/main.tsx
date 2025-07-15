// BekonOS (c) 2025 asr319. All rights reserved. Proprietary.
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./App.tsx";
import { UserProvider } from "./context/UserContext";
import { registerSW } from "virtual:pwa-register";
import { WebSocketProvider } from "./context/WebSocketContext";

registerSW({ immediate: true });

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <UserProvider>
      <WebSocketProvider>
        <App />
      </WebSocketProvider>
    </UserProvider>
  </StrictMode>,
);
