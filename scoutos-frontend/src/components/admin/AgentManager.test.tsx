import { describe, it, expect, vi, type Mock } from 'vitest'
import { render, waitFor } from '@testing-library/react'
import AgentManager from './AgentManager'
import { UserContext, type User } from '../../context/UserContext'

const user: User = { id: 1, username: 'bob', token: 'tok' }

function renderComp(fetchMock: Mock) {
  vi.stubGlobal('fetch', fetchMock)
  return render(
    <UserContext.Provider value={{ user, setUser: vi.fn() }}>
      <AgentManager />
    </UserContext.Provider>
  )
}

describe('AgentManager', () => {
  it('fetches configs on load', async () => {
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: () => Promise.resolve([{ name: 'a', enabled: true, settings: {} }]) })
    const { findByText } = renderComp(fetchMock)
    expect(await findByText('a')).toBeTruthy()
    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalled()
    })
  })
})
