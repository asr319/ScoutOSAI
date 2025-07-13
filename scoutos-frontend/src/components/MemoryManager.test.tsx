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

  it('calls /ai/tags after adding memory', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve([]) }) // list
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ memory: { id: 1, user_id: 1, content: 'c', topic: 't', tags: [] } }) }) // add
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ tags: ['x'] }) }) // tags

    const { getByPlaceholderText, getByText } = renderWithUser(fetchMock)

    fireEvent.change(getByPlaceholderText('Content'), { target: { value: 'c' } })
    fireEvent.change(getByPlaceholderText('Topic'), { target: { value: 't' } })
    fireEvent.change(getByPlaceholderText('Tags comma separated'), { target: { value: '' } })
    fireEvent.click(getByText('Add Memory'))

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith(expect.stringContaining('/ai/tags'), expect.any(Object))
    })
  })

  it('requests summary and merge advice', async () => {
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve([]) }) // list
      .mockResolvedValue({ ok: true, json: () => Promise.resolve({}) })

    const { getAllByText } = renderWithUser(fetchMock)

    fireEvent.click(getAllByText('Get Summary')[0])
    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith(expect.stringContaining('/ai/summary'), expect.any(Object))
    })

    fireEvent.click(getAllByText('Merge Advice')[0])
    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith(expect.stringContaining('/ai/merge'), expect.any(Object))
    })
  })
})
