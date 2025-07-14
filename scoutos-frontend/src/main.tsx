import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.tsx'
import { UserProvider } from './context/UserContext'
<<<<<<< HEAD
import { registerSW } from 'virtual:pwa-register'

registerSW({ immediate: true })
=======
import { WebSocketProvider } from './context/WebSocketContext'
>>>>>>> origin/Next-Phase

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <UserProvider>
      <WebSocketProvider>
        <App />
      </WebSocketProvider>
    </UserProvider>
  </StrictMode>,
)
