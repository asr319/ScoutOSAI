import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { render, fireEvent, waitFor } from '@testing-library/react'
import MemoryManager from './MemoryManager'
import { UserContext, type User } from '../context/UserContext'
import type { Mock } from 'vitest'

function renderWithUser(fetchMock: Mock) {
  const user: User = { id: 1, username: 'bob', token: 'tok' }
  vi.stubGlobal('fetch', fetchMock)
  return render(
    <UserContext.Provider value={{ user, setUser: vi.fn() }}>
      <MemoryManager />
    </UserContext.Provider>
  )
}

describe('MemoryManager API calls', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })
  afterEach(() => {
    vi.restoreAllMocks()
  })

  it('requests tags and merge advice', async () => {
    const memories = [
      { id: 1, user_id: 1, content: 'a', topic: 't', tags: [], timestamp: '' },
      { id: 2, user_id: 1, content: 'b', topic: 't', tags: [], timestamp: '' },
    ]
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve(memories) }) // list
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ tags: [] }) })
      .mockResolvedValue({ ok: true, json: () => Promise.resolve({ verdict: 'merge!' }) })

    const { getAllByText, getAllByPlaceholderText, getByText, findByText } = renderWithUser(fetchMock)

    fireEvent.change(getAllByPlaceholderText('Content')[0], { target: { value: 'foo' } })
    fireEvent.click(getByText('Suggest Tags'))
    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith(expect.stringContaining('/ai/tags'), expect.any(Object))
    })
    const tagCall = fetchMock.mock.calls.find(c => (c[0] as string).includes('/ai/tags'))
    expect(tagCall).toBeTruthy()
    if (tagCall) {
      expect(JSON.parse((tagCall[1] as RequestInit).body as string)).toEqual({ text: 'foo' })
    }

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2))

    fireEvent.click(getAllByText('Merge Advice')[0])
    await waitFor(() => {
      expect(
        fetchMock.mock.calls.some(
          c =>
            (c[0] as string).includes('/ai/merge') &&
            JSON.parse((c[1] as RequestInit).body as string).memory_ids[0] === 1
        )
      ).toBe(true)
    })
    expect(await findByText('merge!')).toBeTruthy()
  })
})
