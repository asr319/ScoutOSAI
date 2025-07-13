import { describe, it, vi, expect, beforeEach, afterEach } from 'vitest'
import { render, screen, fireEvent, waitFor, cleanup } from '@testing-library/react'
import AuthForm from './AuthForm'
import { UserContext, type User } from '../context/UserContext'

function renderWithProvider(setUser: (u: User | null) => void) {
  return render(
    <UserContext.Provider value={{ user: null, setUser }}>
      <AuthForm />
    </UserContext.Provider>
  )
}

describe('AuthForm', () => {
  beforeEach(() => {
    vi.resetAllMocks()
  })
  afterEach(() => {
    vi.restoreAllMocks()
    cleanup()
  })

  it('renders inputs', () => {
    const { container } = renderWithProvider(() => {})
    expect(container.querySelector('input')).toBeTruthy()
  })

  it('submits login data', async () => {
    const setUser = vi.fn()
    const fetchMock = vi.fn().mockResolvedValue({ ok: true, json: () => Promise.resolve({ id: 1, token: 't' }) })
    vi.stubGlobal('fetch', fetchMock)

    renderWithProvider(setUser)

    fireEvent.change(screen.getAllByPlaceholderText('Username')[0], { target: { value: 'bob' } })
    fireEvent.change(screen.getAllByPlaceholderText('Password')[0], { target: { value: 'pw' } })
    fireEvent.click(screen.getAllByRole('button', { name: /login/i })[0])

    await waitFor(() => {
      expect(fetchMock).toHaveBeenCalled()
    })
    await waitFor(() => {
      expect(setUser).toHaveBeenCalled()
    })
    expect(setUser).toHaveBeenCalledWith({ id: 1, username: 'bob', token: 'abc' })
  })

  it('registers then logs in', async () => {
    const setUser = vi.fn()
    const fetchMock = vi
      .fn()
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ id: 2 }) })
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve({ id: 2, token: 'x' }) })
    vi.stubGlobal('fetch', fetchMock)

    renderWithProvider(setUser)

    fireEvent.click(screen.getAllByText('Need an account? Register')[0])
    fireEvent.change(screen.getAllByPlaceholderText('Username')[0], { target: { value: 'alice' } })
    fireEvent.change(screen.getAllByPlaceholderText('Password')[0], { target: { value: 'pw' } })
    const regButtons = screen.getAllByRole('button', { name: /^Register$/i })
    regButtons.forEach(btn => fireEvent.click(btn))

    await waitFor(() => {
      expect(setUser).toHaveBeenCalledWith({ id: 2, username: 'alice', token: 'abc' })
    })
  })
})
