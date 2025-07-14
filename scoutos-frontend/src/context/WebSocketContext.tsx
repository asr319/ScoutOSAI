/* eslint-disable react-refresh/only-export-components */
import { createContext, useState, useEffect, type ReactNode } from 'react'
import { useUser } from '../hooks/useUser'

interface WebSocketContextType {
  events: unknown[]
}

export const WebSocketContext = createContext<WebSocketContextType | undefined>(undefined)

export function WebSocketProvider({ children }: { children: ReactNode }) {
  const { user } = useUser()
  const [events, setEvents] = useState<unknown[]>([])

  useEffect(() => {
    if (!user) return
    const base = import.meta.env.VITE_API_URL || 'http://localhost:8000'
    const wsUrl = base.replace(/^http/, 'ws') + `/ws/${user.id}`
    const ws = new WebSocket(wsUrl)
    ws.addEventListener('message', (ev) => {
      try {
        setEvents((e) => [...e, JSON.parse(ev.data)])
      } catch {
        // ignore
      }
    })
    return () => {
      ws.close()
    }
  }, [user])

  return (
    <WebSocketContext.Provider value={{ events }}>
      {children}
    </WebSocketContext.Provider>
  )
}
