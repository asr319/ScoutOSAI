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
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve([]) }) // list
      .mockResolvedValue({ ok: true, json: () => Promise.resolve({ response: 'merge!' }) })

    const { getAllByText, getAllByPlaceholderText, getByText, findByText } = renderWithUser(fetchMock)

    fireEvent.change(getAllByPlaceholderText('Content')[0], { target: { value: 'foo' } })
    fireEvent.click(getByText('Suggest Tags'))
    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith(expect.stringContaining('/ai/tags'), expect.any(Object))
    })

    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(2))

    fireEvent.click(getAllByText('Merge Advice')[0])
    await waitFor(() => {
      expect(
        fetchMock.mock.calls.some(
          c => (c[0] as string).includes('/ai/merge')
        )
      ).toBe(true)
    })
    expect(await findByText('merge!')).toBeTruthy()
  })
})
