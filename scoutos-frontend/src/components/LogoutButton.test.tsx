import { describe, it, expect, vi } from 'vitest'
import { render, fireEvent } from '@testing-library/react'
import LogoutButton from './LogoutButton'
import { UserContext, type User } from '../context/UserContext'

function renderWithProvider(setUser: (u: User | null) => void) {
  return render(
    <UserContext.Provider value={{ user: { id: 1, username: 'bob', token: 'abc' }, setUser }}>
      <LogoutButton />
    </UserContext.Provider>
  )
}

describe('LogoutButton', () => {
  it('calls setUser(null) on click', () => {
    const setUser = vi.fn()
    const { getByRole } = renderWithProvider(setUser)
    fireEvent.click(getByRole('button', { name: /logout/i }))
    expect(setUser).toHaveBeenCalledWith(null)
  })
})
