import { describe, it, expect, vi } from 'vitest'
import { render } from '@testing-library/react'
import { WebSocketProvider } from './WebSocketContext'
import { UserContext, type User } from './UserContext'

function renderWithUser(user: User) {
  return render(
    <UserContext.Provider value={{ user, setUser: vi.fn() }}>
      <WebSocketProvider>
        <div>child</div>
      </WebSocketProvider>
    </UserContext.Provider>
  )
}

describe('WebSocketProvider', () => {
  it('opens connection with user id', () => {
    const wsMock = vi.fn(() => ({ addEventListener: vi.fn(), close: vi.fn() }))
    vi.stubGlobal('WebSocket', wsMock)
    renderWithUser({ id: 1, username: 'bob', token: 't' })
    expect(wsMock).toHaveBeenCalledWith('ws://localhost:8000/ws/1')
  })
})
